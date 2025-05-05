import ipaddress

from pyats import aetest
from pyats.aetest.steps import Steps, Step
from pyats.topology import loader
from genie.libs.conf.ospf.ospf import Ospf
from genie.libs.conf.interface.iosxe import Interface

tb = loader.load('testbed_example2.yaml')
device = tb.devices['em-r2']


class Example(aetest.Testcase):

    @aetest.test
    def configure_ospf_scr(self, steps: Steps):
        with steps.start('Connect to device'):
            device.connect(log_stdout=True)

        with steps.start('Create Interface Object'):
            intf = Interface(name='GigabitEthernet2')
            intf.device = device
            intf.ipv4 = ipaddress.IPv4Interface('192.168.105.1/24')
            config = intf.build_config(apply=False)
            device.configure(config.cli_config.data)

        with steps.start('Configure OSPF'):
            ospf = Ospf()
            ospf.device_attr[device].vrf_attr['default'].instance = '1'
            ospf.device_attr[device].vrf_attr['default'].router_id = '192.168.102.2'
            ospf.device_attr[device].vrf_attr['default'].area_attr[0].area = 0
            ospf.build_config(devices=[device])


if __name__ == '__main__':
    aetest.main()
