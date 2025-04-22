from pyats import aetest
from pyats.topology import loader

from modul6.part1.telnet_connector import TelnetConnector

tb = loader.load('testbed_example.yaml')


class Example(aetest.Testcase):

    @aetest.test
    def connect_to_devices(self):
        dev = tb.devices['CSR']
        conn = dev.connections.telnet['class'](dev)  # type: TelnetConnector
        conn.connect(connection=dev.connections.telnet)
        conn.do_initial_configuration()
        conn.enable_rest()
        conn.disconnect()

    @aetest.test
    def test_rest_connection(self):
        pass




if __name__ == '__main__':
    aetest.main()
