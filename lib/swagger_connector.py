from typing import Optional

import requests
import urllib3
from bravado.requests_client import RequestsClient
from pyats.datastructures import AttrDict
from pyats.topology import Device


class SwaggerConnector:

    def __init__(self, device: Device, **kwargs):
        self._session = None
        self._auth = None
        self._headers = None
        self._url = None
        self._url_login = None
        self.device = device
        self.connection: Optional[AttrDict] = None
        self.api_endpoints: list[str] = None
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def connect(self, **kwargs):
        self.connection = kwargs['connection']
        self._url = f'https://{self.connection.ip.compressed}:{self.connection.port}'
        self.__login(
            self.connection.credentials.login.username,
            self.connection.credentials.login.password.plaintext
        )
        https_client = RequestsClient()
        https_client.session.verify = False
        https_client.session.headers = self._headers

    def __login(self, username: Optional[str] = None, password: Optional[str] = None):
        endspoint = '/api/fdm/v3/fdm/token'
        requests.post(self._url + endspoint)

    def disconnect(self):
        pass

    def execute(self, command, **kwargs):
        pass

    def configure(self, command, **kwargs):
        pass

    def is_connected(self):
        pass
