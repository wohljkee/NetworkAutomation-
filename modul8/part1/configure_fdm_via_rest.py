"""Added docstrings for module"""

import ssl

from pyats import aetest
from pyats.aetest.steps import Steps
from pyats.topology import loader

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

        with steps.start('Change DHCP server'):
            dhcp_servers = swagger.client.DHCPServerContainer.getDHCPServerContainerList().result()
            for dhcp_server in dhcp_servers['items']:
                dhcp_server.servers = []
                result = swagger.client.DHCPServerContainer.editDHCPServerContainer(
                    objId=dhcp_server.id,
                    body=dhcp_server
                ).result()
                print(result)

        with steps.start('create security zone'):
            ref = swagger.client.get_model('ReferenceModel')
            phy = swagger.client.Interface.getPhysicalInterfaceList().result()['items'][2]
            security_zone = swagger.client.get_model('SecurityZone')
            sz = security_zone(
                name='AutoCreated1',
                mode='ROUTED',
                interfaces=[ref(id=phy.id, name=phy.name, hardwareName=phy.hardwareName, type=phy.type)]
            )
            result = swagger.client.SecurityZone.addSecurityZone(body=sz).result()
            print(result)

        with steps.start("configure Interface"):
            existing_object = swagger.client.Interface.getPhysicalInterfaceList().result()['items']
            for obj in existing_object:
                if obj.hardwareName == 'GigabitEthernet0/0':
                    obj.ipv4.ipAddress.ipAddress = device_fdm.interfaces['GigabitEthernet0/0'].ipv4.ip.compressed
                    obj.ipv4.ipAddress.netmask = device_fdm.interfaces['GigabitEthernet0/0'].ipv4.netmask.compressed
                    obj.enabled = True
                    obj.ipv4.dhcp = False
                    obj.ipv4.ipType = 'STATIC'
                elif obj.hardwareName == 'GigabitEthernet0/1':
                    obj.ipv4.ipAddress.ipAddress = device_fdm.interfaces['GigabitEthernet0/1'].ipv4.ip.compressed
                    obj.ipv4.ipAddress.netmask = device_fdm.interfaces['GigabitEthernet0/1'].ipv4.netmask.compressed
                    obj.enabled = True
                    obj.ipv4.dhcp = False
                    obj.ipv4.ipType = 'STATIC'
                else:
                    continue
                result = swagger.client.Interface.editPhysicalInterface(objId=obj.id, body=obj).result()
                print(result)

        with steps.start('Create network object'):
            network_object = swagger.client.get_model('NetworkObject')

        with steps.start('Deploy configuration'):
            response = swagger.client.Deployment.addDeployment().result()
            for _ in range(10):
                tasks = swagger.client.Deployment.getDeployment(objId=response.id).result()
                status = tasks['deploymentStatusMessages'][-1]
                if status.taskState == "FINISHED":
                    break
            else:
                print("Deployment failed")


if __name__ == '__main__':
    aetest.main()
