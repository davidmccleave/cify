import numpy as np
from cify.si.pso.particle import Particle
from cify.core.utils import get_objective_function
from cify.core.position import Position
from cify.core.objective_function import ObjectiveFunction


def test_init():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    p1 = Particle([1, 1, 1], obj_func=obj_func)
    p2 = Particle(p1, velocity=[.5, .5, .5], obj_func=obj_func)
    p3 = Particle(Position(vector=[3, 3, 3], obj_func=obj_func), obj_func=obj_func)
    p4 = Particle(obj_func=obj_func)
    assert all(x == 1 for x in p1.position.vector)
    assert all(x == 1 for x in p2.position.vector)
    assert all(x == 3 for x in p3.position.vector)
    assert p4.satisfies_constraints()


def test_property_calls():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    particle = Particle([1, 1, 1], obj_func=obj_func)
    assert type(particle.position) == Position
    assert type(particle.p_best_position) == Position
    assert type(particle.social_best_pos) == Position
    assert all(x == 0. for x in particle.velocity)
    assert type(particle.obj_func) == ObjectiveFunction


def test_property_setters():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    particle = Particle([1, 1, 1], obj_func=obj_func)
    particle.position = [2, 2, 2]
    assert all(x == 2 for x in particle.position.vector)
    particle.p_best_position = [4, 4, 4]
    assert all(x == 4 for x in particle.p_best_position.vector)
    particle.social_best_pos = [6, 6, 6]
    assert all(x == 6 for x in particle.social_best_pos.vector)
    particle.velocity = [7, 7, 7]
    assert all(x == 7 for x in particle.velocity)
    new_obj_func = get_objective_function('schwefel', n_dimensions=3)
    particle.obj_func = new_obj_func
    assert particle.obj_func == new_obj_func


def test_evaluate():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    particle = Particle([1., 1., 1.], obj_func=obj_func)
    particle.evaluate()
    assert particle.position.value == 1.


def test_copy():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    p1 = Particle([1., 1., 1.], obj_func=obj_func)
    p2 = p1.copy()
    assert p1.position == p2.position
    assert all(x == y for x, y in zip(p1.velocity, p2.velocity))
    assert p1.obj_func == p1.obj_func


def test_str():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    particle = Particle([1., 1., 1.], obj_func=obj_func)
    assert type(str(particle)) == str


def test_equality():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    p1 = Particle([1., 1., 1.], obj_func=obj_func)
    p2 = p1.copy()
    assert p1 == p2


def test_comparison_operators():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    p1 = Particle([1., 1., 1.], obj_func=obj_func)
    p2 = Particle([8., 8., 8.], obj_func=obj_func)
    assert p1 < p2
    assert p1 <= p2
    assert p2 > p1
    assert p2 >= p1
