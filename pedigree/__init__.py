"""
Metaclass framework for "merging" multiple parent classes, overriding default inheritance behavior.

Examples are included in this package's examples.py.
"""
from functools import reduce
from inspect import getattr_static


class Pedigree(type):
    """
    A metaclass to "merge" the behavior of multiple parent classes

    Class attributes of the parents with the same name are combined using a function of choice via functools.reduce.
    The default behavior is to call all parent attributes and return the final value.
    This contrasts the standard OOP behavior of overriding the desired attribute with the first viable parent.
    Iteration order is dictated by the order of the bases parameter
    """

    def __new__(mcs, clsname: str, bases: tuple, attrs: dict, func=None, ignores=None):
        """

        """
        func = func or (lambda x, y: y)
        ignores = ignores or ()
        keeps = tuple(base for base in bases if base not in ignores)

        # Collect every non-dunder attribute
        for attr in (k for k in set(sum((dir(base) for base in keeps), [])) | set(attrs.keys())
                     if not k.startswith("__")):
            ps = [getattr_static(base, attr) for base in keeps if hasattr(base, attr)]

            if any(callable(p) for p in ps):
                def __init__(self, pc):
                    self.__func__ = pc

                # Turn attributes into constant methods and special methods into less special methods
                ps = [p if hasattr(p, "__func__") else
                      type("", (), {"__init__": __init__})(p if callable(p) else lambda *args, **kwargs: p)
                      for p in ps]

                # Fun flip-flop algorithm to merge ordered methods
                for order in range(len(ps)):
                    def front(p):
                        try:
                            o = getattr(p.__func__, "__order")
                            return (o - order > 0 or o <= -1) - (o - order < 0 <= o)
                        except AttributeError:
                            return 1

                    def back(p):
                        try:
                            o = getattr(p.__func__, "__order")
                            return (o + order > -1 >= o) - (o + order < -1 or o >= 0)
                        except AttributeError:
                            return -1

                    ps.sort(key=front)
                    ps.sort(key=back)

                # Determine if self needs to be passed to the methods
                def caller(f):
                    if isinstance(f, staticmethod):
                        return lambda *args, **kwargs: f.__func__(*args[1:], **kwargs)

                    else:
                        return f.__func__

                # Make a dynamic class to hold onto the parents
                def __init__(self, psc: list):
                    self.__ps = psc.copy()
                    self.__func__ = lambda *args, **kwargs: \
                        reduce(func, map(lambda f: caller(f)(*args, **kwargs), self.__ps))

                # Would make the class callable but that gets oddly messy
                attrs[attr] = type("", (), {"__init__": __init__})(ps).__func__
            else:
                # It's just attributes
                attrs[attr] = reduce(func, ps)

            # Remove attributes handled by not ignored parents
            for base in ignores:
                if hasattr(base, attr):
                    delattr(base, attr)

        # Make the derived class think it knows its parents
        attrs["__bases__"] = bases
        return super().__new__(mcs, clsname, ignores, attrs)


def force(order: int):
    """
    Decorator which pushes methods to the specified position in the call order, regardless of position in the MRO.
    Methods with non-negative order are pushed to the front, ordered accordingly
    Methods with negative order are pushed to the back, ordered accordingly
    Precedence between multiple decorated methods then falls back to the MRO.
    """
    def forcer(func):
        func.__order = order
        return func

    return forcer


def force_first(func):
    """
    Decorator which pushes methods to the front of the call order, regardless of position in the MRO.
    Precedence between multiple decorated methods then falls back to the MRO.
    """
    return force(0)(func)


def force_last(func):
    """
    Decorator which pushes methods to the end of the call order, regardless of position in the MRO.
    Precedence between multiple decorated methods then falls back to the MRO.
    """
    return force(-1)(func)


__all__ = ["Pedigree", "force", "force_first", "force_last"]
