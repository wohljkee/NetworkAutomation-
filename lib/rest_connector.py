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
        self.device = device
        self.connection: Optional[AttrDict] = None
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
        endpoint=f'/restconf/data/ietf-interfaces:interfaces/interface={interface_name}'
        url=self._url+endpoint
        response = requests.get(url, auth=self._auth, headers=self._headers, verify=False)
        return response.json()

    def disconnect(self):
        pass

    def execute(self, command, **kwargs):
        pass

    def configure(self, command, **kwargs):
        pass

    def is_connected(self):
        pass
