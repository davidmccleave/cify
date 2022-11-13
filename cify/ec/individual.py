from cify import Agent
from cify.core.position import Position
from cify.core.objective_function import ObjectiveFunction
from cify.core.utils import get_position_vector

__all__ = ['Individual']


class Individual(Agent):
    """
    Defines an :class:`Individual` for use in evolutionary computation.

    :class:`Individual` s are at the core of any evolutionary computation algorithm. When instantiating an
    :class:`Individual`, it is only necessary to supply an :class:`ObjectiveFunction`. If no chromosome is provided,
    the elements of the chromosome will be sampled from a uniform distribution within the bounds of the
    :class:`ObjectiveFunction`.
    """

    def __init__(
        self,
        chromosome: Position = None,
        obj_func: ObjectiveFunction = None,
        **kwargs,
    ):
        """
        :param chromosome: The initial chromosome.
        :type chromosome: :class:`~cify.core.position.Position` or array-like
        :param obj_func: The objective function used for evaluation and bounds by the :class:`Individual`.
        :type obj_func: :class:`ObjectiveFunction`
        """
        super().__init__(**kwargs)

        self.__obj_func = obj_func

        if isinstance(chromosome, Individual):
            self.__chromosome = chromosome.chromosome
        elif isinstance(chromosome, Position):
            self.__chromosome = chromosome
        else:
            if chromosome is not None:
                self.__chromosome = Position(obj_func=obj_func, vector=chromosome)
            else:
                self.__chromosome = Position(
                    obj_func=obj_func, vector=get_position_vector(obj_func=obj_func)
                )

        # Set personal best position and social best position.
        self.__p_best_position = self.__chromosome.copy()
        self.__social_best_pos = self.chromosome.copy()

    # --------------------------------- Getters --------------------------------

    @property
    def position(self) -> Position:
        """Returns the ``chromosome`` as a :class:`Position` object."""
        return self.chromosome

    @property
    def chromosome(self) -> Position:
        """Returns the ``chromosome`` as a :class:`Position` object."""
        return self.__chromosome

    @property
    def p_best_chromosome(self) -> Position:
        """Returns the personal best ``chromosome`` as a :class:`Position` object."""
        return self.__p_best_position

    @property
    def p_best_position(self) -> Position:
        """Returns the personal best ``chromosome`` as a :class:`Position` object."""
        return self.__p_best_position

    @property
    def social_best_chromosome(self) -> Position:
        """Returns the social or neighbourhood best ``chromosome`` as a :class:`Position` object."""
        return self.__social_best_pos

    @property
    def social_best_pos(self) -> Position:
        """Returns the social or neighbourhood best ``chromosome`` as a :class:`Position` object."""
        return self.__social_best_pos

    @property
    def obj_func(self) -> ObjectiveFunction:
        """Returns the :class:`ObjectiveFunction` this :class:`Individual` will be optimizing."""
        return self.__obj_func

    # --------------------------------- Setters --------------------------------

    @position.setter
    def position(self, position):
        """Sets the :class:`Individual`'s ``chromosome``."""
        if not self.frozen:
            self.__chromosome = Position(obj_func=self.__obj_func, vector=position)

    @chromosome.setter
    def chromosome(self, chromosome):
        """Sets the :class:`Individual`'s ``chromosome``."""
        if not self.frozen:
            self.__chromosome = Position(obj_func=self.__obj_func, vector=chromosome)

    @p_best_position.setter
    def p_best_position(self, position):
        """Sets the :class:`Individual`'s personal best chromosome."""
        if not self.frozen:
            self.__p_best_position = Position(obj_func=self.__obj_func, vector=position)

    @p_best_chromosome.setter
    def p_best_chromosome(self, position):
        """Sets the :class:`Individual`'s personal best chromosome."""
        if not self.frozen:
            self.__p_best_position = Position(obj_func=self.__obj_func, vector=position)

    @social_best_chromosome.setter
    def social_best_chromosome(self, position):
        """Sets the :class:`Individual`'s social or neighbourhood best chromosome."""
        if not self.frozen:
            self.__social_best_pos = Position(obj_func=self.__obj_func, vector=position)

    @social_best_pos.setter
    def social_best_pos(self, position):
        """Sets the :class:`Individual`'s social or neighbourhood best chromosome."""
        if not self.frozen:
            self.__social_best_pos = Position(obj_func=self.__obj_func, vector=position)

    @obj_func.setter
    def obj_func(self, obj_func):
        """Sets the :class:`Individual`'s :class:`ObjectiveFunction`."""
        self.__obj_func = obj_func

    # --------------------------------- Methods --------------------------------

    def reinit_uniform_chromosome(self):
        """Reinitializes the :class:`Individual`'s chromosome uniformly within the bounds of the search space.'"""
        self.chromosome.vector = get_position_vector(obj_func=self.obj_func)

    def evaluate(self):
        """Evaluates the :class:`Individual`'s chromosome."""
        self.__chromosome.evaluate()

    def satisfies_constraints(self) -> bool:
        """
        Checks whether the :class:`~cify.ec.individual.Individual` satisfies the constraints
        of its :class:`~cify.core.obj_func.ObjectiveFunction`.
        """
        return self.obj_func.satisfies_constraints(self.chromosome.vector)

    def copy(self):
        """Creates and returns a copy of the :class:`Individual` object.

        :return: A copy of the original individual object.
        :rtype: :class:`Individual`
        """
        duplicate = Individual(
            chromosome=self.__chromosome.copy(),
            obj_func=self.__obj_func,
        )
        return duplicate

    # ----------------------------- Special Methods ----------------------------

    def __str__(self) -> str:
        """Returns a str representation of the :class:`Individual`."""
        return f"chromosome: {self.chromosome}\n" \
               f"p_best_chromosome: {self.p_best_chromosome}" \
               f"obj_func: {self.obj_func}\n"

    def __eq__(self, other) -> bool:
        if isinstance(other, Individual):
            return self.__chromosome == other.__chromosome \
                   and self.__obj_func == other.__obj_func
        else:
            return False

    def __lt__(self, other) -> bool:
        if self.__chromosome.value is None:
            return False
        elif other.__chromosome.value is None:
            return True
        return self.__chromosome.value < other.__chromosome.value

    def __le__(self, other) -> bool:
        if self.__chromosome.value is None:
            return False
        elif other.__chromosome.value is None:
            return True
        return self.__chromosome.value <= other.__chromosome.value

    def __gt__(self, other) -> bool:
        if self.__chromosome.value is None:
            return False
        elif other.__chromosome.value is None:
            return True
        return self.__chromosome.value > other.__chromosome.value

    def __ge__(self, other) -> bool:
        if self.__chromosome.value is None:
            return False
        elif other.__chromosome.value is None:
            return True
        return self.__chromosome.value >= other.__chromosome.value
