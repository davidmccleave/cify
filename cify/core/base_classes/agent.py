import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from cify.core.position import Position

__all__ = ['Agent']
fields = ['vector', 'value', 'p_best_vector', 'p_best_value',
          'social_best_vector', 'social_best_value', 'frozen', 'name']


class Agent(ABC, object):
    """
    Agents are the individual elements in :class:`~cify.core.base_classes.Collection`
    objects. Any object can be an :class:`Agent` simply by using :class:`Agent` as a base class.
    There are three methods that must be implemented by any :class:`Agent` class:

    * `position(self)`
    * `p_best_position(self)`
    * `social_best_pos(self)`

    These methods define how the :class:`Agent` will behave when used with general components
    such as topologies or evolutionary operators. A number of classes provided by CIFY
    use :class:`Agent` as a base class, most notably :class:`~cify.si.pso.particle.Particle`
    and :class:`~cify.ec.individual.Individual`.

    .. warning::
       Not returning :class:`Position` objects from these three methods will result in errors in the supplied
       algorithms.
    """

    def __init__(self, name: str = None, **kwargs):
        """
        :param name: An optional name for the :class:`Agent`.
        :type name: str, optional
        """
        if 'frozen' in kwargs:
            self.__frozen = kwargs.get('frozen')
            del kwargs['frozen']
        else:
            self.__frozen = False
        self.__name = name
        self.__dict__.update(kwargs)

    # --------------------------------- Getters --------------------------------

    @property
    def vector(self) -> np.ndarray:
        """The vector of the :class:`Agent`'s `position`."""
        return self.position.vector

    @property
    def value(self) -> float:
        """The value of the :class:`Agent`'s `position`."""
        return self.position.value

    @property
    @abstractmethod
    def position(self) -> Position:
        """
        The :class:`Position` at which the :class:`Agent` sits in the search space.
        For use cases where this naming is not appropriate, make this
        method return the new property. This method must always return
        a :class:`Position` object.

        :return: The :class:`Position` at which the :class:`Agent` sits in the search space.
        :rtype: :class:`Position`
        """
        pass

    @property
    @abstractmethod
    def p_best_position(self) -> Position:
        """
        The personal best :class:`Position` found by this :class:`Agent`.

        :return: The :class:`Agent`'s personal best :class:`Position`.
        :rtype: :class:`Position`
        """
        pass

    @property
    @abstractmethod
    def social_best_pos(self) -> Position:
        """
        The neighbourhood or social best :class:`Position` found by this :class:`Agent`.
        When topologies are used that share best positions found between all :class:`Agent`'s,
        this field is equivalent to the global optimum.

        :return: The :class:`Agent`'s neighbourhood best :class:`Position`.
        :rtype: :class:`Position`
        """
        pass

    @property
    def name(self) -> str:
        """
        :return: The :class:`Agent`'s name
        :rtype: str
        """
        return self.__name

    @property
    def frozen(self) -> bool:
        """
        Returns a boolean representing whether the :class:`Agent` is frozen. When an :class:`Agent` is
        frozen, they do not update any of their parameters or components. An example,
        of where this functionality is useful would be when detecting changes in a dynamic objective
        function search space using sentries.

        :return: Whether the :class:`Agent` is frozen or not.
        :rtype: bool
        """
        return self.__frozen

    # --------------------------------- Setters --------------------------------

    @position.setter
    def position(self, position):
        """Sets the :class:`Agent`'s :class:`Position`."""
        self.position = position

    @p_best_position.setter
    def p_best_position(self, position):
        """Sets the :class:`Agent`'s personal best :class:`Position`."""
        self.p_best_position = position

    @social_best_pos.setter
    def social_best_pos(self, position):
        """Sets the :class:`Agent`'s social or neighbourhood best :class:`Position`."""
        self.social_best_pos = position

    @name.setter
    def name(self, name):
        """Sets the :class:`Agent`'s name."""
        self.__name = name

    def freeze(self):
        """Freezes the :class:`Agent`."""
        self.__frozen = True

    def unfreeze(self):
        """Instantaneously defrosts the :class:`Agent`."""
        self.__frozen = False

    # --------------------------------- Methods --------------------------------

    def to_series(self) -> pd.Series:
        """
        Converts the current values of all the :class:`Agent`'s fields into a Pandas :class:`Series`.

        :return: A Pandas :class:`Series`.
        :rtype: Pandas :class:`Series`
        """
        return pd.Series([
            self.vector, self.value,
            self.p_best_position.vector, self.p_best_position.value,
            self.social_best_pos.vector, self.social_best_pos.value,
            self.frozen, self.name
        ], fields)

    # ----------------------------- Special Methods ----------------------------

    def __str__(self) -> str:
        """Returns a string representation of the :class:`Agent`."""
        return self.to_series().str
