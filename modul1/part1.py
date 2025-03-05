# # Integer
# a = 10
# print('Result of 10 + 12 = ', (10).__add__(12))
# print(f"Integer: {a}")
#
# # Float
# b = 10.7
# print(f"Float: {b}")
#
# # Complex
# c = 3 + 6j
# print(f"Complex: {c}")
#
# # addition
# print(f"{type(a + b)}")
#
#
#
#
#
# # String manipulation
# name = "Alice"
# name = 'Alice'
# name = """Alice
# """
# name = '''Alice
# '''
# name = f"Alice\n {a}"
# name = r"Alice\n"
# name = u"Alice\nabc"
#         #012345 678
# print(name[0::2])  # Accessing the first character
# print(name)
# # # String methods
# print(name.upper())  # Uppercase
# print(name.lower())  # Lowercase
# print(name.replace("Al", "Bob"))  # Replace Alice with Bob


# # List (mutable)
# fruits = ["apple", 12, "cherry"]
# print(id(fruits))
# fruits.append("orange")  # Add an item
# print(fruits)
# print(id(fruits))
#
# name = "Alice"
# print(id(name))
# name = name.upper()
# print(id(name))
#
# number1 = 1055555 + 200
# print(id(number1))
# number2 = 1055655 + 100
# print(id(number2))
#
# # Tuple (immutable)
# coordinates = (10, 20)
# print(coordinates)


# # Boolean values
# is_raining = True
# is_sunny = False
# print(is_raining and is_sunny)  # False
# print(is_raining or is_sunny)  # True

# # Sets
# set1 = {1, 2, 2, 3}
# print(set1)
# set1.add(4)
# print(set1)
# set1.add(1)
# print(set1)
# print((5).__hash__())
# print(('1').__hash__())
# # print(('1').__hash__())
#
# print([1,2])
# list1 = [1]
# print(id(list1))
# list1.append(2)
# print(id(list1))
# print(list1.__hash__)

# print(set1.difference({2,3,5}))
# print({2,3,5}.difference(set1))
# print(set1.intersection({2,3,5}))

# # dict
# dict1 = {'key1': '1', 'key2': 2, 'key3': []} #, {1:1}: 3} - non hashable objects cannot be keys
# print(dict1)
# print(dict1.get('key1'))
# print(dict1['key2'])
# print(dict1.get('key4', "not present"))
# # print(dict1['key4']) # will generate exception when key not present
# dict1.update({'new_KEY': set()}) # update method does not return anything (returns None)
# print(dict1)
#
# print('keys resutns', dict1.keys(), 'with type', type(dict1.keys()))
# print(list(dict1.keys())[1])
#
# print('keys resutns', dict1.values(), 'with type', type(dict1.values()))
# print(list(dict1.values())[1])


# x = 8
# if x > 10:
#     print("x is greater than 10")
# elif x == 10:
#     print("x equals 10")
# elif x == 8:
#     print("x equals 8")
# else:
#     print("x is less than 10")

# numbers = [1, 2, 3, 4, 5]
# for number in numbers:
#     print(number, end='\t')

# numbers = [1, 2, 3, 4, 5]
# for number in numbers:
#     if number == 3:
#         numbers.remove(number)
#     print(number, end='\t')
# print(numbers)

# numbers = [1, 2, 3, 4, 5]
# for number in numbers.copy():
#     if number == 3:
#         numbers.remove(number)
#     print(number, end='\t')
# print(numbers)

# letters = 'abcde'
# for letter in letters:
#     if letter == 'c':
#         letters = letters.replace('c', '')
#     print(letter, end='\t')
# print(letters)

# numbers = [1, 2, 3, 4, 5]
# for number in numbers.copy():
#     if number == 3:
#         continue
#     print(number, end='\t')
# print(numbers)

# numbers = [1, 2, 3, 4, 5]
# for number in numbers.copy():
#     if number == 3:
#         break
#     print(number, end='\t')
# print(numbers)

# letters = 'abcde'
# for letter in letters:
#     if letter == 'c':
#         break
#     print(letter, end='\t')
# print(letters)

# numbers = [1, 2, 3, 4, 5]
# for number in numbers.copy():
#     if number == 3:
#         continue
#     print(number, end='\t')
# else:
#     print('done')

# numbers = [1, 2, 4, 5, 3]
# for number in numbers.copy():
#     if number == 3:
#         break
#     print(number, end='\t')
# else:
#     print('did not find number 3')
#

# count = 1
# while count <= 5:
#     password = input('Password: ')
#     print(count)
#     if password == 'my_password':
#         count += 1
#     else:
#         continue
#     print(password)


# 7780 - print login success

# def greet(name, greeting="Hello"):
#     return f"{greeting}, {name}!"
#
# print(greet("Alice"))
# print(greet("Bob", "Hi"))

result = ''
def greet(*args, **kwargs):
    global result
    print(f'all kw args: {kwargs}')
    for name in args:
        result += f"{kwargs['greeting']}, {name}!\n"
    # return result

print('Before:', result)

print(greet("Alice", greeting='Hello',  name='Alice'))
print(greet("Bob", 'Jim', 'Tomas', greeting="Hi"))

print('response from print is: ', print('After:', result))

# numbers = []
# for number in numbers.copy():
#     pass
# print(number)