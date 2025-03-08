# Reading user input for switch config


Create and call python function that will collect vlan information
for each port of a switch and return a dictionary as in the example below:
```python
{
    'SW1': {
        'Ethernet1/1': {'vlans': [100, 200, 300]},
        'Ethernet1/2': {'vlans': [100, 500, 20]},
    },
    'SW2': {
        'Ethernet1/1': {'vlans': [10, 20, 30]},
        'Ethernet1/4': {'vlans': [11, 12, 13]},
    }
}
```
## Steps:
 - ask user for switch name
 - ask user for switch port 
 - ask user for vlans corresponding to above port
   - user will provide vlans as "100,200,300"
   - user will be asked to add more vlans or press q
 - if no more vlans are provided user will be asked to provide additional port or press 'q'
 - if no more ports are provided user will be asked ro provide additional switch or press 'q'

## Checks:
 - make sure that vlans do not repeat for port - hint: set()
 - check if user provides same port name a second time
 - check if user provides same switch name a second time  