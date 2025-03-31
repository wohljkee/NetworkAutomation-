from subprocess import PIPE, Popen
from ipaddress import ip_address

subnet_mask = '24'
network_address = ip_address('192.168.11.0')
pc_address = ip_address('192.168.11.254')
router_address = ip_address('192.168.11.1')

set_ip_command = f'sudo ip address add {pc_address}/{subnet_mask} dev ens4'.split(' ')
remove_ip_command = f'sudo ip remove address {pc_address}/{subnet_mask} dev ens4'.split(' ')
add_route_command = f'ip route add {network_address}/{subnet_mask} via {router_address}'.split(' ')
set_int_on_command = 'ip link set dev ens4 up'.split(' ')

set_ip = Popen(set_ip_command, stdout=PIPE, stderr=PIPE)
print(set_ip.communicate())

set_interf_on = Popen(set_int_on_command, stdout=PIPE, stderr=PIPE)
print(set_interf_on.communicate())

set_route = Popen(set_int_on_command, stdout=PIPE, stderr=PIPE)
print(set_route.communicate())