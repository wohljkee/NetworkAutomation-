# ping_helper.py

import logging
import time
from typing import Callable, Tuple
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
"""
Contributors: Jude Victor
"""

def test_pings(
    topology_addresses: list[str],
    execute: Callable[..., str],
    read: Callable[[], str],
    device_name: str,
    os: str
    ) -> Tuple[bool, dict[str, bool]]:
    """Testing connectivity with ping command from a device to a list of IP addresses from testbed"""
    ping_results: dict[str, bool] = {}
    pattern = r'(?:Success rate is (\d{1,3}) percent)|(?:(\d{1,3})\% packet loss)'

    if os != 'ubuntu':
        execute('\r', prompt=[r'\w+#'])

    for addr in topology_addresses:
        ping_command = f'ping {addr}' if os != 'ubuntu' else f'ping -c 4 {addr}'
        print(f"\n--- Running ping command: {ping_command} ---")
        out = execute(ping_command, prompt=[])
        matched_regex = False
        percentage = 0

        for i in range(4):
            time.sleep(1)
            out += read() if i != 0 else ""
            print(f"\n--- Ping Output Round {i + 1} ---\n{out}\n")

            match = re.search(pattern, out)
            if match:
                matched_regex = True
                percentage = int(match.group(1)) if match.group(1) is not None else 100 - int(match.group(2))
                break

        if not matched_regex:
            logger.error(out)
            percentage = 0

        if percentage == 0:
            ping_results[addr] = False
            logger.warning('Ping from %s to %s failed\n', device_name, addr)
        else:
            ping_results[addr] = True
            logger.info('Ping from %s to %s succeeded\n', device_name, addr)

    return all(ping_results.values()), ping_results