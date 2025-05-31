import unittest
from unittest.mock import MagicMock

from scripts.device_config import set_device_hostname, get_device_prompt

class TestDeviceConfig(unittest.TestCase):
    """
    Contributors: Jude Victor, Carina Furmanek
    """
    def setUp(self):
        self.mock_device = MagicMock()
        self.mock_device.name="TestMagicMock"

    def test_set_hostname_with_mock(self):
        target_hostname="Mockk"
        result=set_device_hostname(self.mock_device, target_hostname)
        self.assertTrue(result)
        self.mock_device.configure.assert_called_once_with(f"hostname {target_hostname}")

if __name__ == '__main__':
    unittest.main()