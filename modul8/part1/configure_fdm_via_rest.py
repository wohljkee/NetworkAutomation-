"""Added docstrings for module"""
import ipaddress

from pyats import aetest
from pyats.aetest.steps import Steps, Step  # pylint: disable=unused-import
from pyats.topology import loader
from genie.libs.conf.ospf.ospf import Ospf
from genie.libs.conf.interface.iosxe import Interface

from lib.swagger_connector import SwaggerConnector

# from genie.libs.conf.device import Device

tb = loader.load('testbed_example2.yaml')
device_fdm = tb.devices['FTD']



class Example3(aetest.Testcase):
    @aetest.test
    def configure_fdm_interface(self, steps: Steps):
        with steps.start('Connect to FDM'):
            conn: SwaggerConnector = device_fdm.connections.rest['class'](device_fdm)



if __name__ == '__main__':
    aetest.main()
