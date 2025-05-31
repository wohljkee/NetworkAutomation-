import unittest
from scripts.ping_helper import test_pings


class TestPingHelper(unittest.TestCase):
    """
    Unit tests for the ping_helper.test_pings function.

    Contributors: Jude Victor
    """

    def setUp(self):
        self.device_name = "IOU1"
        self.os = "ios"
        self.addresses = ["192.168.101.2", "192.168.102.2", "192.168.11.2"]

    def test_all_success(self):
        """All ping targets respond successfully (IOS format)."""
        def fake_execute(cmd, **kwargs):
            return "Success rate is 100 percent (5/5)"

        def fake_read():
            return ""

        result, details = test_pings(
            topology_addresses=self.addresses,
            execute=fake_execute,
            read=fake_read,
            device_name=self.device_name,
            os=self.os
        )

        self.assertTrue(result, "Expected all pings to succeed.")
        self.assertTrue(all(details.values()), "Expected all detail entries to be True.")

    def test_some_fail(self):
        """One ping fails out of three."""
        def fake_execute(cmd, **kwargs):
            if "192.168.102.2" in cmd:
                return "Success rate is 0 percent (0/5)"
            return "Success rate is 100 percent (5/5)"

        def fake_read():
            return ""

        result, details = test_pings(
            topology_addresses=self.addresses,
            execute=fake_execute,
            read=fake_read,
            device_name=self.device_name,
            os=self.os
        )

        self.assertFalse(result, "Expected overall result to be False due to failure.")
        self.assertTrue(details["192.168.101.2"], "Expected 192.168.101.2 to pass.")
        self.assertFalse(details["192.168.102.2"], "Expected 192.168.102.2 to fail.")
        self.assertTrue(details["192.168.11.2"], "Expected 192.168.11.2 to pass.")

    def test_ubuntu_style(self):
        """Simulate Ubuntu-style ping output (packet loss logic)."""
        self.os = "ubuntu"
        addresses = ["8.8.8.8"]

        def fake_execute(cmd, **kwargs):
            return "4 packets transmitted, 4 received, 0% packet loss"

        def fake_read():
            return ""

        result, details = test_pings(
            topology_addresses=addresses,
            execute=fake_execute,
            read=fake_read,
            device_name="UbuntuServer",
            os=self.os
        )

        self.assertTrue(result, "Expected ping to 8.8.8.8 to succeed.")
        self.assertTrue(details["8.8.8.8"], "Expected 8.8.8.8 to be marked as reachable.")


if __name__ == '__main__':
    unittest.main()