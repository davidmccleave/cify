import operator
from enum import Enum

__all__ = ['Optimization']


class Optimization(Enum):
    """
    The :class:`Optimization` class is an enum that is used to define whether an :class:`ObjectiveFunction` is to
    be minimized or maximized. The class contains two methods, of which one is more useful, ``cmp``.
    """

    Min = 1
    Max = 2

    def cmp(self, a, b) -> bool:
        """
        A comparison function returned by an objective function which can be used when constructing algorithms
        to handle optimizing minimization or maximization objective functions. The ``cmp`` function takes two
        arguments, the first argument is the value of a :class:`~cify.core.position.Position` object that is being
        compared to a second :class:`~cify.core.position.Position` object to see if it's value is better.

        For minimization objective functions the ``cmp`` function checks whether the first position value is less than
        the second position value, and for maximization objective functions the ``cmp`` function checks whether the
        first position value is greater than the second position value. Think of it as saying, "is this first position
        better than the second position".

        :param a: The first value
        :type a: Any real valued number, typically a float
        :param b: The second value
        :type b: Any real valued number, typically a float

        :return: Whether ``a`` is better than ``b``.
        :rtype: bool
        """
        if self.value == Optimization.Min.value:
            return operator.lt(a, b)
        elif self.value == Optimization.Max.value:
            return operator.gt(a, b)
        else:
            raise TypeError(f"One of your objective functions does not have an optimization type "
                            f"(Optimization.Min or Optimization.Max)")

    def verb(self) -> str:
        """Returns a verb representation of the optimization type."""
        if self.value == 1:
            return "Minimizing"
        return "Maximizing"
