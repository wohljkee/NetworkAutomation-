# Create a switch object

1) Create a class for a switch object that will implement the following methods:
    - __init__ - requires minimal "model" argument and "serial"
    - add_switch_port() - allows for adding information about switch port (min: name, vlan, duplex, speed, state)
    - remove_switch_port() - can remove ports from the object based on 'name'
    - update_switch_port() - can update any switch port data

2) Add conversion to string and representation of the switch object:
    - when converted to string format should be 'serial:number_of_prts'
    - when represented inside another object format should be 'model:serial'

3) Make the switch object iterable:
    - each iteration will return a dictionary containing port information until all ports are consumed
    - (extra) - return port objects on iteration (new class for port objects nees to be defined)

4) Create generator for random switch:
    - generator will produce the number of switches provided as argument ex: generator_switches(5) will return generator
      that can generate 5 switch objects with random data
    - generator will add random number of ports (between: 8-64 with step of 4 ) using the add_switch_port() method

5) Execution:
    - call the above generator with argument of 100
    - in for loop iterated over the generated switches and list only switches that:
        - have more than 28 ports
        - have ports in vlan 200
        - and speed is 1000+