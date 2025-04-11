from pyats import aetest
from pyats.topology import loader

from modul5.telnet_connector import TelnetConnector

tb = loader.load('modul5/testbed_example.yaml')


class Example(aetest.Testcase):

    @aetest.test
    def connect_to_devices(self):
        conn = tb.devices['IOU1'].connections.ssh['class']() # type: TelnetConnector
        print(conn)
        print(tb.devices['IOU1'].connections.ssh)

if __name__ == '__main__':
    aetest.main()
