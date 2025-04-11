import telnetlib


class TelnetConnector:

    def __init__(self):
        self.conn = None

    def connect(self, *args, **kwargs):
        address = kwargs['address']
        port = kwargs['port']
        self.conn = telnetlib.Telnet(host=address, port=port)

    def do_initial_configuration(self):
        self.conn.execute("")