import telnetlib


class TelnetContext:
    def __init__(self, address: str, port: int, hostname: bytes):
        self.address = address
        self.port = port
        self.connection = None
        self.hostname = hostname

    def __enter__(self):
        self.connection = telnetlib.Telnet(self.address, self.port)
        self.connection.write(b"\n")
        out = self.connection.read_very_eager()
        # print(out.decode())
        if b'(config)' in out or b'(config-' in out:
            self.connection.write(b"end\n")
        return self

    def write(self, command: bytes):
        self.connection.write(command + b"\n")

    def expect(self, regex: list[bytes]):
        self.connection.expect([self.hostname + regex[0]])

    def __exit__(self, type, value, traceback):
        self.connection.close()
