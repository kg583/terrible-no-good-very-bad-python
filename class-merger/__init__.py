"""
A mixin class to "merge" the behavior of multiple parent classes

Attributes of the parents with the same name are combined using a function of choice via functools.reduce
The default behavior is to call all parent attributes and return the final value
This contrasts the standard OOP behavior of overriding the desired attribute with the first viable parent

Class attributes are searched first, followed by instance attributes
The latter behavior requires a memory footprint double that of a usual instance
If an attribute name is found both in the class and in an instance, the class value takes priority

Iteration order is dictated by the derived class's MRO
The relevant MRO starts after this class, allowing some parents to be excluded from the merge
If no parent contains the desired attribute, default __getattribute__ behavior resumes for the derived class

Examples are included in this package's examples.py
"""
from functools import reduce

class Merger:
    def __init__(self, *args, func=None, **kwargs):
        # Get the MRO as an iterator
        # This pattern is roughly how super() works
        mro = iter(object.__getattribute__(self, "__class__").__mro__)
        for cls in mro:
            if cls is Merger:
                break

        # Get the __dict__'s for instances AND classes in the MRO
        dicts = []
        for cls in mro:
            try:
                # These instances are all created again by the actual constructor, oh well
                it = cls(*args, **kwargs)
                dct = it.__dict__
                del it
                try:
                    # Class attributes take precedence is they exist
                    dct.update(cls.__dict__)
                except AttributeError:
                    pass
                dicts.append(dct)
            except AttributeError:
                pass

        # Continue the initialization chain
        super().__init__(*args, **kwargs)
        self.__dicts = dicts
        
        # Set the default reductive behavior
        self.__func = func if func is not None else lambda x, y: y

    def __getattribute__(self, name):
        # Find all viable attributes from the list of __dict__'s
        attrs = []
        for dct in object.__getattribute__(self, "_Merger__dicts"):
            try:
                attr = dct[name]
                try:
                    # Get the function part of a static method if necessary
                    attrs.append(attr.__func__)
                except AttributeError:
                    attrs.append(attr)
            except KeyError:
                # Don't worry if a parent lacks the attribute
                pass

        func = object.__getattribute__(self, "_Merger__func")
        if attrs:
            if all(hasattr(attr, "__call__") for attr in attrs):
                # If EVERY attribute can be called, return a function that reduces with whatever arguments
                return lambda *args, **kwargs: reduce(func, map(lambda meth: meth(*args, **kwargs), attrs))
            else:
                # If just one attribute is not a function, return the reduction
                return reduce(func, attrs)
        else:
            # Fallback to the default __getattribute__ behavior
            # Using object would be safer, but a parent could theoretically also redefine this
            return super().__getattribute__(self, name)
