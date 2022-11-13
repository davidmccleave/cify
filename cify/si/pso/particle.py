import numpy as np

from cify import Agent
from cify.core.position import Position
from cify.core.objective_function import ObjectiveFunction
from cify.core.utils import get_position_vector

__all__ = ['Particle']


class Particle(Agent):
    """
    Defines a :class:`~cify.si.pso.particle.Particle` object for use in PSO.

    :class:`~cify.si.pso.particle.Particle` objects are at the core of any swarm-based optimization algorithm. When
    instantiating a :class:`Particle` it is only necessary to supply an :class:`ObjectiveFunction` to be optimized.
    The remaining fields will then be given default values appropriate for the :class:`ObjectiveFunction`.
    """

    def __init__(
        self,
        position=None,
        velocity=None,
        obj_func: ObjectiveFunction = None,
        **kwargs,
    ):
        """
        :param position: The initial position, defaults to a uniformly sampled vector within the bounds of the provided
                         :class:`ObjectiveFunction`.
        :type position: :class:`~cify.core.position.Position` or array-like, optional
        :param velocity: The initial velocity.
        :type velocity: Any array-like, optional
        :param obj_func: The objective function used for evaluation and bounds by the :class:`Individual`.
        :type obj_func: :class:`ObjectiveFunction`
        """
        super().__init__(**kwargs)

        self.__obj_func = obj_func

        # Set position
        if isinstance(position, Particle):
            self.__position = position.position
        elif isinstance(position, Position):
            self.__position = position
        else:
            if position is not None:
                self.__position = Position(obj_func=obj_func, vector=position)
            else:
                self.__position = Position(
                    obj_func=obj_func, vector=get_position_vector(obj_func=obj_func)
                )

        # Set personal best position and social best position.
        self.__p_best_position = self.__position.copy()
        self.__social_best_pos = self.__position.copy()

        # Set initial velocity
        if velocity is not None:
            self.__velocity = velocity
        else:
            if self.__obj_func is None:
                self.__velocity = np.zeros(len(self.__position))
            else:
                self.__velocity = np.zeros(obj_func.n_dimensions)

    # --------------------------------- Getters --------------------------------

    @property
    def position(self) -> Position:
        """Returns the position as a :class:`Position` object."""
        return self.__position

    @property
    def p_best_position(self) -> Position:
        """Returns the personal best position as a :class:`Position` object."""
        return self.__p_best_position

    @property
    def social_best_pos(self) -> Position:
        """Returns the social or neighbourhood best position as a :class:`Position` object."""
        return self.__social_best_pos

    @property
    def velocity(self) -> np.ndarray:
        """Returns the current velocity as a Numpy array."""
        return self.__velocity

    @property
    def obj_func(self) -> ObjectiveFunction:
        """Returns the :class:`ObjectiveFunction` this :class:`Particle` will be optimizing."""
        return self.__obj_func

    # --------------------------------- Setters --------------------------------

    @position.setter
    def position(self, position):
        """Set's the :class:`Individual`'s ``position``."""
        if not self.frozen:
            self.__position = Position(obj_func=self.__obj_func, vector=position)

    @p_best_position.setter
    def p_best_position(self, position):
        """Set's the :class:`Individual`'s personal best position."""
        if not self.frozen:
            self.__p_best_position = Position(obj_func=self.__obj_func, vector=position)

    @social_best_pos.setter
    def social_best_pos(self, position):
        """Set's the :class:`Individual`'s social or neighbourhood best position."""
        if not self.frozen:
            self.__social_best_pos = Position(obj_func=self.__obj_func, vector=position)

    @velocity.setter
    def velocity(self, velocity):
        """Set's the :class:`Individual`'s velocity."""
        if not self.frozen:
            self.__velocity = np.array(velocity)

    @obj_func.setter
    def obj_func(self, obj_func):
        """Set's the :class:`Individual`'s :class:`ObjectiveFunction`."""
        self.__obj_func = obj_func

    # --------------------------------- Methods --------------------------------

    def reinit_uniform_position(self):
        """Reinitializes the :class:`Particle`'s position uniformly within the bounds of the search space.'"""
        self.position.vector = get_position_vector(obj_func=self.obj_func)

    def evaluate(self):
        """Evaluates the :class:`Particle`'s position."""
        self.__position.evaluate()

    def satisfies_constraints(self) -> bool:
        """
        Checks whether the :class:`~cify.si.pso.particle.Particle` satisfies the constraints
        of the passed :class:`~cify.core.obj_func.ObjectiveFunction`.
        """
        return self.obj_func.satisfies_constraints(self.position.vector)

    def copy(self):
        """Creates and returns a copy of the :class:`~cify.si.pso.particle.Particle` object.

        :return: A copy of the original particle object.
        :rtype: :class:`~cify.si.pso.particle.Particle`
        """
        duplicate = Particle(
            position=self.__position.copy(),
            velocity=self.__velocity.copy(),
            obj_func=self.__obj_func,
        )
        return duplicate

    # ----------------------------- Special Methods ----------------------------

    def __str__(self) -> str:
        """Returns a str representation of the :class:`Particle`."""
        return f"position: {self.position}\n" \
               f"velocity: {self.velocity}\n" \
               f"p_best_position: {self.p_best_position}\n" \
               f"obj_func: {self.obj_func}\n"

    def __eq__(self, other) -> bool:
        if isinstance(other, Particle):
            return self.position == other.__position \
                   and np.array_equal(self.__velocity, other.__velocity) \
                   and self.obj_func == other.__obj_func
        else:
            return False

    def __lt__(self, other) -> bool:
        if self.__position.value is None:
            return False
        elif other.__position.value is None:
            return True
        return self.__position.value < other.__position.value

    def __le__(self, other) -> bool:
        if self.__position.value is None:
            return False
        elif other.__position.value is None:
            return True
        return self.__position.value <= other.__position.value

    def __gt__(self, other) -> bool:
        if self.__position.value is None:
            return False
        elif other.__position.value is None:
            return True
        return self.__position.value > other.__position.value

    def __ge__(self, other) -> bool:
        if self.__position.value is None:
            return False
        elif other.__position.value is None:
            return True
        return self.__position.value >= other.__position.value
