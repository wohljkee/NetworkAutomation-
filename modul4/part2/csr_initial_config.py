import time

import telnetlib3
import asyncio

address = '192.168.0.100'
port = 5025


async def configure_csr_device(address: str, port: int, user: str, password: str, hostname: str):
    connection = await telnetlib3.open_connection(address, port)
    t_reader, t_writer = connection
    t_writer.write("\n")
    response = await t_reader.readuntil(b"[yes/no]:")
    print(type(connection))
    print(connection)
    print(response)

    if b'initial configuration dialog? [yes/no]' in response:
        t_writer.write('yes\n')
        await t_reader.readuntil(b"management setup? [yes/no]:")
        t_writer.write('yes\n')
        await t_reader.readuntil(b"host name [Router]:")
        t_writer.write(f'{hostname}\n')
        await t_reader.readuntil(b"Enter enable secret:")
        t_writer.write(f'{password}\n')
        await t_reader.readuntil(b"Enter enable password:")
        t_writer.write(f'{password}\n')
        await t_reader.readuntil(b"Enter virtual terminal password:")
        t_writer.write(f'{password}\n')
        await t_reader.readuntil(b"SNMP Network Management? [yes]:")
        t_writer.write('no\n')
        await t_reader.readuntil(b"interface summary:")
        t_writer.write('GigabitEthernet1\n')
        await t_reader.readuntil(b"IP on this interface? [yes]:")
        t_writer.write('yes\n')
        await t_reader.readuntil(b"IP address for this interface:")
        t_writer.write('192.168.102.2\n')
        await t_reader.readuntil(b"mask for this interface [255.255.255.0] :")
        t_writer.write('255.255.255.0\n')
        await t_reader.readuntil(b"Enter your selection [2]:")
        t_writer.write('2\n')

        for _ in range(10):
            time.sleep(60)
            t_writer.write('\n')
            await t_reader.readuntil(hostname.encode())
    elif b'Router>' in response:
        print('Router is configured')



asyncio.run(configure_csr_device(address, port, user='admin', password='Cisco!12', hostname='Router'))
