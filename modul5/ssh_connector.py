class SSHConnector:

    def __init__(self):
        self.username = None
        self.password = None

    def connect(self, *args, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']

    def get_device_details(self, *args, **kwargs):
        pass

    def do_initial_configuration(self):
        pass

