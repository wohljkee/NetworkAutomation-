from netmiko import ConnectHandler

connection_data = {
    'device_type': 'cisco_ios',
    'host': '192.168.102.2',
    'username': 'admin',
    'password': 'password',
    'secret': 'Cisco!12'
}
connection = ConnectHandler(**connection_data)
print(type(connection))
connection.enable()  # basically does the transition to enable prompt #
output = connection.send_command('show version')
print(output)
