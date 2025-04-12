# Use connection classes and testbed

1) Based on the code in '[telnet_connector.py](../modul5/part2/telnet_connector.py)' add support for
   configuring CSR router with initial configuration by adding elif branch to the below code:

   ```python
   def do_initial_configuration(self):
       if self.device.os == 'ios':
           ...
   ```

2) Create tests to do the initial configuration of both routers
3) Recreate structure and add your custom methods to the 'SSHConnector'
4) Add test to check that ssh connections are working and custom methods can be called
5) Recreate the diagram in "untitled" project and try to create testbed for the full configuration 