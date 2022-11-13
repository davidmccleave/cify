from cify.ec.ga.algorithm import GA
from cify.core.utils import get_objective_function
from cify.ec.utils import get_population
from cify.ec.operators.crossover import *
from cify.ec.operators.selection import *
from cify.ec.operators.mutation import *


def test_ea():
    obj_func = get_objective_function('mean-dimensions')
    GA(obj_func=obj_func)
    GA(obj_func=obj_func, n_individuals=35)
    algo = GA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)])
    algo.execute(10, 10000, lambda: True)


def test_npoint_crossover_on_ga():
    obj_func = get_objective_function('mean-dimensions')
    algo = GA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=npoint_crossover,
              selection_operator=elitism_selection,
              mutation_operator=random_mutation)
    algo.execute(1)


def test_one_point_crossover_on_ga():
    obj_func = get_objective_function('mean-dimensions')
    algo = GA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=one_point_crossover,
              selection_operator=tournament_selection,
              mutation_operator=inorder_mutation,
              mutation_params={'range': (2, 4)})
    algo.execute(1)


def test_two_point_crossover_on_ga():
    obj_func = get_objective_function('mean-dimensions')
    algo = GA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=two_point_crossover,
              mutation_operator=headless_chicken_mutation)
    algo.execute(1)


def test_hillclimbing_crossover_on_ga():
    obj_func = get_objective_function('mean-dimensions')
    algo = GA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=hillclimbing_crossover)
    algo.execute(1)


def test_linear_crossover_on_ga():
    obj_func = get_objective_function('mean-dimensions')
    algo = GA(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              crossover_operator=linear_crossover)
    algo.execute(1)
