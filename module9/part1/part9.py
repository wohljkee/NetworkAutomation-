import pylint
import os
from multiprocessing import Process

# args = ['--disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods', 'modul7/part2/configre_ospf.py']
# pylint.run_pylint(args)

dir = os.getcwd()
print(dir)
scan_list = []

# option 1 - running on directory with same-structure
# pylint.run_pylint([dir])

# option2 - run for each file in folder structure
# for root, _, files in os.walk(dir):
#     for file in files:
#         result = os.path.join(root, file)
#         if result.endswith('.py'):
#             scan_list.append(result)
#
# if __name__ == '__main__':
#     process_list = []
#     for file in scan_list:
#         p = Process(target=pylint.run_pylint, args=([file],))
#         p.start()
#         process_list.append(p)
#     for p in process_list:
#         p.join()

# option 3 - run with pylint_rc file
# pylint will check dir for RC file or use provided path
args = ['--rcfile=pylintrc', 'modul7/part2/configre_ospf.py']
pylint.run_pylint(args)