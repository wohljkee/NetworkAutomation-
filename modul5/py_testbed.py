from pyats.topology import loader
# import yaml
#
#
# with open('testbed_example.yaml', 'r') as f:
#     out = yaml.load(f, Loader=yaml.SafeLoader)
#
# print(out)

tb = loader.load('testbed_example.yaml')
dev = tb.devices['IOU1']
conn = dev.connections.ssh
print(conn)

print(conn)