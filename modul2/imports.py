# imports

# import time
# import modul2.to_import
import modul2.to_import as ti
print(ti.time)
# from modul2.to_import import variable_to_import
from modul2.to_import import time
print(time)
from modul2.to_import import *
print(datetime)
from modul2.to_import import variable_to_import as va
import modul2.package_to_import as pi
print(pi.package_variable)
print(pi.package_module_function())

print(va)
# modul2.to_import.import_test_function()
print(ti.import_test_function())