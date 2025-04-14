from napalm import *
from pyats import aetest
from pyats.topology import loader


tb = loader.load('testbed_example.yaml')


class Example(aetest.Testcase):

    @aetest.test
    def connect_to_devices(self):
        dev = tb.devices['IOU1']
        conn = dev.connections.ssh
        username = conn.credentials.login.username
        password = conn.credentials.login.password.plaintext
        driver = get_network_driver('ios')

        e = driver(str(conn.ip), username, password)
        e.open()
        response = e.get_interfaces()
        print(type(response))
        print(response)

    @aetest.test
    def use_napalm(self):
        dev = tb.devices['IOU1']
        # e = dev.connect(alias='napalm', via='napalm')
        conn = dev.connections.napalm
        c = conn['class']
        driver = c.get_network_driver('ios')
        username = conn.credentials.login.username
        password = conn.credentials.login.password.plaintext
        e = driver(str(conn.ip), username, password)
        e.open()
        response = e.get_interfaces()
        print(response)



if __name__ == '__main__':
    aetest.main()
