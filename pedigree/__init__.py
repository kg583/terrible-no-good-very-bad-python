"""
Metaclass framework for "merging" multiple parent classes, overriding default inheritance behavior.

Examples are included in this package's examples.py.
"""
from functools import reduce


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
        keeps = tuple(set(bases) - set(ignores))

        # Collect every non-dunder attribute
        for attr in (k for k in set(sum((dir(base) for base in keeps), [])) | set(attrs.keys())
                     if not k.startswith("__")):
            ps = [getattr(base, attr) for base in keeps if hasattr(base, attr)]

            if any(callable(p) for p in ps):
                # Turn attributes into constant methods
                ps = [p if callable(p) else lambda *args, **kwargs: p for p in ps]

                # Fun flip-flop algorithm to merge ordered methods
                for order in range(len(ps)):
                    def front(p):
                        try:
                            o = getattr(p, "__order")
                            return (o - order > 0 or o <= -1) - (o - order < 0 <= o)
                        except AttributeError:
                            return 1

                    def back(p):
                        try:
                            o = getattr(p, "__order")
                            return (o + order > -1 >= o) - (o + order < -1 or o >= 0)
                        except AttributeError:
                            return -1

                    ps.sort(key=front)
                    ps.sort(key=back)

                # Make a dynamic class to hold onto the parents
                def __init__(self, psc: list):
                    self.__ps = psc.copy()
                    self.f = lambda *args, **kwargs: reduce(func, map(lambda f: f(*args, **kwargs), self.__ps))

                # Would make the class callable but that gets oddly messy
                attrs[attr] = type(attr, (), {"__init__": __init__})(ps).f
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
