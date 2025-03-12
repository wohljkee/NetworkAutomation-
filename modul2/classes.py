# Classes

class Car(object):
    def __init__(self, model, year):
        print('object at memory location: ', id(self))
        self.model = model
        self.year = year

    def print_car_info(self):
        print('car model: ', self.model)
        print('car year: ', self.year)

    def __str__(self):
        return f'{self.model} - {self.year}'

    def __repr__(self):
        return f'{self.model}:{self.year}'

    def __add__(self, other):
        return Car(self.model + other.model, self.year + other.year)


car1 = Car('subaru', 2011)
print(car1.model)
print(id(car1))
car1.print_car_info()

# dict method
print(car1.__dir__())
print(dir(car1))

# str method
print('Printing car1 object', str(car1), car1.__str__())
car2 = Car('Logan', 2013)
print('Printing car2 object', car2)

# repr method
print('All cals list:', [car1, car2])

# add method

car3 = car1 + car2
car3.print_car_info()

# def func1():
#     print('func1')
#
# func1.new_attr = 10
# print(func1.new_attr)
#
# def func2(func1):
#     print('func2')
#     print(func1.new_attr)
#
#
# func1.func2 = func2
# func1.func2(func1)
