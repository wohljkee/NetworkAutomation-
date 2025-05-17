import json
from typing import Optional

import requests
import urllib3
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from pyats.datastructures import AttrDict
from pyats.topology import Device



class SwaggerConnector:

    def __init__(self, device: Device, **kwargs):
        self._session = None
        self._auth = None
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self._url = None
        self._url_login = None
        self.device = device
        self.connection: Optional[AttrDict] = None
        self.api_endpoints: list[str] = None
        self.client: Optional[SwaggerClient] = None
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def connect(self, **kwargs):
        self.connection = kwargs['connection']
        endpoint = '/apispec/ngfw.json'
        self._url = f'https://{self.connection.ip.compressed}:{self.connection.port}'
        self.__login(
            self.connection.credentials.login.username,
            self.connection.credentials.login.password.plaintext
        )
        self._headers.update({'Authorization': f'{self.token_type} {self.access_token}'})
        https_client = RequestsClient()
        https_client.session.verify = False
        https_client.ssl_verify = False
        https_client.session.headers = self._headers
        swagger_client = SwaggerClient.from_url(
            self._url + endpoint,
            http_client=https_client,
            request_headers=self._headers,
            config={'validate_certificate': False, 'validate_responses': False},
        )
        self.client = swagger_client

    def __login(self, username: Optional[str] = None, password: Optional[str] = None):
        endspoint = '/api/fdm/latest/fdm/token'
        response = requests.post(
            self._url + endspoint,
            verify=False,
            data=json.dumps({'username': username, 'password': password, 'grant_type': 'password'}),
            headers=self._headers
        )
        self.access_token = response.json()['access_token']
        self.token_type = response.json()['token_type']
        self.refresh_token = response.json()['refresh_token']


    def disconnect(self):
        pass

    def execute(self, command, **kwargs):
        pass

    def configure(self, command, **kwargs):
        pass

    def is_connected(self):
        pass
