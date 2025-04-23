from typing import Optional

from pyats.datastructures import AttrDict
from pyats.topology import Device


class RESTConnector:

    def __init__(self, device: Device, **kwargs):
        self._session = None
        self.device = device
        self.connection: Optional[AttrDict] = None

    def connect(self, **kwargs):
        self.connection = kwargs['connection']
        pass

    def disconnect(self):
        pass

    def execute(self, command, **kwargs):
        pass

    def configure(self, command, **kwargs):
        pass

    def is_connected(self):
        pass
