# Classes

## Decorators

```py
@ordered
class Foo:
    pass

# becomes

from functools import total_ordering
@total_ordering
class Foo:
    pass
```

```py
@meta(baz=baz, *args)
class Foo(Bar):
    pass

# becomes

class Foo(Bar, metaclass=meta, baz=baz, *args):
    pass
```

## Operators

```py
class Foo:
    op [self + other]:
        pass
        
    op [self * other]:
        pass
        
    op [self | other]:
        pass

# becomes

class Foo:
    def __add__(self, other):
        pass
        
    def __mul__(self, other):
        pass
        
    def __or__(self, other):
        pass
```

```py
class Foo:
    op self.other:
        pass
        
    op self[other]:
        pass
        
    op cls[other]:
        pass

# becomes

class Foo:
    def __getattr__(self, other):
        pass
        
    def __getitem__(self, other):
        pass
        
    def __class_getitem__(cls, other):
        pass
```

```py
class Foo:
    meth len(self):
        pass
        
    meth self(bar):
        pass
        
    meth init(bar):
        pass

# becomes

class Foo:
    def __len__(self):
        pass
        
    def __call__(self, bar):
        pass
        
    def __init__(self, bar):
        pass
```

# Functions

# Binding

```py
func foo(bar):
meth foo(bar):

# become

def foo(bar):
def foo(self, bar):
```

```py
class Baz:
    proc foo(bar):

# becomes

class Baz:
    @classmethod
    def foo(cls, bar):
```

```py
class Baz:
    static foo(bar):

# becomes

class Baz:
    @staticmethod
    def foo(bar):
```

## Chaining

```py
a => b => c
*a => **b => c
[a1 => b1, a2 => b2] => c

# become

c(b(a))
c(**b(*a))
c((b1(a1), b2(a2))
```

## Lambdas

```py
bar = foo(_, 1, 2)
baz = foo(*_, 4, **_)
qux = foo(a, b, b, a)
quy = foo(*c, _, *c)

# become

bar = lambda _: foo(_, 1, 2)
baz = lambda *_0, **_1: foo(*_0, 4, **_1)
qux = lambda a, b: foo(a, b, b, a)
quy = lambda c, _: foo(*c, _, *c)
```

# Syntax

## Constants

```py
static PI = 3.14
PI = 7

# becomes

class _static:
    def __init__(self):
        self.__PI = 3.14
        
    @property
    def PI(self):
        return self.__PI
        
_static.PI = 7
```

## Soft Keywords

```py
# require identifiers directly after
async
class
def
del
func
global
import
meth
nonlocal
op
proc
static
```

# Typing

## Annotations

```py
func foo(bar: int):
    pass
    
# becomes

def foo(bar: int):
    if not isinstance(bar, int):
        raise TypeError("argument 'bar' is not of type 'int'")
```

```py
func foo(bar: Qux & Quy):
    pass
    
# becomes

def foo(bar):
    if not isinstance(bar, Qux):
        raise TypeError("argument 'bar' is not of type 'Qux'")
        
    if not isinstance(bar, Quy):
        raise TypeError("argument 'bar' is not of type 'Quy'")
```

```py
func foo(bar: ['a_method']):
    pass
    
# becomes

def foo(bar):
    if not all(hasattr(bar, attr) for attr in ['a_method']):
        raise TypeError("argument 'bar' lacks method 'a_method'")
```
