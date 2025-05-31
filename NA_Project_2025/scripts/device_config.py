from typing import Any

"""
Contributors: Jude Victor, Carina Furmanek
"""

def set_device_hostname(device: Any, hostname: str) -> bool:
    """Sets the hostname on the given device."""
    if not hostname or not isinstance(hostname, str):
        print("Error: Hostname must be a non-empty string.")
        return False

    print(f"Attempting to set hostname to '{hostname}' on device '{device.name}'...")
    try:
        device.configure(f"hostname {hostname}")
        print(f"Hostname configuration command sent for {device.name}.")
        return True
    except Exception as e:
        print(f"Error sending hostname configuration to {device.name}: {e}")
        return False


def get_device_prompt(device: Any) -> str | None:
    """Retrieves the current prompt of the device."""
    try:
        return device.prompt
    except Exception as e:
        print(f"Error retrieving prompt for {device.name}: {e}")
        return None