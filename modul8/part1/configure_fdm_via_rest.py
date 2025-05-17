"""Added docstrings for module"""

from pyats import aetest
from pyats.aetest.steps import Steps
from pyats.topology import loader

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from lib.swagger_connector import SwaggerConnector

tb = loader.load('testbed_example.yaml')
device_fdm = tb.devices['FTD']


class Example3(aetest.Testcase):
    @aetest.test
    def configure_fdm_interface(self, steps: Steps):
        with steps.start('Connect to FDM'):
            swagger: SwaggerConnector = device_fdm.connections.rest['class'](device_fdm)
            swagger.connect(connection=device_fdm.connections.rest)
        with steps.start('create security zone'):
            security_zone = swagger.client.get_model('SecurityZone')


        with steps.start("configure Interface"):
            interface = swagger.client.get_model('PhysicalInterface')


        with steps.start('Create network object'):
            network_object = swagger.client.get_model('NetworkObject')


if __name__ == '__main__':
    aetest.main()
