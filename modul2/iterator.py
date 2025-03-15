# iterator

list1 = [1,2,3]
iterator = list1.__iter__()
print(type(iterator))
print(iterator.__next__())
print(iterator.__next__())
print(iterator.__next__())

# no more objects
# print(iterator.__next__())

class AnimalIterator:
    def __init__(self, animal):
        self.animal = animal
        print(self.animal)

    def __next__(self):
        if not self.animal:
            raise StopIteration
        return self.animal.pop(0)

class Animals:
    def __init__(self, animals):
        self.animals = animals

    def __iter__(self):
        return AnimalIterator(self.animals)


animals = Animals(['dog', 'cat', 'bat'])
for animal in animals:
    print(animal)