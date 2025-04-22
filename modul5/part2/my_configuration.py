from pyats import aetest
from pyats.topology import loader

from modul5.part2.telnet_connector import TelnetConnector

tb = loader.load('testbed_example.yaml')


class Example(aetest.Testcase):

    @aetest.test
    def connect_to_devices(self):
        dev = tb.devices['IOU1']
        conn = dev.connections.telnet['class'](dev)  # type: TelnetConnector
        conn.connect(connection=dev.connections.telnet)
        conn.do_initial_configuration()
        conn.disconnect()

    def use_napalm(self):
        pass



if __name__ == '__main__':
    aetest.main()
