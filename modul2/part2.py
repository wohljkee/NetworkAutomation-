import subprocess
import re

# output = subprocess.call('dir', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# print(output)


# result = subprocess.Popen(['dir'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# result = result.communicate()
# # output = result.stdout.read()
#
# print(result)

result = subprocess.Popen(['ping', '8.8.8.8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = result.communicate()
print(result)

pattern = r'(\d+)% loss'
found_output = re.search(pattern, str(result[0]))
print(type(found_output))
print(found_output.group(0))
