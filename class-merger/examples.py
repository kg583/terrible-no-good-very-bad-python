import class_merger import Merger





tenzing = YakBarber()
tenzing.shave("Yakety Sax")

"""
>>> Washing Yakety Sax!
>>> Rinsing Yakety Sax!
>>> Shearing Yakety Sax!
"""


class One:
    def __init__(self):
        self.value = 1
        super().__init__()
    
    
class Two:
    value = 2
    def __init__(self):
        super().__init__()
    
    
class Three:
    value = 3
    def __init__(self):
        self.value = 4
        super().__init__()
    
    
class Sum(Merger, One, Two, Three):
    def __init__(self):
        super().__init__(func=lambda x, y: x + y)
        
        
class SkipSum(One, Merger, Two, Three):
    def __init__(self):
        Merger.__init__(self, func=lambda x, y: x + y)
        
        
gauss = Sum()
print(gauss.value)

gauss_but_dumber = SkipSum()
print(gauss_but_dumber.value)

"""
>>> 6
>>> 5
"""
