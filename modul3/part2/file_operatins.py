# file operations

# file = open('text.txt', 'r')
# output = file.read()
# print(output)
#
# file = open('text.txt', 'w')
# file.write('\nNew Hello Python\n')
# file.flush()
# file.close()
#
# file = open('text.txt', 'r')
# output = file.read()
# print(output)

with open('text.txt', 'w') as file:
    file.write('\nSecond Hello Python\n')

with open('text.txt', 'r') as file:
    print(file.read())