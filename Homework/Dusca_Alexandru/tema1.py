# Create and call python function that will collect vlan information for each port of a switch and return a dictionary as in the example below:

import pprint

def view_vlan_info():
    vlan_data = {}

    while (switch_name := input("Enter switch name [or press 'q' to quit]: ").strip().lower()) != 'q':
        vlan_data.setdefault(switch_name, {})

        while (port_name := input(f"Enter port for {switch_name} [or press 'q' to quit]: ").strip().lower()) != 'q':
            vlan_data[switch_name].setdefault(port_name, {"vlans": set()})

            while (vlan_input := input(f"Enter VLANs for {switch_name} {port_name} "
                                       f"[or press 'q' to stop]: ").strip().lower()) != 'q':
                try:
                    vlans = set(map(int, vlan_input.split(','))) # set used to add VLANs
                    vlan_data[switch_name][port_name]["vlans"].update(vlans)
                except Exception as e:
                    print(f"Invalid input. Please enter VLANs as numbers separated by commas. Exception raised: {e}")

            vlan_data[switch_name][port_name]["vlans"] = sorted(vlan_data[switch_name][port_name]["vlans"])

    return vlan_data

# Calling the function view_vlan_info()
vlan_info = view_vlan_info()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(vlan_info)
