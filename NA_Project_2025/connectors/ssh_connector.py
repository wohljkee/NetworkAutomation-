import ipaddress
import logging
import re
import time
from ipaddress import IPv4Address, IPv4Interface

from paramiko import SSHClient, AutoAddPolicy, Transport
from pyats.topology import Device

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Transport._preferred_kex = (
# #     'diffie-hellman-group14-sha1',
# #     'diffie-hellman-group-exchange-sha1',
# #     'diffie-hellman-group1-sha1',
# )

class SSHConnector:
    """
    Class used for ssh connections and methods

    Contributors: Dusca Alexandru, Furmanek Carina, Jude Victor, Ivaschescu Gabriel
    """
    def __init__(self, device: Device):
        self.device = device
        self._ssh = SSHClient()

        # Automatically accept new/unknown SSH host keys (prevents yes/no prompt)
        self._ssh.set_missing_host_key_policy(AutoAddPolicy())
        self._shell = None

    def connect(self, **kwargs):
        conn = kwargs['connection']
        self._ssh.connect(
            hostname=conn.ip.compressed,
            port=conn.port or 22,
            username=conn.credentials.login.username,
            password=conn.credentials.login.password.plaintext,
            look_for_keys = False,
            allow_agent = False,
            disabled_algorithms = {
                "kex": [
                    "curve25519-sha256",
                    "curve25519-sha256@libssh.org",
                    "ecdh-sha2-nistp256",
                    "ecdh-sha2-nistp384",
                    "ecdh-sha2-nistp521",
                ]
            }
        )
        self._shell = self._ssh.invoke_shell()
        self._shell.recv(65535)  # Clear banner or leftover output

    def _send_cmd(self, cmd: str, prompts: list[str] = None, delay: float = 0.5, timeout: float = 0) -> str:
        logger.info(f"Sending command: {cmd}")
        self._shell.send(f'{cmd}\n')
        time.sleep(delay + timeout)

        output = ""
        while self._shell.recv_ready():
            output += self._shell.recv(65535).decode(errors='ignore')
            time.sleep(0.2)

        logger.info(f"Output:\n{output}")

        if "% Incomplete command" in output:
            raise RuntimeError(f"Incomplete command detected for '{cmd}':\n{output}")

        if prompts:
            if not any(re.search(p, output) for p in prompts):
                raise RuntimeError(f"Expected prompt(s) {prompts} not found in output:\n{output}")

        return output

    def is_connected(self) -> bool:
        return not self._shell.closed

    def disconnect(self):
        self._ssh.close()

    def read(self) -> str:
        return self._shell.recv(65535).decode() if self._shell.recv_ready() else ''

    def configure_interfaces(self):
        for intf in self.device.interfaces.values():
            self._send_cmd(f"interface {intf.name}", prompts=[r'\(config-if\)#'])
            if intf.ipv4:
                ip = intf.ipv4.ip.compressed
                mask = intf.ipv4.network.netmask.exploded
                self._send_cmd(f"ip address {ip} {mask}", prompts=[r'\(config-if\)#'])
            else:
                self._send_cmd("ip address dhcp", prompts=[r'\(config-if\)#'])
            self._send_cmd("no shutdown", prompts=[r'\(config-if\)#'])
            self._send_cmd("exit", prompts=[r'\(config\)#'])

    def configure_rip(self):
        rip_cfg = self.device.custom.get('rip')
        if self.device.type != 'router' or not rip_cfg:
            return
        self._send_cmd("router rip", prompts=[r'\(config-router\)#'])
        self._send_cmd("version 2", prompts=[r'\(config-router\)#'])
        self._send_cmd("no auto-summary", prompts=[r'\(config-router\)#'])
        for net_str in rip_cfg.get('networks', []):
            net = ipaddress.IPv4Network(net_str)
            self._send_cmd(f"network {net.network_address}", prompts=[r'\(config-router\)#'])
        for iface in rip_cfg.get('passive-interfaces', []):
            self._send_cmd(f"passive-interface {iface}", prompts=[r'\(config-router\)#'])
        self._send_cmd("exit", prompts=[r'\(config\)#'])


    def configure_ospf(self):
        if self.device.type != 'router' or not self.device.custom.get('ospf_enabled'):
            return
        ospf_process_id = 1
        ospf_area = 0
        self._send_cmd(f"router ospf {ospf_process_id}", prompts=[r'\(config-router\)#'])
        for intf in self.device.interfaces.values():
            if hasattr(intf, 'ipv4') and intf.ipv4:
                ip: IPv4Interface = intf.ipv4
                network = ip.network.network_address
                wildcard_mask = ip.hostmask.exploded
                self._send_cmd(
                    f'network {network} {wildcard_mask} area {ospf_area}',
                    prompts=[r'\(config-router\)#']
                )
        # Optionally make interfaces passive if marked
        passive_interfaces = self.device.custom.get('ospf_passive_interfaces', [])
        for iface_name in passive_interfaces:
            self._send_cmd(f'passive-interface {iface_name}', prompts=[r'\(config-router\)#'])
        self._send_cmd('exit', prompts=[r'\(config\)#'])
        self._send_cmd('do show run | sect ospf', prompts=[r'\(config\)#'])

    def configure_dhcp_pools(self):
        pools = self.device.custom.get('dhcp_pools', {})
        for name, pool in pools.items():
            self._send_cmd(f"ip dhcp pool {name}", prompts=[r'\(dhcp-config\)#'])
            net = ipaddress.IPv4Network(pool['network'])
            self._send_cmd(f"network {net.network_address} {net.netmask}", prompts=[r'\(dhcp-config\)#'])
            self._send_cmd(f"default-router {pool['default_router']}", prompts=[r'\(dhcp-config\)#'])
            if pool.get('domain_name'):
                self._send_cmd(f"domain-name {pool['domain_name']}", prompts=[r'\(dhcp-config\)#'])
            if pool.get('dns_server'):
                self._send_cmd(f"dns-server {pool['dns_server']}", prompts=[r'\(dhcp-config\)#'])
            self._send_cmd("exit", prompts=[r'\(config\)#'])
            for rng in pool.get('excluded_address_ranges', []):
                self._send_cmd(f"ip dhcp excluded-address {rng['start']} {rng['end']}", prompts=[r'\(config\)#'])

    def save_config(self):
        self._send_cmd('end', prompts=[r'#'])
        output = self._send_cmd('write', prompts=[], timeout=5)
        if 'Continue? [no]:' in output or '[confirm]' in output:
            self._send_cmd('yes', prompts=[r'#'])
        self._send_cmd('', prompts=[r'#'])

    def configure(self):
        if self.device.os not in ('ios', 'iosxe'):
            return

        self._send_cmd('enable', prompts=[r'#'])
        self._send_cmd('configure terminal', prompts=[r'\(config\)#'])

        hostname = self.device.custom.hostname
        self._send_cmd(f'hostname {hostname}', prompts=[fr'{hostname}\(config\)#'])

        self.configure_interfaces()
        self.configure_rip()
        self.configure_ospf() # testing ospf configuration
        self.configure_dhcp_pools()

        self.save_config()
