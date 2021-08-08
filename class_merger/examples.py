from class_merger import Merger


class Soap:
    @staticmethod
    def shave(yak):
        print(f"Washing {yak}!")


class Water:
    @classmethod
    def shave(cls, yak):
        print(f"Rinsing {yak}!")


class Shears:
    def shave(self, yak):
        print(f"Shearing {yak}!")


class YakBarber(Merger, Soap, Water, Shears):
    pass


tenzing = YakBarber()
tenzing.shave("Yakety Sax")

"""
>>> Washing Yakety Sax!
>>> Rinsing Yakety Sax!
>>> Shearing Yakety Sax!
"""


class One:
    def __init__(self, *args, **kwargs):
        self.value = 1
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


class Sum(Merger, One, Two, Three):
    def __init__(self):
        super().__init__(func=lambda x, y: x + y)


class SkipSum(One, Merger, Two, Three):
    def __init__(self):
        super().__init__(func=lambda x, y: x + y)


gauss = Sum()
print(gauss.value)

gauss_but_dumber = SkipSum()
print(gauss_but_dumber.value)

"""
>>> 6
>>> 5
"""
