from pyats import aetest
from pyats.topology import loader

tb = loader.load('modul6/part1/testbed_example.yaml')


class Example(aetest.Testcase):
    @aetest.test
    def connect_to_devices(self):
        dev = tb.devices['CSR']
        conn = dev.connections.rest
        username = conn.credentials.login.username
        password = conn.credentials.login.password.plaintext
        conn_class = conn['class'](dev)
        conn_class.connect(connection=conn, username=username, password=password)
        out = conn_class.get_interface('GigabitEthernet1')
        print(out)


if __name__ == '__main__':
    aetest.main()

