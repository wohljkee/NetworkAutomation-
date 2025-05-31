

from pyats.aetest.steps import Steps
from connectors.swagger_connector import SwaggerConnector


def configure_interfaces(steps: Steps, swagger: SwaggerConnector):
    """
    Configures ipv4 addresses on interfaces

    Contributors: Dusca Alexandru, Furmanek Carina
    """
    with steps.start("Configuring Interface"):
        existing_object = swagger.client.Interface.getPhysicalInterfaceList().result()['items']
        for obj in existing_object:
            if obj.hardwareName == 'GigabitEthernet0/0':
                interface_ip = device.interfaces['GigabitEthernet0/0'].ipv4.ip.compressed
                interface_mask = device.interfaces['GigabitEthernet0/0'].ipv4.netmask.compressed
                obj.ipv4.ipAddress.ipAddress = interface_ip
                obj.ipv4.ipAddress.netmask = interface_mask
                obj.enabled = True
                obj.ipv4.dhcp = False
                obj.ipv4.ipType = 'STATIC'
            elif obj.hardwareName == 'GigabitEthernet0/1':
                interface_ip = device.interfaces['GigabitEthernet0/1'].ipv4.ip.compressed
                interface_mask = device.interfaces['GigabitEthernet0/1'].ipv4.netmask.compressed
                obj.ipv4.ipAddress.ipAddress = interface_ip
                obj.ipv4.ipAddress.netmask = interface_mask
                obj.enabled = True
                obj.ipv4.dhcp = False
                obj.ipv4.ipType = 'STATIC'
            else:
                continue
            swagger.client.Interface.editPhysicalInterface(objId=obj.id, body=obj).result()