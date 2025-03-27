import telnetlib
import time


class TelnetContext:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = telnetlib.Telnet(self.host, self.port)
        self.connection.write(b"\n")
        time.sleep(3)
        out = self.connection.read_very_eager()
        if b'(config)' in out:
            self.connection.write(b'exit')
        elif b'config-' in out:
            self.connection.write(b'end')
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()
