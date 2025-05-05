import ipaddress

from pyats import aetest
from pyats.aetest.steps import Steps, Step
from pyats.topology import loader
from genie.libs.conf.ospf.ospf import Ospf
from genie.libs.conf.interface.iosxe import Interface

tb = loader.load('testbed_example2.yaml')
device_csr = tb.devices['em-r2']
device_iosv = tb.devices['IOSv15']


class Example(aetest.Testcase):

    @aetest.test
    def configure_ospf_csr(self, steps: Steps):
        with steps.start('Connect to device'):
            device_csr.connect(log_stdout=True)

        with steps.start('Create Interface Object CSR'):
            intf = Interface(name='GigabitEthernet2')
            intf.device = device_csr
            intf.ipv4 = ipaddress.IPv4Interface('192.168.105.1/24')
            config = intf.build_config(apply=False)
            device_csr.configure(config.cli_config.data)

        with steps.start('Configure OSPF on CSR'):
            ospf = Ospf()
            ospf.device_attr[device_csr].vrf_attr['default'].instance = '1'
            ospf.device_attr[device_csr].vrf_attr['default'].router_id = '192.168.102.2'
            area = ospf.device_attr[device_csr].vrf_attr['default'].area_attr[0]
            area.area = 0
            area.networks.append('192.168.105.0 0.0.0.255')
            ospf.build_config(devices=[device_csr])


class Example2(aetest.Testcase):
    @aetest.test
    def configure_ospf_iosv(self, steps: Steps):
        with steps.start('Connect to IOSv'):
            device_iosv.connect(log_stdout=True)

        with steps.start('Create Interface Object IOSv'):
            intf_name = 'to_FTD'
            intf = device_iosv.interfaces[intf_name]
            intf = Interface(name=intf.name)
            intf.device = device_iosv
            intf.ipv4 = intf.ipv4
            config = intf.build_config(apply=False)
            device_iosv.configure(config.cli_config.data)

        with steps.start('Configure OSPF on IOSV'):
            ospf = Ospf()
            ospf.device_attr[device_iosv].vrf_attr['default'].instance = '1'
            ospf.device_attr[device_iosv].vrf_attr['default'].router_id = '192.168.103.2'
            area = ospf.device_attr[device_iosv].vrf_attr['default'].area_attr[0]
            area.area = 0
            area.networks.append('192.168.107.0 0.0.0.255')
            ospf.build_config(devices=[device_iosv])


if __name__ == '__main__':
    aetest.main()
