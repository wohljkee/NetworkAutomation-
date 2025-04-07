# import os
# import time
# from multiprocessing import Pool
# import telnetlib
#
# def my_print(port):
#     with open(f'{os.getpid()}{port}.txt', 'w') as f:
#         f.write("Hello World, {}".format(port))
#     c = telnetlib.Telnet('192.168.0.100', port=port)
#     c.write(b'\n')
#     return 'Process {}'.format(os.getpid()), c
#
#
# if __name__ == '__main__':
#     with Pool(5) as pool:
#         result = pool.map(my_print, [5024, 5036, 5027, 5044, 5035,])
#         print(result)
#     time.sleep(10)
#     for i in result:
#         i[1].write(b'\n')

import os
import time
from multiprocessing import Process, Queue
import telnetlib

def my_print(port, queue):
    with open(f'{os.getpid()}{port}.txt', 'w') as f:
        f.write("Hello World, {}".format(port))
    c = telnetlib.Telnet('192.168.0.100', port=port)
    c.write(b'\n')
    time.sleep(3)
    out = c.read_very_eager()
    queue.put((out, port))
    return 'Process {}'.format(os.getpid()), c


if __name__ == '__main__':
    q = Queue()
    processes = []
    for _ in [5024, 5036, 5027, 5044, 5035]:
        proc = Process(target=my_print, args=(_,q))
        proc.start()
        processes.append(proc)
    for p  in processes:
        p.join()

    while not q.empty():
        print(q.get())

