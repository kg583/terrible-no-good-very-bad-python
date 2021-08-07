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

        # Create the parent instances to use before the actual constructor
        its = []
        for cls in mro:
            if cls is not object:
                its.append(cls(*args, **kwargs))

        # Continue the initialization chain
        super().__init__(*args, **kwargs)
        self.__its = its

        # Set the default reductive behavior
        self.__func = func if func is not None else lambda x, y: y

    def __getattribute__(self, name):
        # Find all viable attributes from the list of __dict__'s
        attrs = {}
        for it in object.__getattribute__(self, "_Merger__its"):
            try:
                # Try the class first
                attr = getattr(it.__class__, name)
            except KeyError:
                # Try the instance next
                try:
                    attr = getattr(it, name)
                except AttributeError:
                    # Guess it's not here
                    continue

            attrs[it] = attr

        if attrs:
            # Get the merge function
            func = object.__getattribute__(self, "_Merger__func")

            if all(hasattr(attr, "__call__") or hasattr(attr, "__func__") for attr in attrs.values()):
                # If EVERY attribute can be called, return a function that reduces with whatever arguments
                # Arity does not NEED to match but it probably should
                def merger(*args, **kwargs):
                    def passer(t):
                        k, v = t
                        try:
                            return v(*args, **kwargs)
                        except TypeError:
                            return v(k, *args, **kwargs)

                    return reduce(func, map(passer, attrs.items()))

                return merger
            else:
                # If just one attribute is not a function, return the reduction
                return reduce(func, attrs.values())
        else:
            # Fallback to the default __getattribute__ behavior
            return super().__getattribute__(self, name)
