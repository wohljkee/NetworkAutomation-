from pyats.topology import loader
tb = loader.load('testbed_example.yaml')
mgmt_int = tb.devices['FTD'].interfaces['mgmt'].link
conn_dev = mgmt_int.connected_devices
for dev in conn_dev:
    if dev == tb.devices['FTD']:
        continue
    for interface in dev.interfaces.values():
        int_found = interface if interface.link == mgmt_int else None
        if int_found:
            break
print(int_found.ipv4.ip.compressed)