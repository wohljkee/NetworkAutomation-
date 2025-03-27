from modul3.part2.telnet_context import TelnetContext

remote_address = '92.83.42.103'
port = 5017
with TelnetContext(remote_address, port, b"IOU1") as te:
    te.write(b'conf t')
    te.write(b"int eth0/0")
    te.expect([b"\(config-if\)#"])
    te.write(b"ip add 192.168.11.1 255.255.255.0")
    te.expect([b"\(config-if\)#"])
    te.write(b"no sh")
    te.expect([b"\(config-if\)#"])
    te.write(b"line vty 0 4")
    te.expect([b"\(config-line\)#"])
    te.write(b"transport input telnet")
    te.expect([b"\(config-line\)#"])
    te.write(b"password password")
    te.expect([b"\(config-line\)#"])
    te.write(b"privilege level 15")
    te.expect([b"\(config-line\)#"])
    te.write(b"exit")
    te.expect([b"\(config\)#"])
    te.write(b"exit")
    te.expect([b"#"])
    te.write(b"wr")
    te.expect([b"\[confirm\]|#"])
