import pandas as pd
from cify.core.base_classes.algorithm import Algorithm
from cify.core.objective_function import ObjectiveFunction
import time

__all__ = ['Task']


class Task(object):
    """
    Defines a :class:`Task` to be executed standalone or by a :class:`Runner`.
    """
    def __init__(self,
                 algorithm: Algorithm,
                 obj_func: ObjectiveFunction,
                 n_iterations: int = 1,
                 n_evaluations: int = None,
                 stopping_condition: callable or bool = None,
                 executables: list = None,
                 name=None,
                 log=False
                 ):
        """
        :param algorithm: The :class:`Algorithm` that will be used to optimize the given :class:`ObjectiveFunction`.
        :param obj_func: The :class:`ObjectiveFunction` to be optimized.
        :type obj_func: :class:`ObjectiveFunction`.
        :param n_iterations: The number of iterations to perform.
        :type n_iterations: int, optional
        :param n_evaluations: The number of total evaluations at which the search will terminate.
        :type n_evaluations: int, optional
        :param stopping_condition: A stopping condition to apply to the :class:`Algorithm`'s search.
        :type stopping_condition: bool or callable that returns a bool.
        :param executables: Any executables that can be executed using Python's ``exec`` method.
                            Executables are executed after completion of the optimization process.
        :type executables: list containing strs or code blocks.
        """
        self.algorithm = algorithm
        self.obj_func = obj_func
        self.algorithm.obj_func = self.obj_func
        self.n_iterations = n_iterations

        if n_evaluations is None:
            self.n_evaluations = 0
        else:
            self.n_evaluations = n_evaluations

        self.stopping_condition = stopping_condition

        if executables is None:
            self.executables = list()
        else:
            self.executables = executables

        if name is None:
            self.name = id(self)
        else:
            self.name = name
        self.log = log
        self.total_running_time = None

    # --------------------------------- Methods --------------------------------

    def get_statistics(self) -> pd.DataFrame:
        """Returns the :class:`Algorithm` s statistics."""
        return self.algorithm.statistics

    def add_executable(self, executable):
        """Appends an executable to the :class:`Task` s list of executables."""
        self.executables.append(executable)

    def execute(self, log=False):
        """
        Begins execution of the :class:`Runner`.
        :return: a tuple of the form, ``(total running time, algorithm.statistics)``.
        """
        self.log = log
        if self.log:
            print(f'----- Beginning Task {self.name} -----')
        start_time = time.time()
        self.algorithm.iterate(n_iterations=self.n_iterations,
                               n_evaluations=self.n_evaluations,
                               stopping_condition=self.stopping_condition,
                               log=self.log)
        if self.log:
            print(f'Completed algorithm iterations. ({time.time() - start_time}s elapsed)')
        if self.executables:
            for executable in self.executables:
                exec(executable)

        self.total_running_time = time.time() - start_time
        print(f'Task {self.name} complete!')
        return self.total_running_time, self.get_statistics()

    def __str__(self) -> str:
        return '{:<30}{:<35}{:<10}'.format(self.algorithm.name, self.obj_func.name, self.obj_func.optimization.verb())
