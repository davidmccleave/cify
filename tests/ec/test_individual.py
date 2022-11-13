import numpy as np
from cify.ec.individual import Individual
from cify.core.utils import get_objective_function
from cify.core.position import Position
from cify.core.objective_function import ObjectiveFunction


def test_init():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual1 = Individual([1, 1, 1], obj_func=obj_func)
    individual2 = Individual(individual1, obj_func=obj_func)
    individual3 = Individual(Position(vector=[3, 3, 3], obj_func=obj_func), obj_func=obj_func)
    individual4 = Individual(obj_func=obj_func)
    assert all(x == 1 for x in individual1.chromosome.vector)
    assert all(x == 1 for x in individual2.chromosome.vector)
    assert all(x == 3 for x in individual3.chromosome.vector)
    assert individual4.satisfies_constraints()


def test_property_calls():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual = Individual([1, 1, 1], obj_func=obj_func)
    assert type(individual.position) == Position
    assert type(individual.chromosome) == Position
    assert type(individual.p_best_chromosome) == Position
    assert type(individual.p_best_position) == Position
    assert type(individual.social_best_pos) == Position
    assert type(individual.social_best_chromosome) == Position
    assert type(individual.obj_func) == ObjectiveFunction


def test_property_setters():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual = Individual([1, 1, 1], obj_func=obj_func)
    individual.position = [2, 2, 2]
    assert all(x == 2 for x in individual.position.vector)
    individual.chromosome = [3, 3, 3]
    assert all(x == 3 for x in individual.chromosome.vector)
    individual.p_best_position = [4, 4, 4]
    assert all(x == 4 for x in individual.p_best_position.vector)
    individual.p_best_chromosome = [5, 5, 5]
    assert all(x == 5 for x in individual.p_best_chromosome.vector)
    individual.social_best_pos = [6, 6, 6]
    assert all(x == 6 for x in individual.social_best_pos.vector)
    individual.social_best_chromosome = [7, 7, 7]
    assert all(x == 7 for x in individual.social_best_chromosome.vector)
    new_obj_func = get_objective_function('schwefel', n_dimensions=3)
    individual.obj_func = new_obj_func
    assert individual.obj_func == new_obj_func


def test_evaluate():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual = Individual([1., 1., 1.], obj_func=obj_func)
    individual.evaluate()
    assert individual.chromosome.value == 1.


def test_copy():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual1 = Individual([1., 1., 1.], obj_func=obj_func)
    individual2 = individual1.copy()
    assert individual2.obj_func == individual1.obj_func
    assert individual2.chromosome == individual1.chromosome


def test_str():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual = Individual([1., 1., 1.], obj_func=obj_func)
    assert type(str(individual)) == str


def test_equality():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual1 = Individual([1., 1., 1.], obj_func=obj_func)
    individual2 = individual1.copy()
    assert individual1 == individual2


def test_comparison_operators():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    individual1 = Individual([1., 1., 1.], obj_func=obj_func)
    individual2 = Individual([8., 8., 8.], obj_func=obj_func)
    assert individual1 < individual2
    assert individual1 <= individual2
    assert individual2 > individual1
    assert individual2 >= individual1
