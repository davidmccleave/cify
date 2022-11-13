import time
from typing import List

from cify.core.objective_function import ObjectiveFunction
from cify.core.base_classes.algorithm import Algorithm
from cify.core.task import Task

__all__ = ['Runner']


class Runner(object):
    """
    The :class:`Runner` class is used to create a list of :class:`Task` s to be run in sequential order.
    :class:`Task` s can be manually created and added or removed from the :class:`Runner` using the
    ``add`` and ``remove`` methods, however, it is not necessary to manually create :class:`Task` s.
    :class:`Algorithm` s and :class:`ObjectiveFunction`'s can be added to or removed from the :class:`Runner`
    using the ``add`` and ``remove`` methods from which the :class:`Runner` will create :class:`Task` s when
    its ``compile`` method is called.
    """

    def __init__(self, tasks: List[Task] = None, name: str = None, log: bool = False):
        """
        :param tasks: The :class:`Task` s to be executed by this :class:`Runner`.
        :type tasks: list of :class:`Task` objects, optional
        :param name: An optional name for the :class:`Runner`, defaults to a unique integer returned by ``id(self)``
        :type name: str, optional
        :param log: Whether to output a log at the end of each iteration, defaults to False.
        :type log: bool, optional
        """
        self.__algorithm_pool = list()
        self.__objective_function_pool = list()
        if tasks is None:
            self.__tasks = list()
            self.__original_tasks = list()
        else:
            self.__tasks = tasks
            self.__original_tasks = self.__tasks.copy()
        if name:
            self.name = name
        else:
            self.name = id(self)
        self.log = log
        self.__results = list()
        self.__compiled = False
        self.total_running_time = None

    # --------------------------------- Getters --------------------------------

    @property
    def algorithm_pool(self) -> list:
        """Returns a list representing the :class:`Algorithm` pool."""
        return self.__algorithm_pool

    @property
    def objective_function_pool(self) -> list:
        """Returns a list representing the :class:`ObjectiveFunction` pool."""
        return self.__objective_function_pool

    @property
    def tasks(self) -> list:
        """Returns the list of :class:`Task` s."""
        return self.__tasks

    @property
    def results(self) -> list:
        """Returns all results calculated by the `Runner`."""
        return self.__results

    # --------------------------------- Methods --------------------------------

    def add(self, item):
        """
        Adds a :class:`Task`, :class:`Algorithm` or :class:`ObjectiveFunction` to the pool.
        Use the ``compile`` method to compile a list of :class:`Task` s from the pool.

        :param item: The item to be added.
        :type item: :class:`Algorithm`, :class:`Task` or :class:`ObjectiveFunction`

        """
        if isinstance(item, Algorithm):
            self.algorithm_pool.append(item)
        elif isinstance(item, ObjectiveFunction):
            self.objective_function_pool.append(item)
        elif isinstance(item, Task):
            self.tasks.append(item)
        else:
            return TypeError(f'Expected Algorithm, ObjectiveFunction or Task, got {type(item)} instead.')

    def remove(self, item):
        """
        Removes a :class:`Task`, :class:`Algorithm` or :class:`ObjectiveFunction` from the pool.
        Use the ``compile`` method to compile a list of :class:`Task` s from the pool.

        :param item: The item to be removed.
        :type item: :class:`Algorithm`, :class:`Task` or :class:`ObjectiveFunction`
        """
        if isinstance(item, Algorithm):
            self.algorithm_pool.remove(item)
        elif isinstance(item, ObjectiveFunction):
            self.objective_function_pool.remove(item)
        elif isinstance(item, Task):
            self.tasks.remove(item)
        else:
            raise TypeError(f'Expected Algorithm, ObjectiveFunction or Task, got {type(item)} instead.')

    def compile(self, n_independent_runs=1, n_iterations=1, n_evaluations=0, stopping_condition=None,
                relationship='many-to-many'):
        """
        This is where all the conditions passed to ``__init__`` and ``compile`` are transformed into a list of
        :class:`Task` s that will be run when the user calls ``execute``. :class:`Task` s already in the `tasks` list
        remain unchanged. For more complex :class:`Task` s, It is recommended that :class:`Task` s are manually created
        and appended to the `tasks` list of the :class:`Runner` instance. The conditions passed to this function
        apply to all tasks created from the ``algorithm_pool`` and ``objective_function_pool``.

        There are four relationship types: ``one-to-one``, ``one-to-many``, ``many-to-one`` and ``many-to-many``.
        Each relationship type represents tasks are created when relating the :class:`Algorithm` s in the
        ``algorithm_pool`` and the :class:`ObjectiveFunction` s in the ``objective_function_pool``.

        :param n_independent_runs: The number of independent runs to perform for each :class:`Task`, defaults to one.
        :type n_independent_runs: int, optional
        :param n_iterations: The number of iterations to perform for each :class:`Task`, defaults to one.
        :type n_iterations: int, optional but highly recommended
        :param n_evaluations: The number of evaluations to terminate at for each :class:`Task`.
        :type n_evaluations: int, optional
        :param stopping_condition: A stopping condition to apply to all :class:`Task` s.
        :type stopping_condition: bool or callable that returns a bool, optional
        :param relationship: A string representing which cardinality to use when creating :class:`Task` s,
                             defaults to ``many-to-many``.
        :type relationship: string, optional
        """
        if self.__compiled:
            self.__tasks = self.__original_tasks.copy()
        else:
            self.__compiled = True

        # Multiply current tasks by n_independent_runs.
        curr_tasks = self.__tasks.copy()
        self.__tasks = list()
        for task in curr_tasks:
            for _ in range(n_independent_runs):
                self.__tasks.append(task)

        #  Append tasks from pools.
        if relationship == 'one-to-one':
            for algo, obj_func in zip(self.algorithm_pool, self.objective_function_pool):
                for _ in range(n_independent_runs):
                    self.tasks.append(Task(algo, obj_func, n_iterations, n_evaluations, stopping_condition))
        elif relationship == 'one-to-many' or relationship == 'many-to-many':
            for algo in self.algorithm_pool:
                for obj_func in self.objective_function_pool:
                    for _ in range(n_independent_runs):
                        self.tasks.append(Task(algo, obj_func, n_iterations, n_evaluations, stopping_condition))
        elif relationship == 'many-to-one':
            for obj_func in self.objective_function_pool:
                for algo in self.algorithm_pool:
                    for _ in range(n_independent_runs):
                        self.tasks.append(Task(algo, obj_func, n_iterations, n_evaluations, stopping_condition))
        else:
            raise TypeError(f'Provide a valid relationship (one-to-one, one-to-many, many-to-one, many-to-many). '
                            f'Got "{relationship}"')

    def summary(self) -> str:
        """
        Returns a string formatted summary of the :class:`Runner` s :class:`Task` s to be executed.

        :rtype: str
        """
        if self.__compiled is False:
            return f'Runner ({self.name}) still needs to be compiled. Try calling compile().'
        if len(self.tasks) == 0:
            return f'No tasks have been added to Runner ({self.name})'
        rstr = \
            '================================================================================\n' \
            f'                          Runner Summary ({self.name})                         \n' + \
            '================================================================================\n' \
            '{:<35}{:<35}{:<10}\n'.format('Algorithm', 'ObjectiveFunction', 'Type') + \
            '--------------------------------------------------------------------------------\n'
        for idx, task in enumerate(self.tasks):
            rstr += '{:<5}{:<75}\n'.format((idx+1), str(task))
        return rstr + '--------------------------------------------------------------------------------\n'

    def __str__(self) -> str:
        return self.summary()

    def execute(self):
        """
        Executes the :class:`Task` s in the :class:`Runner` s internal `tasks` list.
        If you have added :class:`Algorithm` s and :class:`ObjectiveFunction` s to this :class:`Runner` using the
        ``add`` method, you should compile the :class:`Runner` first.
        """
        print(f'----- Beginning Runner {self.name} -----')
        start_time = time.time()
        for task in self.tasks:
            task.execute()
            self.results.append(task.get_statistics())
        self.total_running_time = time.time() - start_time
        print(f'Runner {self.name} complete!')
