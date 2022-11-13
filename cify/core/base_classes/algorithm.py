import numpy as np
import pandas as pd
from tqdm import tqdm
from abc import ABC, abstractmethod
from typing import List
from cify.core.objective_function import ObjectiveFunction
from cify.core.base_classes.collection import Collection
from cify.core.position import Position

__all__ = ['Algorithm']


class Algorithm(ABC):
    """
    The :class:`Algorithm` class is a base class used by all implemented algorithms.
    The class handles iterating, statistics and handling of fields used by all algorithms.
    This base class is used when implementing novel algorithms not supplied by CIFY, whilst
    maintaining integration with all the other CIFY components.
    """

    def __init__(self, obj_func: ObjectiveFunction, global_optimum_pos: Position = None, name: str = None, **kwargs):
        """
        :param obj_func: The :class:`ObjectiveFunction` this :class:`Algorithm` will be optimizing.
        :type obj_func: :class:`ObjectiveFunction`
        :param global_optimum_pos: The currently found global optimum. This parameter would usually not be set on init.
        :type global_optimum_pos: :class:`Position`, optional
        :param name: An optional name for the :class:`Algorithm`.
        :type name: str, optional
        """
        self.obj_func = obj_func
        if name is not None:
            self.name = name
        else:
            self.name = self.__class__.__name__
        self.iteration = 0
        self.n_evaluations = 0

        # Set up statistics
        self.stats_columns = ['iteration', 'best', 'worst', 'mean', 'stdev', 'global_optimum', 'n_evaluations']
        self.statistics = pd.DataFrame(columns=self.stats_columns)
        self.statistics.set_index('iteration', inplace=True)
        self.global_optimum_pos = global_optimum_pos  # the best Position found so far.

        self.__dict__.update(kwargs)

        if 'store_agents' in kwargs:
            if kwargs['store_agents']:
                self.agents = []
            else:
                self.store_agents = False
        else:
            self.store_agents = False

    @abstractmethod
    def do_iteration(self):
        """
        The only function that must be overridden when implementing your own algorithm.
        This function must be the logic of one iteration of your algorithm and must
        return a list of the collections used by your algorithm so that statistics
        can be calculated. It is important that this method returns a list of the
        :class:`Collection`'s used by the algorithm at the end of the iteration. These will be
        used to update the statistics.

        :return: A list of :class:`~cify.Collection` s.
        """
        pass

    # --------------------------------- Methods --------------------------------

    def execute(self, n_iterations=1, n_evaluations=0, stopping_condition=None, log=False):
        """
        A wrapper of the ``Algorithm.iterate()`` method.
        """
        self.iterate(n_iterations, n_evaluations, stopping_condition, log=log)

    def iterate(self, n_iterations=1, n_evaluations=0, stopping_condition=None, log=False):
        """
        Iterate the :class:`Algorithm`.

        :param n_iterations: The number of iterations to perform, defaults to 1.
        :type n_iterations: int, optional
        :param n_evaluations: The number of evaluations to perform. If no value is set, the number of evaluations
               will not be used as a stopping criterion.
        :type n_evaluations: int, optional
        :param stopping_condition: A callable that returns a boolean that determines when to terminate iterating over
               the algorithm. If a stopping condition is provided, it will override the n_iterations parameter.
        :type stopping_condition: callable, optional
        :param log: Whether to print to the console after completing each iteration.
        :type log: bool, optional
        """
        internal_iteration_count = 0

        if stopping_condition is None and n_evaluations == 0:
            for _ in tqdm(range(n_iterations)):
                internal_iteration_count += 1
                self.iteration += 1
                iteration_evaluations = self.obj_func.get_n_evaluations()
                self.n_evaluations += iteration_evaluations
                self.__set_statistics(self.do_iteration(), iteration_evaluations, log=log)
                self.obj_func.increment()

        def __conditions():
            if stopping_condition is not None:
                if n_evaluations != 0:
                    if n_iterations != 1:
                        return internal_iteration_count < n_iterations \
                               and self.n_evaluations < n_evaluations \
                               and stopping_condition() is not False
                    return self.n_evaluations < n_evaluations and stopping_condition() is not False
                return stopping_condition() is not False
            elif n_evaluations != 0:
                if n_iterations != 1:
                    return internal_iteration_count < n_iterations and self.n_evaluations < n_evaluations
                return self.n_evaluations < n_evaluations
            return internal_iteration_count < n_iterations

        while __conditions():
            internal_iteration_count += 1
            self.iteration += 1
            iteration_evaluations = self.obj_func.get_n_evaluations()
            self.n_evaluations += iteration_evaluations
            self.__set_statistics(self.do_iteration(), iteration_evaluations, log=log)
            self.obj_func.increment()

    def __set_statistics(self, collections: List[Collection], itr_evals, log=False):
        """This is an internal method used by ``iterate`` that sets the statistics at the end of an iteration."""
        if self.store_agents:
            self.agents.append(collections)

        best = collections[0][0].value
        worst = collections[0][0].value
        all_values = []

        # Set best and worst positions for the iteration.
        for collection in collections:
            for agent in collection:
                all_values.append(agent.value)
                if self.obj_func.cmp(agent.value, best):
                    best = agent.value
                if self.obj_func.cmp(worst, agent.value):
                    worst = agent.value
                if self.obj_func.cmp(agent.value, self.global_optimum_pos.value):
                    self.global_optimum_pos = agent.position

        mean, stdev = np.mean(np.array(all_values)), np.std(np.array(all_values))

        data_list = [self.iteration, best, worst, mean, stdev, self.global_optimum_pos.value, itr_evals]
        for i in range(len(data_list), len(self.stats_columns)):
            try:
                data_list.append(self.__dict__[self.stats_columns[i]])
            except Exception:
                raise TypeError('Could not append an additional statistics column.')

        curr_stats = pd.DataFrame([data_list], columns=self.stats_columns)
        curr_stats.set_index('iteration', inplace=True)
        if log:
            print(f'Completed iteration: {self.iteration}\t(global optimum: {round(self.global_optimum_pos.value, 4)})',
                  end='\x1b[2K\r')
        self.statistics = pd.concat([self.statistics, curr_stats])

    def add_stats_columns(self, columns: list or str):
        """
        Appends the passed column or columns to the :class:`Algorithm`'s ``statistics`` field to enable tracking
        for this value. The names passed must be valid attributes of the :class:`Algorithm`.

        :raises TypeError: if the wrong values are passed in columns.

        :param columns: The names of the attributes to track.
        :type columns: str of list of strs.
        """
        if isinstance(columns, list):
            for col in columns:
                self.stats_columns.append(col)
        elif isinstance(columns, str):
            self.stats_columns.append(columns)
        else:
            raise TypeError(f"Expected string or list, received {type(columns)}.")

    def remove_stats_columns(self, columns: list or str):
        """
        Removes the passed column or columns from the :class:`Algorithm`'s ``statistics`` field.

        :raises TypeError: if the wrong values are passed in columns.

        :param columns: The names of the attributes to remove.
        :type columns: str of list of strs.
        """
        if isinstance(columns, list):
            for col in columns:
                self.stats_columns.remove(col)
        elif isinstance(columns, str):
            self.stats_columns.remove(columns)
        else:
            raise TypeError(f"Expected string or list, received {type(columns)}.")

    # ----------------------------- Special Methods ----------------------------

    def __next__(self):
        """
        Performs a single iteration of the algorithm and yields the statistics of the algorithm
        after this iteration as a Pandas DataFrame containing one row.

        :return: The statistics at the end of one iteration.
        :rtype: A generator object
        """
        self.iterate()
        yield self.statistics.iloc(self.iteration - 1)

    def __str__(self) -> str:
        """Returns a string representation of the :class:`Algorithm`."""
        string = ''
        for item in self.__dict__:
            string += item.__str__()
        return string
