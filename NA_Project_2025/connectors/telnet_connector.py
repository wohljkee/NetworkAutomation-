import ipaddress
import logging
import re
# pylint: disable=deprecated-module
import telnetlib
import time
from typing import Optional

from pyats.datastructures import AttrDict
from pyats.topology import Device

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TelnetConnector:
    """
    Class used for telnet connections and methods

    Contributors: Dusca Alexandru, Furmanek Carina, Jude Victor, Ivaschescu Gabriel
    """
    def __init__(self, device: Device):
        self.device = device
        self._conn: Optional[telnetlib.Telnet] = None
        self.connection: Optional[AttrDict] = None

    def connect(self, **kwargs):
        """
        Connects to the device using Telnet
        """
        self.connection = kwargs['connection']
        self._conn = telnetlib.Telnet(
            host=self.connection.ip.compressed,
            port=self.connection.port,
        )

    def read(self) -> str:
        """
        Reads any immediate output from the device
        """
        return self._conn.read_very_eager().decode()

    def write(self, command: str) -> None:
        """
        Sends command followed by newline
        """
        self._conn.write(command.encode() + b'\n')

    def write_raw(self, command: str) -> str:
        """
        Writes a command without newline
        """
        self._conn.write(command.encode())
        return self._conn.read_very_eager().decode()

    def contains(self, pattern: list[str]) -> bool:
        """
        Checks if any of the given patterns appear in output
        """
        out = self.read()
        return any(p in out for p in pattern)

    def execute(self, command: str, **kwargs):
        """
        Sends a command and waits for one of the prompt patterns
        """
        if not self._conn:
            raise RuntimeError('Connection is not established')
        prompt: list[bytes] = list(map(lambda s: s.encode(), kwargs['prompt']))
        self._conn.write(f'{command}\n'.encode())
        if kwargs.get('timeout'):
            time.sleep(kwargs['timeout'])
        response = self._conn.expect(prompt)
        return response[2].decode('utf8') if isinstance(response, tuple) else response

    def configure_initial_interface(self):
        """
        Configures the initial interface with IP address and brings it up
        """
        for iface_name, interface in self.device.interfaces.items():
            if interface.type != 'ethernet' or not interface.ipv4:
                continue

            ip = interface.ipv4.ip.compressed
            mask = interface.ipv4.network.netmask.exploded
            logger.info(f"Configuring interface {iface_name} with IP {ip} {mask}")
            self.execute(f'interface {iface_name}', prompt=[r'\(config-if\)#'])
            self.execute(f'ip address {ip} {mask}', prompt=[r'\(config-if\)#'])
            self.execute('no shutdown', prompt=[r'\(config-if\)#'])
            self.execute('exit', prompt=[r'\(config\)#'])

    def configure_ssh(self):
        """
        Enables SSH access with local login
        """
        username = self.device.connections.ssh.credentials.login.username
        password = self.device.connections.ssh.credentials.login.password.plaintext
        self.execute('ip ssh version 2', prompt=[r'\(config\)#'])
        self.execute(f'username {username} privilege 15 secret {password}', prompt=[r'\(config\)#'])
        self.execute('ip domain name cisco.com', prompt=[r'\(config\)#'])
        self.execute('crypto key generate rsa modulus 2048', prompt=[r'\(config\)#'])
        self.execute('line vty 0 4', prompt=[r'\(config-line\)#'])
        self.execute('transport input ssh', prompt=[r'\(config-line\)#'])
        self.execute('login local', prompt=[r'\(config-line\)#'])
        self.execute('exit', prompt=[r'\(config\)#'])

    def configure_ftd(self):
        """
        Goes through the initial setup of FTD
        """
        creds = self.device.credentials
        mgmt = self.device.interfaces['GigabitEthernet0/0'].ipv4
        mgmt_ip, mask = mgmt.ip.compressed, mgmt.network.netmask.exploded
        gateway = ipaddress.ip_address(self.device.custom['mgmt_gw']).compressed
        dns = ipaddress.ip_address(self.device.custom['dns']).compressed
        domain = self.device.custom['domain']

        self.write('\n\r')
        time.sleep(2)
        out = self.read()

        if re.search(r'(firepower) login:', out):
            logger.info("Attempting FTD login")
            if 'Password:' in out:
                self.execute('\n', prompt=[r'FTD login\:'])
            self.write(creds.default.username)
            time.sleep(3)
            out = self.read()
            self.write(
                creds.login.password.plaintext if 'Enter new password:' in out else creds.default.password.plaintext)
            time.sleep(5)
            out = self.read()

        if any(k in out for k in ['Press <ENTER>', 'You must change', '--More--']):
            logger.info("Proceeding through FTD setup")
            if 'Press <ENTER>' in out or '--More--' in out:
                for _ in range(20):
                    out = self.write_raw(' ')
                    time.sleep(.3)
                    if 'AGREE to the EULA' in out:
                        print(f'Printing: {out}')
                        self.execute('YES', prompt=[r'Enter new password\:'])

            cmds = [
                (creds.login.password.plaintext, r'Confirm new password:'),
                (creds.login.password.plaintext, r'IPv4\? \(y/n\) \[y\]:'),
                ('y', r'IPv6\? \(y/n\) \[n\]:'),
                ('n', r'\(dhcp\/manual\) \[manual\]:'),
                ('manual', r'management interface \[.*\]:'),
                (mgmt_ip, r'netmask for the management interface \[.*\]:'),
                (mask, r'gateway for the management interface \[.*\]:'),
                (gateway, r'fully qualified hostname for this system \[.*\]:'),
                ('firepower', r'comma\-separated list of DNS servers or \'none\' \[.*\]:'),
                (dns, r'comma\-separated list of search domains or \'none\' \[\]:'),
                (domain, r'Manage the device locally\? \(yes\/no\) \[yes\]:')
            ]
            for cmd, prompt in cmds:
                self.execute(cmd, prompt=[prompt])
            self.write('yes')

            # Wait for setup to finish
            for _ in range(10):
                time.sleep(2)
                if '>' in self.read():
                    logger.info("FTD setup completed.")
                    return
            logger.error("FTD setup timed out.")
        elif 'Login incorrect' in out:
            logger.error("FTD default credentials failed.")

    def enable_secret(self):
        """
        Sets the enable secret password
        """
        enable_pass = self.device.credentials.default.enable_password.plaintext
        self.execute(f'enable secret {enable_pass}', prompt=[r'\(config\)#'])

    def save_config(self):
        """
        Saves the running configuration
        """
        self.execute('end', prompt=[r'\w+#'])
        self.write('write memory')
        if self.contains(['Continue? [no]:', '[confirm]']):
            self.execute('yes', prompt=[r'\w+#'])
        self.execute('', prompt=[r'\w+#'])

    def configure_routes(self):
        if not self.device.custom.get('routes'):
            return
        for route in self.device.custom['routes'].values():
            net = ipaddress.IPv4Network(route['network'])
            self.execute(
                f"ip route {net.network_address} {net.netmask} {route['via']} 150",
                prompt=[r'\(config\)#']
            )

    def do_initial_config(self):
        """
        Performs initial setup for IOS/IOSv devices
        """
        if self.device.os in ('ios', 'iosxe'):
            self.write('\r')
            time.sleep(1)
            self.write('en')
            time.sleep(1)
            out = self.read()
            if 'Password:' in out:
                self.execute(self.device.credentials.default.enable_password.plaintext,
                             prompt=[r'\w+#'])
            self.execute('conf t', prompt=[r'\(config\)#'])
            self.execute(f'hostname {self.device.custom.hostname}', prompt=[r'\(config\)#'])

            self.configure_initial_interface()
            self.configure_routes()
            self.configure_ssh()
            if self.device.platform == 'iou':
                self.enable_secret()
            self.save_config()

    def is_connected(self) -> bool:
        """
        Returns the current status of Telnet connection
        """
        return not self._conn.eof

    def disconnect(self):
        """
        Closes the connection
        """
        self._conn.close()
