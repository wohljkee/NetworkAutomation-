import time
from modul3.part2.telnet_context import TelnetContext

with TelnetContext(address="192.168.11.1", hostname=b"IOU1", port=23) as t:
    with open("test.txt", "wb") as file:
        out = b''
        t.write(b"show running-config")
        while True:
            time.sleep(2)
            var1 = t.read_very_eager()  # type: bytes
            out += b'\n'.join([line for line in var1.splitlines() if b"--More--" not in line and b'IOU1#' not in line])
            if b'\nIOU1#' in out:
                break
            else:
                t.write(b"")
        file.write(out)
