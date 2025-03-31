import telnetlib
from time import sleep

class TelnetContext:
    def __init__(self, address: str, port: int, hostname: bytes):
        self.address = address
        self.port = port
        self.connection = None
        self.hostname = hostname

    def __enter__(self):
        self.connection = telnetlib.Telnet(self.address, self.port)
        self.connection.write(b"\n")
        sleep(1)
        out = self.connection.read_very_eager()
        # print(out.decode())
        if b'(config)' in out or b'(config-' in out:
            self.connection.write(b"end\n")
        elif b'Password' in out:
            self.connection.write(b"pass\n")
        return self

    def write(self, command: bytes):
        self.connection.write(command + b"\n")

    def expect(self, regex: list[bytes]):
        self.connection.expect([self.hostname + regex[0]])
    def read_very_eager(self):
        return self.connection.read_very_eager()
    def __exit__(self, type, value, traceback):
        self.connection.close()
