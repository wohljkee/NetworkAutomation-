import os
import subprocess
import unittest

from pyats.topology import loader

from scripts.ping_helper import test_pings

vor: bool = True


class RealPingTests(unittest.TestCase):
    """
    Unit test for verifying ping connectivity from UbuntuServer to all other devices
    defined in the testbed configuration.

    Contributors: Jude Victor
    """

    @classmethod
    def setUpClass(cls):
        """
         testbed and collect all destination IPs.
        """
        testbed_path = os.path.join(os.path.dirname(__file__), "testbed_config.yaml")
        cls.testbed = loader.load(testbed_path)

        cls.device = cls.testbed.devices["UbuntuServer"]
        cls.device_name = cls.device.name
        cls.os = cls.device.os or "linux"

        cls.topology_addresses = []

        print("\nCollected IPs from testbed:")

        for dev in cls.testbed.devices.values():
            if dev.name == cls.device_name:
                continue
            for intf in dev.interfaces.values():
                if hasattr(intf, "ipv4") and intf.ipv4:
                    ip = intf.ipv4.ip.compressed
                    cls.topology_addresses.append(ip)
                    print(f" - {dev.name} -> {intf.name}: {ip}")

    @staticmethod
    def real_execute(command: str, **kwargs) -> str:
        """
        Executes a shell command (ping) and captures its output.
        """
        if not command.strip():
            return ""

        # Enforce Linux-style ping count
        if command.startswith("ping ") and " -c " not in command:
            command = command.replace("ping", "ping -c 4", 1)

        print(f"\n[INFO] Running ping command: {command}")

        try:
            process = subprocess.Popen(
                ["sh", "-c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(timeout=10)
            decoded_stdout = stdout.decode()
            decoded_stderr = stderr.decode()

            print("\n--- Raw Ping Output ---")
            print(decoded_stdout.strip())

            if process.returncode == 0:
                print(f"[PASS] Ping successful for {command.split()[-1]}")
                return decoded_stdout
            else:
                print(f"[FAIL] Ping failed for {command.split()[-1]}")
                print(decoded_stderr.strip())
                return decoded_stdout + decoded_stderr

        except subprocess.TimeoutExpired as e:
            process.kill()
            print(f"[TIMEOUT] Ping to {command.split()[-1]} timed out after 10s")
            return f"TimeoutExpired: {str(e)}"

    def real_read(self) -> str:
        """Placeholder read function to satisfy test_pings interface."""
        return ""

    def test_ping_all_devices(self):
        """Runs real ping tests to all IPs collected from the testbed."""
        result, ping_details = test_pings(
            topology_addresses=self.topology_addresses,
            execute=self.real_execute,
            read=lambda: "",
            device_name=self.device_name,
            os=self.os
        )

        for ip, success in ping_details.items():
            with self.subTest(ip=ip):
                self.assertTrue(success, msg=f"Ping to {ip} failed")

        self.assertTrue(result, msg="One or more devices did not respond to ping")
