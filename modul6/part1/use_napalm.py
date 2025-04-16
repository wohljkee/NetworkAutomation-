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
        config = e.get_config()
        with open('config.cfg', 'w') as file:
            file.write(config['startup'])
        # do changes to config
        with open('config.cfg', 'r') as file:
            modified_config = file.read()

        e.load_merge_candidate(config='''interface Ethernet0/1
 ip address 192.168.102.1 255.255.255.0
        ''')
        e.replace_merge_candidate(config=modified_config)

        save = e.commit_config()
        print(config)



if __name__ == '__main__':
    aetest.main()
