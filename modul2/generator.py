# generator
import random


def generator1(length):
    for _ in range(length):
        if _ == 3:
            return  # stops execution of function (any type of function)
        yield random.randint(1, 10000)
        print('after yield')


result = generator1(3)
print(result)
result.__next__()
print(next(result))
print(next(result))
print(next(result))

# no more numbers to generate
# print(next(result))

for i in generator1(5):
    print('Generated number: ', i)
