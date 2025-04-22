import os
import time
from threading import Thread, Lock
import telnetlib

queue = []
lock = Lock()


def my_print(port):
    with open(f'{os.getpid()}{port}.txt', 'w') as f:
        f.write("Hello World, {}".format(port))
    c = telnetlib.Telnet('192.168.0.100', port=port)
    c.write(b'\n')
    time.sleep(3)
    out = c.read_very_eager()
    lock.acquire(timeout=10)
    if port == 5024:
        raise Exception('port 5024')
    print(out)
    lock.release()
    c.close()
    return 'Process {}'.format(os.getpid()), c


thds = []
for _ in [5024, 5036, 5027, 5044, 5035]:
    proc = Thread(target=my_print, args=(_,))
    proc.start()
    thds.append(proc)
for p in thds:
    p.join()

for item in queue:
    print(item)
