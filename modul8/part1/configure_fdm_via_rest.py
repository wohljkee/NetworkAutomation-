"""Added docstrings for module"""

from pyats import aetest
from pyats.aetest.steps import Steps
from pyats.topology import loader

from lib.swagger_connector import SwaggerConnector

tb = loader.load('testbed_example.yaml')
device_fdm = tb.devices['FTD']


class Example3(aetest.Testcase):
    @aetest.test
    def configure_fdm_interface(self, steps: Steps):
        with steps.start('Connect to FDM'):
            swagger: SwaggerConnector = device_fdm.connections.rest['class'](device_fdm)
            swagger.connect(connection=device_fdm.connections.rest)


if __name__ == '__main__':
    aetest.main()
