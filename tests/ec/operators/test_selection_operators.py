import numpy as np

from cify.core.base_classes.collection import Collection
from cify.ec.individual import Individual
from cify.core.utils import get_objective_function
from cify.ec.operators.selection import *


def test_elitism_selection():
    obj_func = get_objective_function('exponential', n_dimensions=3)
    population = Collection([Individual([2, 2, 2], obj_func),
                             Individual([1, 1, 1], obj_func),
                             Individual([0, 0, 0], obj_func)]
                            )
    assert population[0].value > population[1].value > population[2].value
    best = elitism_selection(population, n_agents=2)
    assert best[0] == population[2]
    assert best[1] == population[1]
    best = elitism_selection(population, n_agents=1)
    assert best[0] == population[2]


def test_random_selection():
    obj_func = get_objective_function('exponential', n_dimensions=3)
    population = Collection([Individual([2, 2, 2], obj_func),
                             Individual([1, 1, 1], obj_func),
                             Individual([0, 0, 0], obj_func)]
                            )
    assert len(random_selection(population)) == len(population)
    assert len(random_selection(population, n_agents=1)) == 1
    assert len(random_selection(population, n_agents=2, replace=True)) == 2


def test_tournament_selection():
    obj_func = get_objective_function('exponential', n_dimensions=3)
    population = Collection([Individual([2, 2, 2], obj_func),
                             Individual([1, 1, 1], obj_func),
                             Individual([0, 0, 0], obj_func)]
                            )
    assert tournament_selection(population, n_agents=1, t_size=3)[0] is population[2]
