"""
Mixin class and metaclass frameworks for "merging" multiple parent classes, overriding default inheritance behavior.

Details for each framework are given in their respective docs.

Examples are included in this package's examples.py.
"""
from functools import reduce
import operator


class MixinMerger:
    """
    A mixin class to "merge" the behavior of multiple parent classes.

    Class attributes of the parents with the same name are combined using a function of choice via functools.reduce.
    The default behavior is to call all parent attributes and return the final value.
    This contrasts the standard OOP behavior of overriding the desired attribute with the first viable parent.

    Iteration order is dictated by the derived class's MRO.
    The traversed MRO starts after this class, allowing earlier parents to be excluded from the merge.
    If no parent contains the desired attribute, super __getattribute__ behavior resumes for the derived class.
    """
    def __init__(self, *args, func=None, ignores=None, **kwargs):
        """
        Initializes this class, passing unused arguments upstream.

        :param func: A function of two arguments with a single return used to combine parent attributes.
                     The default value of None corresponds to the function which returns its second argument.
        :param ignores: An iterable of classes to ignore when merging (can be empty or None).
        """
        # Get the MRO as an iterator
        # This pattern is roughly how super() works
        mro = iter(object.__getattribute__(self, "__class__").__mro__)
        for cls in mro:
            if cls is MixinMerger:
                break
        mro = [cls for cls in mro if cls not in tuple(ignores or ()) + (object,)]

        # Continue the initialization chain
        super().__init__(*args, **kwargs)

        # Set the default merge behavior
        self.__func = func or (lambda x, y: y)
        self.__mro = mro

    def __getattribute__(self, name):
        # Partition attributes into first, default, and last sections of the call order
        attrs = [[], [], []]
        for cls in object.__getattribute__(self, "_MixinMerger__mro"):
            try:
                # Try the class first
                attr = getattr(cls, name)
            except AttributeError:
                # Guess it's not here
                continue

            # Store the desired attribute in the appropriate section
            attrs[getattr(attr, "__merge_order__", 1)] += [(cls, attr)]

        # Unite the sections to get the final call order
        attrs = dict(reduce(operator.add, attrs))
        if attrs:
            # Get the merging function
            func = object.__getattribute__(self, "_MixinMerger__func")

            if all(hasattr(attr, "__call__") for attr in attrs.values()):
                # If EVERY attribute can be called, return a function that reduces with whatever arguments
                # Arity does not need to match between methods
                def merger(*args, **kwargs):
                    def passer(t):
                        k, v = t
                        try:
                            # The method is static
                            return v(*args, **kwargs)
                        except TypeError:
                            # The method is regular or class
                            return v(k, *args, **kwargs)

                    return reduce(func, map(passer, attrs.items()))

                return merger
            else:
                # If at least one attribute is not a function, return the reduction
                # This technically permits mixing fields and methods
                return reduce(func, attrs.values())
        else:
            # Fallback to the default __getattribute__ behavior
            # Calling from object is technically safer, but the other parents could theoretically override it as well
            return super().__getattribute__(self, name)


def merge_first(func):
    """
    Decorator which pushes class methods to the front of the call order, regardless of position in the MRO.
    Precedence between multiple decorated methods then falls back to the MRO.
    """
    func.__merge_order__ = 0
    return func


def merge_last(func):
    """
    Decorator which pushes class methods to the end of the call order, regardless of position in the MRO.
    Precedence between multiple decorated methods then falls back to the MRO.
    """
    func.__merge_order__ = -1
    return func
