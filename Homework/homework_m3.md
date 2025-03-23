# Create a class to retrieve system information

Create class named SystemUtils that will have methods for getting the following info 
- get_ipv4_interfaces() - returns list of dict with interface name/IP/subnet/MAC
- get_ipv4_routes() - returns list of dict with routeing information destination/gateway/interface/
- get_ipv6_interfaces() - returns list of dict with interface name/IP/subnet/MAC
- get_ipv6_routes() - returns list of dict with routeing information destination/gateway/interface/
- get_listening_ports() - create table like format that can be later printed with tabulate and should contain all the 
columns (and data) in the output of command netstat -ln

Import and use ipaddress module to  return all data as ip_address objects  

```python
# example
import ipaddress
ipaddress.ip_address('192.168.0.1')
ipaddress.ip_interface('8001::5/64')
```

IP commands are available on the ubuntu containers but if you want to use 'ifconfig' or other tools use:
```shell
sudo apt install net-tools
```

To get listening ports you can use the netstat command as in the example below
Ignore established connection only capture servers listening 
```shell
osboxes@osboxes:~$ netstat -ln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.54:53           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
udp        0      0 127.0.0.54:53           0.0.0.0:*
udp        0      0 127.0.0.53:53           0.0.0.0:*
udp        0      0 192.168.1.18:68         0.0.0.0:*
raw6       0      0 :::58                   :::*                    7
```
for displaying table object you can use the tabulate module that can be installed from packages or using 'pip install tabulate'
```python
from tabulate import tabulate
table = [["tcp",'127.0.0.53:53','0.0.0.0:*'],["tcp6",':::22',':::*'],["raw6",':::58',':::*']]
print(tabulate(table, headers=['Proto', 'Local Address', 'Foreign Address']))
```
