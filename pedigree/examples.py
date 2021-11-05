from __init__ import *


class Soap:
    def shave(self, yak):
        print(f"Washing {yak}!")


class Water:
    def shave(self, yak):
        print(f"Rinsing {yak}!")


class Shears:
    def shave(self, yak):
        print(f"Shearing {yak}!")


class YakBarber(Soap, Water, Shears, metaclass=Pedigree):
    pass


tenzing = YakBarber()
tenzing.shave("Yakety Sax")

"""
>>> Washing Yakety Sax!
>>> Rinsing Yakety Sax!
>>> Shearing Yakety Sax!
"""


class One:
    value = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Two:
    value = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Three:
    value = 3

    def __init__(self, *args, **kwargs):
        self.value = 4
        super().__init__(*args, **kwargs)


add = lambda x, y: x + y


class Sum(One, Two, Three, metaclass=Pedigree, func=add):
    pass


class SkipSum(One, Two, Three, metaclass=Pedigree, func=add, ignores=(Three,)):
    pass


gauss = Sum()
print()
print(gauss.value)

gauss_but_dumber = SkipSum()
print(gauss_but_dumber.value)


"""
>>> 6
>>> 4
"""


class First:
    def first(self):
        print("I will run first")

    @force_last
    def last(self):
        print("I will definitely run last")


class Last:
    @force(order=0)
    def first(self):
        print("I will definitely run first")

    def last(self):
        print("I will run last")


class Runner(First, Last, metaclass=Pedigree):
    pass


kipchoge = Runner()
print()
kipchoge.first()
kipchoge.last()


"""
>>> I will definitely run first
>>> I will run first
>>> I will run last
>>> I will definitely run last
"""


joiner = lambda father, mother: f"Child of {Father.name} and {Mother.name}"


class Person:
    name = "John Doe"

    def say_hello(self) -> str:
        return f"Hello! I'm {self.name}!"


class Father(Person):
    name = "Donald"


class Mother(Person):
    name = "Grace"


class Child(Mother, Father, metaclass=Pedigree, func=joiner):
    pass


def greeter(person: Person) -> str:
    return person.say_hello()


guido = Child()
print()
print(greeter(guido))


"""
>>> Child of Donald and Grace
"""


class Value:
    baz = 420


class Method:
    def baz(self, arg):
        return arg


class Mixed(Value, Method, metaclass=Pedigree, func=add):
    pass


two_face = Mixed()
print()
print(two_face.baz(69))


"""
>>> 489
"""