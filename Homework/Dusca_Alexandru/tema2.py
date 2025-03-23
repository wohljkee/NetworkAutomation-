import random

"""
Example of switchport configuration:
device{
    'model': Cisco,
    'serial': 
    'name': SW1,
    'vlan': 1952,
    'duplex': full-duplex,
    'speed': 10Gbps,
    'state': active
}
"""

# Task 3:(extra) - return port objects on iteration (new class for port objects nees to be defined)
class Port:
    def __init__(self, name: str, vlan: int, duplex: str, speed: str, state: str):
        self.name = name
        self.vlan = vlan
        self.duplex = duplex
        self.speed = speed
        self.state = state

    def __repr__(self):
        return f"Port {self.name}, VLAN={self.vlan}, Duplex={self.duplex}, Speed={self.speed}, State={self.state}"

    def to_dict(self):
        return {
            "name": self.name,
            "vlan": self.vlan,
            "duplex": self.duplex,
            "speed": self.speed,
            "state": self.state
        }


class Switch:
    def __init__(self, model, serial):
        self.model = model
        self.serial = serial
        self.ports = {}

    # method which allows for adding information about switch port (min: name, vlan, duplex, speed, state)
    def add_switch_port(self, name: str, vlan: int, duplex: str, speed: str, state: str):
        try:
            if name in self.ports:
                raise ValueError(f"Port {name} already exists!")

            self.ports[name] = Port(name, vlan, duplex, speed, state)  # use of class Port
            print(f"Port {name} added to {self.serial}.")
        except Exception as e:
            print(f"Error adding port: {e}")

    # method to remove ports from the object based on 'name' attribute
    def remove_switch_port(self, name: str):
        try:
            if name not in self.ports:
                raise KeyError(f'Port {name} does not exist')
            del self.ports[name]  # just delete the port[name]
            print(f'Port {name} was just removed.')
        except KeyError as e:  # catch the KeyError exception when trying to remove the wrong name
            print(f'Error removing port {name}: {e}')
        except Exception as e:
            print(f'Unexpected error catched: {e}')

    # method to update any switch port data (update = add more data to the switch - using **kwargs)
    def update_switch_port(self, name: str, **kwargs):
        try:
            if name not in self.ports:
                raise KeyError(f'Port {name} does not exist!')
            for key, value in kwargs.items():
                if hasattr(self.ports[name], key):
                    setattr(self.ports[name], key, value)
            print(f"Port {name} updated.")
        except KeyError as e:
            print(f'Error updating port {name}: {e}')
        except Exception as e:
            print(f'Unexpected error catched: {e}')

    # Add conversion to string and representation of the switch object:
    # then converted to string format should be 'serial:number_of_prts'
    def __str__(self):
        return f"{self.serial}: {len(self.ports)}"

    # when represented inside another object format should be 'model:serial'
    def __repr__(self):
        return f"{self.model}:{self.serial}"

    # Make the switch object iterable:
    def __iter__(self):
        return iter(self.ports.values())


if __name__ == "__main__":
    """
    Execution:
    call the above generator with argument of 100
    in for loop iterated over the generated switches and list only switches that:
    - have more than 28 ports
    - have ports in vlan 200
    - and speed is 1000+"
    """

    def generator_switches(num: int):
        models = ["Cisco Catalyst 9300", "Cisco Nexus 5000", "Cisco Catalyst 9400", "Juniper EX4300"]
        for _ in range(num):
            model = random.choice(models)  # random model
            serial = f"SN{random.randint(10000, 95000)}"
            switch_val = Switch(model=model, serial=serial)  # call the Switch class
            num_ports = random.choice(range(8, 65, 4))

            for i in range(1, num_ports + 1):
                vlan = random.choice([10, 20, 30, 50, 100, 200, 250, 300])
                duplex = random.choice(['full', 'half'])
                speed = random.choice(['100', '1000', '10000'])
                state = random.choice(['up', 'down', 'admin-down'])
                name = f'Gig{(i // 10) + 1}/{i % 10}'  # for gig1/0 -  gig 1/9 -> then reset and move to gig2/0-...
                switch_val.add_switch_port(name, vlan, duplex, speed, state)  # call the add_switch_port() method

            yield switch_val

    # Execute the generator
    for switch in generator_switches(100):
        if len(switch.ports) > 28 and any(
                isinstance(p, Port) and p.vlan == 200 and int(p.speed) > 1000 for p in switch):
            print(switch)