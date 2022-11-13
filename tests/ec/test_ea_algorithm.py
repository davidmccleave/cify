from cify.ec.ea.algorithm import EA
from cify.core.utils import get_objective_function
from cify.ec.utils import get_population
from cify.ec.operators.crossover import *
from cify.ec.operators.selection import *


def test_ea():
    obj_func = get_objective_function('mean-dimensions')
    EA(obj_func=obj_func)
    EA(obj_func=obj_func, n_individuals=35)
    algo = EA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)])
    algo.execute(10, 10000, lambda: True)


def test_npoint_crossover_on_ea():
    obj_func = get_objective_function('mean-dimensions')
    algo = EA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=npoint_crossover,
              selection_operator=elitism_selection)
    algo.execute(1)


def test_one_point_crossover_on_ea():
    obj_func = get_objective_function('mean-dimensions')
    algo = EA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=one_point_crossover,
              selection_operator=tournament_selection)
    algo.execute(1)


def test_two_point_crossover_on_ea():
    obj_func = get_objective_function('mean-dimensions')
    algo = EA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=two_point_crossover)
    algo.execute(1)


def test_hillclimbing_crossover_on_ea():
    obj_func = get_objective_function('mean-dimensions')
    algo = EA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=hillclimbing_crossover)
    algo.execute(1)


def test_linear_crossover_on_ea():
    obj_func = get_objective_function('mean-dimensions')
    algo = EA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=linear_crossover)
    algo.execute(1)
