import numpy as np
from typing import List
from cify.core.objective_function import ObjectiveFunction, MultiObjectiveFunction

__all__ = ['Position']


class Position:
    """
    A simple object that defines a position vector, and it's evaluation.
    :class:`~cify.core.position.Position` objects are typically handled
    by an instantiating :class:`Agent` such as a :class:`~cify.si.pso.particle.Particle`
    or :class:`~cify.ec.individual.Individual`. It is rare that a user may wish to
    use :class:`Position` objects directly.
    """

    def __init__(
            self,
            vector: np.ndarray or list = None,
            obj_func: ObjectiveFunction or MultiObjectiveFunction = None,
            value: float or List[float] = None,
    ):
        """
        :param vector: The position vector. This will always be converted to a Numpy array.
        :type vector: Numpy array or list
        :param obj_func: The :class:`ObjectiveFunction` to use for :class:`Position` evaluation.
        :type obj_func: :class:`~cify.core.objectivefunction.ObjectiveFunction` or
                        :class:`~cify.core.objectivefunction.MultiObjectiveFunction`
        :param value: The evaluated value or values of the position vector.
        :type value: float or list of floats
        """

        # Set vector
        if isinstance(vector, Position):
            self.__vector = vector.vector
        else:
            self.__vector = np.array(vector)

        # Set objective function
        self.__obj_func = obj_func
        if self.__obj_func:
            self.__prev_obj_func = self.__obj_func.copy()
        else:
            self.__prev_obj_func = None

        # Set value(s)
        if value:
            if type(value) is not list and type(self.__obj_func) is MultiObjectiveFunction:
                self.__value[0] = value
                for i in range(1, len(self.__obj_func.functions)):
                    self.__value[i] = None
            else:
                self.__value = value
        else:
            if self.__obj_func:
                self.__value = obj_func.evaluate(self.__vector)
            else:
                self.__value = None

    # --------------------------------- Getters --------------------------------

    @property
    def vector(self) -> np.ndarray:
        """Returns the vector as a Numpy array."""
        return self.__vector

    @property
    def obj_func(self) -> ObjectiveFunction:
        """Returns the :class:`Position`'s :class:`ObjectiveFunction`."""
        return self.__obj_func

    @property
    def value(self) -> float or list:
        """
        Returns the current value of the :class:`Position` in its :class:`ObjectiveFunction`'s search space.

        If the value has already been evaluated and the :class:`Position` has not changed its position,
        its vector has not changed, and the :class:`ObjectiveFunction` has not changed, the value will not be
        re-evaluated. This is in an attempt to save from the computational budget of CIFY algorithms as no
        :class:`Position` evaluations should take place when they do not need to.
        """
        if self.__obj_func != self.__prev_obj_func and self.__obj_func is not None:
            self.__value = self.__obj_func.evaluate(self.__vector)
            self.__prev_obj_func = self.__obj_func.copy()
        return self.__value

    # --------------------------------- Setters --------------------------------

    @vector.setter
    def vector(self, vector: np.ndarray or list):
        """
        Sets the :class:`Position` s vector. Triggers reevaluation of the :class:`Position`'s value.

        :param vector: A new vector.
        :type vector: Numpy array or list
        """
        if not isinstance(vector, np.ndarray) and not isinstance(vector, list):
            raise TypeError(f"Expected np.ndarray or list, received {type(vector)}.")

        if isinstance(vector, Position):
            self.__vector = vector.vector
        elif isinstance(vector, np.ndarray):
            self.__vector = vector
        else:
            self.__vector = np.array(vector)
        self.__value = None

    @obj_func.setter
    def obj_func(self, obj_func: ObjectiveFunction):
        """Sets the :class:`Position`'s `ObjectiveFunction`."""
        self.__obj_func = obj_func

    @value.setter
    def value(self, value: float or list):
        """
        Sets the :class:`Position`'s value, it is rare that a user will directly set the value of a :class:`Position`.
        """
        self.__value = value

    # --------------------------------- Methods --------------------------------

    def copy(self):
        """
        Creates and returns a deep copy of the :class:`~cify.core.position.Position` object.

        :return: A copy of the original :class:`~cify.core.position.Position` object.
        """
        return Position(
            obj_func=self.obj_func, vector=self.vector.copy(), value=self.value
        )

    def evaluate(self):
        """
        Evaluates the :class:`Position` object using its :class:`ObjectiveFunction` and sets its ``value`` field. This
        function should not be called directly, since smart evaluation is handled when directly
        accessing the :class:`Position`'s ``value`` field.
        """
        self.value = self.obj_func.evaluate(self.vector)

    def satisfies_constraints(self) -> bool:
        """
        Checks whether the :class:`~cify.core.position.Position` satisfies the constraints
        of its :class:`~cify.core.obj_func.ObjectiveFunction`.
        """
        return self.obj_func.satisfies_constraints(self.vector)

    # ----------------------------- Special Methods ----------------------------

    # or self is not other \
    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)) \
                or not all(x == y for x, y in zip(self.vector, other.vector)) \
                or not all(x == y for x, y in zip(self.__dict__, other.__dict__)):
            return False
        return True

    # Comparative Operators

    def __lt__(self, other) -> bool:
        if self.value is None:
            return 0 < other.value
        if other.value is None:
            return self.value < 0
        return self.value < other.value

    def __le__(self, other) -> bool:
        if self.value is None:
            return 0 <= other.value
        if other.value is None:
            return self.value <= 0
        return self.value <= other.value

    def __gt__(self, other) -> bool:
        if self.value is None:
            return 0 > other.value
        if other.value is None:
            return self.value > 0
        return self.value > other.value

    def __ge__(self, other) -> bool:
        if self.value is None:
            return 0 >= other.value
        if other.value is None:
            return self.value >= 0
        return self.value >= other.value

    # Mathematical Operators

    def __add__(self, other):
        if type(other) == Position:
            return Position(obj_func=self.__obj_func, vector=(self.__vector + other.__vector))
        else:
            return Position(obj_func=self.__obj_func, vector=(self.__vector + np.array(other)))

    def __sub__(self, other):
        if type(other) == Position:
            return Position(obj_func=self.__obj_func, vector=(self.__vector - other.__vector))
        else:
            return Position(obj_func=self.__obj_func, vector=(self.__vector - np.array(other)))

    def __mul__(self, other):
        if type(other) == Position:
            return Position(obj_func=self.__obj_func, vector=(self.__vector * other.__vector))
        else:
            return Position(obj_func=self.__obj_func, vector=(self.__vector * np.array(other)))

    def __truediv__(self, other):
        if type(other) == Position:
            return Position(obj_func=self.__obj_func, vector=(self.__vector / other.__vector))
        else:
            return Position(obj_func=self.__obj_func, vector=(self.__vector / np.array(other)))

    def __floordiv__(self, other):
        if type(other) == Position:
            return Position(obj_func=self.__obj_func, vector=(self.__vector // other.__vector))
        else:
            return Position(obj_func=self.__obj_func, vector=(self.__vector // np.array(other)))

    # Misc Special Methods

    def __len__(self) -> int:
        return len(self.__vector)

    def __iter__(self):
        return iter(self.__vector)

    def __getitem__(self, index):
        return self.__vector[index]

    def __setitem__(self, index, value):
        self.__vector[index] = value

    def __str__(self) -> str:
        """Returns a string representation of the :class:`Position`."""
        return f"{self.vector} -- value --> {self.value}"
