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
    meth len():
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

## Decorators

```py
@cached
func foo(x):
    pass
    
# becomes

from functools import lru_cache
@lru_cache
def foo(x):
    pass
```

# Syntax

```py
|val| + 7
|lst| // 2

# become

abs(val) + 7
len(lst) // 2
```

```py
start..end

# becomes

range(start, end + 1)

```

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
