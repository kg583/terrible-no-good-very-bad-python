"""
A mixin class to "merge" the behavior of multiple parent classes.

Attributes of the parents with the same name are combined using a function of choice via functools.reduce.
The default behavior is to call all parent attributes and return the final value.
This contrasts the standard OOP behavior of overriding the desired attribute with the first viable parent.

Class attributes are searched first, followed by instance attributes.
The latter behavior requires a memory footprint double that of a usual instance.
If an attribute name is found both in the class and in an instance, the class value takes priority.

Iteration order is dictated by the derived class's MRO.
The traversed MRO starts after this class, allowing earlier parents to be excluded from the merge.
If no parent contains the desired attribute, default __getattribute__ behavior resumes for the derived class.

Examples are included in this package's examples.py.
"""
from functools import reduce
import operator


class Merger:
    """
    Merges parent classes by combining identically-named attributes in a specified way.
    Only parents further up the MRO than this class are merged.
    """
    def __init__(self, *args, func=None, ignores=None, use_instances=False, **kwargs):
        """
        Initializes this class, passing unused arguments upstream.

        :param func: A function of two arguments with a single return used to combine parent attributes.
                     The default value of None corresponds to the function which returns its second argument.
        :param ignores: An iterable of classes to ignore when merging (can be empty or None).
        :param use_instances: A boolean dictating whether instance attributes are merged.
                              If set to True, copies of each parent instance are kept in memory for future look-up.
                              By default, instance attributes are not merged.
        """
        # Get the MRO as an iterator
        # This pattern is roughly how super() works
        mro = iter(object.__getattribute__(self, "__class__").__mro__)
        for cls in mro:
            if cls is Merger:
                break

        # Create parent instances to use before the actual constructor
        # All parent classes must be cooperative (or just take the same args) for this to work
        clits = []
        for cls in mro:
            if all(cls is not ignore for ignore in tuple(ignores if ignores is not None else ()) + (object,)):
                # This pattern expects cooperative parents
                clits.append((cls, cls(*args, **kwargs) if use_instances else None))

        # Continue the initialization chain
        super().__init__(*args, **kwargs)
        self.__clits = clits

        # Set the default merge behavior
        self.__func = func if func is not None else lambda x, y: y

    def __getattribute__(self, name):
        # Partition attributes into first, default, and last sections of the call order
        attrs = [[], [], []]
        for cls, it in object.__getattribute__(self, "_Merger__clits"):
            try:
                # Try the class first
                attr = getattr(cls, name)
            except AttributeError:
                # Try the instance next (will be None if use_instances is False)
                try:
                    attr = getattr(it, name)
                except AttributeError:
                    # Guess it's not here
                    continue

            # Store the desired attribute in the appropriate section
            attrs[getattr(attr, "__merge_order__", 1)] += [(cls, attr)]

        # Unite the sections to get the final call order
        attrs = dict(reduce(operator.add, attrs))
        if attrs:
            # Get the merging function
            func = object.__getattribute__(self, "_Merger__func")

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
