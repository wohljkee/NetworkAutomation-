import logging
from typing import Dict

from pyats import aetest
from pyats.aetest.steps import Steps
from pyats.topology import loader

from connectors.ssh_connector import SSHConnector
from connectors.telnet_connector import TelnetConnector
from ubuntu_config import configure as configure_ubuntu_server

testbed = loader.load('testbed_config.yaml')

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, encoding='utf-8')

"""
Contributor: Dusca Alexandru
"""
class SetupTelnetConnections(aetest.CommonSetup):
    """
    Setup Phase: Initialize and connect to devices via Telnet
    """

    @aetest.subsection
    def initialize_telnet_objects(self):
        """Create a dictionary to store TelnetConnector objects"""
        self.parent.parameters['telnet_objects'] = {}

    @aetest.subsection
    def connect_telnet_devices(self, telnet_objects: Dict[str, TelnetConnector]):
        """Connects all devices with a Telnet connection in the testbed"""
        for dev_name, dev in testbed.devices.items():
            if 'telnet' not in dev.connections:
                log.info(f"No Telnet connection for '{dev_name}'")
                continue

            telnet_class = dev.connections.telnet.get('class')
            if not telnet_class:
                log.warning(f"Telnet class not defined for '{dev_name}'")
                continue

            try:
                log.info(f"Connecting to '{dev_name}' via Telnet...")
                conn = telnet_class(dev)
                conn.connect(connection=dev.connections.telnet)
                telnet_objects[dev_name] = conn
                log.info(f"Successfully connected to '{dev_name}'")
            except Exception as e:
                log.error(f"[ERROR] Could not connect to '{dev_name}': {e}")


class TelnetDeviceConfiguration(aetest.Testcase):
    """Configure all devices connected via Telnet"""

    @aetest.test
    def configure_ubuntu_first(self, steps: Steps):
        """Run ubuntu server configuration before configuring routers"""
        with steps.start("Configure Ubuntu Server"):
            try:
                configure_ubuntu_server(testbed.devices['UbuntuServer'])
                log.info("Ubuntu Server configured successfully")
            except Exception as e:
                log.error(f"Ubuntu Server configuration failed: {e}")
                self.failed("Failed to configure Ubuntu Server", goto=['next_tc'])

    @aetest.test
    def configure_telnet_devices(self, steps: Steps, telnet_objects: Dict[str, TelnetConnector]):
        """Iterate over telnet-connected devices and apply configs"""
        for dev_name, connector in telnet_objects.items():
            with steps.start(f"Configuring {dev_name}"):
                try:
                    if connector.device.os == 'ftd':
                        connector.configure_ftd()
                    else:
                        connector.do_initial_config()
                        # continue
                    log.info(f"Successfully configured '{dev_name}'")
                except Exception as e:
                    log.error(f"Failed to configure '{dev_name}': {e}")


class SSHDeviceConfiguration(aetest.Testcase):
    @aetest.test
    def create_ssh_connection_objects(self):
        """Creates SSH connection dictionary to store the objects"""
        self.parent.parameters['ssh_objects'] = {}

    @aetest.test
    def connect_all_devices_via_ssh(self, ssh_objects: dict[str, SSHConnector]):
        """Connects all testbed devices via SSH and stores objects"""
        for dev_name, dev in testbed.devices.items():
            if dev.type != 'router':
                log.info(f"[SKIP] Device '{dev_name}' is type '{dev.type}', skipping SSH connection")
                continue
            if 'ssh' not in dev.connections:
                log.warning(f"Device '{dev_name}' has no SSH connection defined, skipping")
                continue
            try:
                ssh_class = dev.connections.ssh.get('class', None)
                if not ssh_class:
                    log.warning(f"Device '{dev_name}' SSH connection has no 'class' defined, skipping")
                    continue

                log.info(f"Connecting to device '{dev_name}' via SSH...")
                ssh_conn = ssh_class(dev)
                ssh_conn.connect(connection=dev.connections.ssh)
                ssh_objects[dev_name] = ssh_conn
                log.info(f"Successfully connected to device '{dev_name}'")

            except Exception as e:
                log.error(f"Failed to connect to device '{dev_name}' via SSH: {e}")

    @aetest.test
    def configure_all_devices(self, steps: Steps, ssh_objects: dict[str, SSHConnector]):
        """Configures all connected devices"""
        for dev_name, connector in ssh_objects.items():
            with steps.start(f"Configuring {dev_name}"):
                log.info(f"Configuring device '{dev_name}'...")
                connector.configure()
                log.info(f"Finished configuring device '{dev_name}'")


class ConnectionToFTD(aetest.Testcase):
    """Connects to the FTD via Swagger REST API and performs simple verification"""

    @aetest.setup
    def setup(self):
        """Initialize Swagger connection to FTD"""
        self.swagger_objects = {}

        for dev_name, dev in testbed.devices.items():
            if dev.os != 'ftd':
                log.info(f"[SKIP] Device '{dev_name}' is not FTD, skipping.")
                continue

            conn_info = dev.connections.get('rest')
            if not conn_info or 'class' not in conn_info:
                log.warning(f"[SKIP] Device '{dev_name}' has no proper REST connection.")
                continue

            try:
                log.info(f"Connecting to FTD '{dev_name}' via Swagger API...")
                connector_class = conn_info['class']
                swagger_conn = connector_class(dev)
                swagger_conn.connect(connection=conn_info)
                self.swagger_objects[dev_name] = swagger_conn
                log.info(f"Successfully connected to FTD device '{dev_name}'")
            except Exception as e:
                log.error(f"Failed to connect to '{dev_name}' via Swagger: {e}")
                self.failed(f"Swagger connection failed: {e}")


# class CommonCleanup(aetest.CommonCleanup):
#
#     @aetest.subsection
#     def disconnect_ssh(self, ssh_objects):
#         """Disconnects all SSH sessions."""
#         for name, conn in ssh_objects.items():
#             conn.disconnect()


if __name__ == '__main__':
    aetest.main()