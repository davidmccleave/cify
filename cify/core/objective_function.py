from typing import List
from copy import deepcopy
from cify.core.optimization import Optimization

__all__ = ['ObjectiveFunction', 'MultiObjectiveFunction']


class ObjectiveFunction(object):
    """
    Defines an objective function to be optimized.
    """

    def __init__(
            self,
            function,
            optimization: Optimization = Optimization.Min,
            n_dimensions: int = 10,
            bounds: list = None,
            vector_constraints: list = None,
            dynamic_variables: dict = None,
            name: str = None,
            **kwargs
    ):
        """
        :param function: A single callable function, or list of callable functions.
        :type function: A function or list of functions
        :param optimization: Indicates whether the :class:`ObjectiveFunction` is to be minimized or maximized.
        :type optimization: :class:`~cify.core.optimization.Optimization` (Optimization.Min or Optimization.Max)
        :param n_dimensions: The number of dimensions for the :class:`ObjectiveFunction`.
        :type n_dimensions: int
        :param bounds: The bounds for the :class:`ObjectiveFunction`. Given as a list of lists.
        :type bounds: A list of lists containing real valued numbers
        :param vector_constraints: Constraints that act on the vectors of :class:`Agent` s.
        :type vector_constraints: list of functions
        :param dynamic_variables: A dictionary of attributes belonging to this :class:`ObjectiveFunction` that must
                                  be called at the end of each iteration.
        :type dynamic_variables: dict
        :param name: An optional name for the objective function.
        :type name: string
        """
        self.__n_evaluations = 0

        self.__function = function
        self.__optimization = optimization
        self.__n_dimensions = n_dimensions

        # Set bounds.
        self.__set_bounds(bounds)

        self.__vector_constraints = vector_constraints
        self.__dynamic_variables = dynamic_variables

        if name is not None:
            self.name = name
        else:
            self.name = self.__function.__name__

        self.__dict__.update(kwargs)

    # --------------------------------- Getters --------------------------------

    @property
    def function(self):
        """
        Returns the function that is to be optimized.

        :return: The function being optimized.
        :rtype: callable
        """
        return self.__function

    @property
    def optimization(self) -> Optimization:
        """
        Returns the :class:`ObjectiveFunction`'s optimization type, minimization or maximization.

        :return: The enum representing the :class:`ObjectiveFunction`'s optimization type.
        :rtype: :class:`Optimization`
        """
        return self.__optimization

    @property
    def n_dimensions(self) -> int:
        """
        The number of dimensions of the search space.

        :return: The number of dimensions in this :class:`ObjectiveFunction`.
        :rtype: int
        """
        return self.__n_dimensions

    @property
    def bounds(self) -> list:
        """
        The boundary constraints represented as a list of the form:

        `[[LB1, UB1], ..., [LBn, UBn]]`

        where UB is the upper bound and LB is the lower bound of the search space for that dimension.
        Can also be passed as a list of the form:

        `[LB, UB]`

        where the bounds will apply to all dimensions of the search space.

        :return: The boundary constraints.
        :rtype: list
        """
        return self.__bounds

    @property
    def vector_constraints(self) -> list:
        """
        The vector constraints represented as a list of lists of the form:

        `[[LB1, UB1], ..., [LBn, UBn]]`

        where UB is the upper bound and LB is the lower bound of that dimension.

        :return: The vector constraints
        :rtype: list
        """
        return self.__vector_constraints

    @property
    def dynamic_variables(self) -> dict:
        """A dictionary of dynamic variables that are updated at each iteration."""
        return self.__dynamic_variables

    # --------------------------------- Setters --------------------------------

    @function.setter
    def function(self, function):
        """Sets the function to be optimized."""
        self.__function = function

    @optimization.setter
    def optimization(self, optimization):
        """Sets the :class:`ObjectiveFunction`'s :class:`Optimization` type."""
        self.__optimization = optimization

    @n_dimensions.setter
    def n_dimensions(self, num: int):
        """Sets the number of dimensions."""
        self.__n_dimensions = num

    @bounds.setter
    def bounds(self, bounds):
        """Sets the boundary constraints of the search space."""
        self.__set_bounds(bounds)

    @vector_constraints.setter
    def vector_constraints(self, vector_constraints):
        """Sets the vector constraints """
        self.__vector_constraints = vector_constraints

    @dynamic_variables.setter
    def dynamic_variables(self, dynamic_variables):
        """Sets the dynamic variables to be updated at each iteration."""
        self.__dynamic_variables = dynamic_variables

    # --------------------------------- Methods --------------------------------

    def __set_bounds(self, bounds):
        if bounds is not None:
            if len(bounds) < self.n_dimensions or (len(bounds) == 2 and len(bounds[0]) != 2 and self.n_dimensions == 2):
                self.__bounds = []
                for _ in range(self.__n_dimensions):
                    self.__bounds.append([bounds[0], bounds[1]])
            else:
                self.__bounds = bounds
        else:
            bnds = []
            for _ in range(self.__n_dimensions):
                bnds.append([-1000, 1000])
            self.__bounds = bnds

    def get_n_evaluations(self) -> int:
        """
        Returns the number of evaluations performed and resets the counter.

        :return: Number of function evaluations.
        :rtype: int
        """
        num = self.__n_evaluations
        self.__n_evaluations = 0
        return num

    def increment(self):
        """
        Increments the :class:`ObjectiveFunction` by calling all dynamic variables contained in ``dynamic_variables``.
        This method is called by the ``iterate`` method of any :class:`Algorithm` and typically does not need to be
        manually called.
        """
        if self.dynamic_variables is not None:
            for key in self.dynamic_variables.keys():
                value = self.dynamic_variables.get(key)
                if callable(value):
                    self.dynamic_variables.update({key: value()})
                    self.__dict__.update({key: value()})
                else:
                    self.dynamic_variables.update({key: value})
                    self.__dict__.update({key: value})

    def cmp(self, a, b) -> bool:
        """
        A comparison method returned by an :class:`ObjectiveFunction` which can be used when constructing algorithms
        to handle optimizing minimization or maximization objective functions. The ``cmp()`` method takes two arguments,
        the first argument is the value of a :class:`~cify.core.position.Position` object that is being compared to
        a second :class:`~cify.core.position.Position` object to see if it's value is better. These arguments can be
        any real valued numbers.

        For minimization objective functions the ``cmp()`` method checks whether the first position value is less than
        the second position value, and for maximization objective functions the ``cmp()`` method checks whether the
        first position value is greater than the second position value. Think of it as saying, "is this first value
        better than the second value".

        :param a: The first value
        :type a: Any real valued number, typically a float
        :param b: The second value
        :type b: Any real valued number, typically a float

        :return: Whether ``a`` is better than ``b``.
        :rtype: bool
        """
        return self.optimization.cmp(a, b)

    def evaluate(self, vector) -> float:
        """
        Evaluates a vector using the :class:`ObjectiveFunction`.

        :param vector: The vector to evaluate.
        :type vector: a list or array-like

        :return: A float representing the result of the evaluation.
        :rtype: float
        """
        self.__n_evaluations += 1
        return self.__function(vector)

    def satisfies_constraints(self, vector) -> bool:
        """
        Checks whether a given vector satisfies the ``vector_constraints`` of the :class:`ObjectiveFunction`.

        :param vector: The vector to check.
        :type vector: a list or array-like
        :return: A boolean value indicating whether the vector satisfies the constraints.
        :rtype: bool
        """

        # Check boundary constraints.
        if self.bounds is not None:
            for idx in range(self.n_dimensions):
                if vector[idx] < self.lower_bounds()[idx] or vector[idx] > self.upper_bounds()[idx]:
                    return False

        # Check vector constraints.
        if self.__vector_constraints is not None:
            return all(f(vector) for f in self.__vector_constraints)

        return True

    def lower_bounds(self) -> list or None:
        """
        Returns a list of floats consisting of the lower bounds of the :class:`ObjectiveFunction` search space per
        dimension.

        :return: A list of the lower bounds of the :class:`ObjectiveFunction` search space.
        :rtype: list or None, if there are no bounds
        """
        if self.bounds is not None:
            return [i[0] for i in self.__bounds]
        else:
            return None

    def upper_bounds(self) -> list or None:
        """
        Returns a list of floats consisting of the upper bounds of the :class:`ObjectiveFunction` search space
        per dimension.

        :return: A list of the upper bounds of the :class:`ObjectiveFunction` search space.
        :rtype: list or None, if there are no bounds
        """
        if self.bounds is not None:
            return [i[1] for i in self.__bounds]
        else:
            return None

    def copy(self):
        """
        Returns a deep copy of the :class:`ObjectiveFunction` object.

        :return: A deep copy of the :class:`ObjectiveFunction`.
        :rtype: :class:`ObjectiveFunction`
        """
        return deepcopy(self)

    # ----------------------------- Special Methods ----------------------------

    def __eq__(self, other) -> bool:
        """Checks if two :class:`ObjectiveFunction` objects are equal."""
        if not isinstance(other, type(self)) \
                or self is not other \
                or self.__dict__ != other.__dict__:
            return False
        return True

    def __str__(self) -> str:
        """Returns a str representation of the :class:`ObjectiveFunction`"""
        if self.optimization == Optimization.Min:
            return f"Minimization: {self.__function}\n" \
                   f"Bounds: {self.__bounds}\n" \
                   f"Vector Constraints: {self.__vector_constraints}\n"
        elif self.optimization == Optimization.Max:
            return f"Maximization: {self.__function}\n" \
                   f"Bounds: {self.__bounds}\n" \
                   f"Vector Constraints: {self.__vector_constraints}\n"


