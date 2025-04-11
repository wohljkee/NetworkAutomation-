from pyats import aetest
from pyats.topology import loader

from modul4.part2.csr_conf_paramiko import username
from modul5.ssh_connector import SSHConnector
from modul5.telnet_connector import TelnetConnector

tb = loader.load('modul5/testbed_example.yaml')


class Example(aetest.Testcase):

    @aetest.test
    def connect_to_devices(self):
        conn = tb.devices['IOU1'].connections.ssh
        conn_obj = conn['class']() # type: SSHConnector
        conn_obj.connect(username=conn.usename, password=conn.password)
        conn_obj.do_initial_configuration()
        conn_obj.get_device_details()

if __name__ == '__main__':
    aetest.main()
