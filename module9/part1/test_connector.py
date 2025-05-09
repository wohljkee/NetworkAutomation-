import unittest
from unittest.mock import MagicMock, patch

from pyats.datastructures import AttrDict

device = MagicMock()
class TestConnector(unittest.TestCase):

    def test_connector_create(self):
        from lib.telnet_connector import TelnetConnector
        self.telnet = TelnetConnector(device)

    @patch('telnetlib.Telnet')
    def test_connector_connect(self, get_mock):
        get_mock.return_value = MagicMock() # not mandatory for MagicMock, only for Mock
        connection = MagicMock()
        from lib.telnet_connector import TelnetConnector
        telnet = TelnetConnector(device)
        self.assertRaises(KeyError,telnet.connect)
        self.assertEqual(None, telnet.connect(connection=connection))

    @patch('telnetlib.Telnet')
    def test_connector_enable_rest(self, get_mock):
        get_mock.return_value = MagicMock()
        from lib.telnet_connector import TelnetConnector
        telnet = TelnetConnector(device)
        telnet._conn = MagicMock(write=lambda *args, **kwargs: None)
        self.assertEqual(None, telnet.enable_rest())

    @patch('telnetlib.Telnet')
    def test_connector_execute_rest(self, get_mock):
        get_mock.return_value = MagicMock()
        from lib.telnet_connector import TelnetConnector
        telnet = TelnetConnector(device)
        telnet._conn = MagicMock(write=lambda *args, **kwargs: None)
        # telnet.execute = lambda *args, **kwargs: args, kwargs
        # self.assertMultiLineEqual('first', 'second', telnet.enable_rest())

