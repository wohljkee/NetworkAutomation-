import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
from typing import Optional

from pyats.datastructures import AttrDict
from pyats.topology import Device


class RESTConnector:

    def __init__(self, device: Device, **kwargs):
        self._session = None
        self._auth = None
        self._headers = None
        self._url = None
        self.device = device
        self.connection: Optional[AttrDict] = None
        self.api_endpoints: list[str] = None
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def connect(self, **kwargs):
        self.connection = kwargs['connection']
        self._auth = HTTPBasicAuth(kwargs['username'], kwargs['password'])
        self._headers = {
            'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json',
        }
        self._url = f'https://{self.connection.ip.compressed}:{self.connection.port}'

    def get_interface(self, interface_name: str) -> Optional[AttrDict]:
        endpoint = f'/restconf/data/ietf-interfaces:interfaces/interface={interface_name}'
        url = self._url + endpoint
        response = requests.get(url, auth=self._auth, headers=self._headers, verify=False)
        return response.json()

    def get_netconf_capabilities(self):
        netconf = f'/restconf/data/netconf-state/capabilities'
        url = self._url + netconf
        response = requests.get(url, auth=self._auth, headers=self._headers, verify=False)
        self.netconf_capabilities = response.json().get(
            'ietf-netconf-monitoring:capabilities', {}
        ).get('capability', [])

    def get_restconf_capabilities(self):
        restconf = f'/restconf/data/ietf-yang-library:modules-state'
        url = self._url + restconf
        response = requests.get(url, auth=self._auth, headers=self._headers, verify=False)
        self.resconf_capabilities = self.__extract_endpoints(response.json())

    def __extract_endpoints(self, response):
        self.api_endpoints = []
        for key, value in response.get('ietf-yang-library:modules-state', []).items():
            if key != 'module':
                continue
            for endpoint in value:
                self.api_endpoints.append(endpoint.get('schema'))

    def disconnect(self):
        pass

    def execute(self, command, **kwargs):
        pass

    def configure(self, command, **kwargs):
        pass

    def is_connected(self):
        pass