class MultiObjectiveFunction(object):
    """
    A :class:`MultiObjectiveFunction` is a wrapper class for a list of :class:`ObjectiveFunction` s and is for use
    by all multi-objective optimization algorithms.
    """

    def __init__(self, functions: List[ObjectiveFunction], **kwargs):
        """
        :param functions: The list of :class:`ObjectiveFunction` s that make up this :class:`MultiObjectiveFunction`.
        :type functions: A list of :class:`ObjectiveFunction` s.
        """
        self.__functions = functions
        self.__dict__.update(kwargs)

    # --------------------------------- Getters --------------------------------

    @property
    def functions(self) -> List[ObjectiveFunction]:
        """Returns a list of the :class:`ObjectiveFunction` s that make up this :class:`MultiObjectiveFunction`."""
        return self.__functions

    def get_function(self, index: int or str) -> ObjectiveFunction or None:
        """
        Returns a specific function based on it's index or name. If a name is supplied, and it cannot be found,
        ``None`` is returned.

        :param index: The index or name of the function to be returned.
        :type index: int or str

        :return: The :class:`ObjectiveFunction` at the given index or with the given name.
        :rtype: :class:`ObjectiveFunction`
        """
        if isinstance(index, int):
            return self.__functions[index]
        if isinstance(index, str):
            for function in self.__functions:
                if hasattr(function, 'name'):
                    if function.name == index:
                        return function
            return None
        else:
            raise TypeError(f'Expected list or str, got {type(index)} instead.')

    # --------------------------------- Setters --------------------------------

    @functions.setter
    def functions(self, functions):
        """Sets the :class:`ObjectiveFunction` s that make up this :class:`MultiObjectiveFunction`."""
        self.__functions = functions

    # --------------------------------- Methods --------------------------------

    def evaluate(self, vector, function: int or str = None) -> float or List[float]:
        """
        Evaluates a vector on one or more objective functions.

        To evaluate a vector on all the objective functions::

            evaluate(vector=<vector>)

        This will return a list of the :class:`ObjectiveFunction` values where the
        first item in the list is the value of the vector evaluated on the
        first :class:`ObjectiveFunction` and the last item is the value of the vector
        evaluated on the last :class:`ObjectiveFunction` passed to the
        :class:`~cify.core.objectivefunction.MultiObjectiveFunction` object.

        To evaluate a vector on only one of the objective functions::

            evaluate(vector=<vector>, function=<index or name>)

        This will return a float representing the value of the vector evaluated
        on the :class:`ObjectiveFunction` corresponding to the function parameter.
        The function parameter can be the index or name of a function.

        :param vector: The vector to evaluate.
        :type vector: a list or array-like
        :param function: Which function to use for vector evaluation, given as an index or name.
        :type function: int or str

        :return: A float representing the result of the evaluation or a list of floats representing all evaluations.
        :rtype: float or list of floats
        """

        if function is not None:
            return self.get_function(function).evaluate(vector)
        else:
            values = []
            for i in range(len(self.__functions)):
                values.append(self.__functions[i].evaluate(vector))
            return values

    def copy(self):
        """Returns a deep copy of the :class:`MultiObjectiveFunction`."""
        return deepcopy(self)

    # ----------------------------- Special Methods ----------------------------

    def __eq__(self, other) -> bool:
        """Checks if two :class:`MultiObjectiveFunction` objects are equal."""
        if not isinstance(other, MultiObjectiveFunction):
            return False
        if len(other.functions) != len(self.functions):
            return False
        for i in range(len(self.functions)):
            if self.functions[i] != other.functions[i]:
                return False
        return True

    def __setitem__(self, index, data):
        self.functions[index] = data

    def __getitem__(self, index):
        return self.get_function(index)
