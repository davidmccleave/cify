import numpy as np

import cify
from cify.core.objective_function import ObjectiveFunction
from cify.core.position import Position
from cify.core.utils import get_objective_function


def test_init_behavior():
    obj_func = get_objective_function('schwefel1', n_dimensions=5)
    pos = Position([0, 0, 0, 0, 0], obj_func)

    assert type(pos.obj_func) == ObjectiveFunction
    assert type(pos.vector) == np.ndarray
    assert np.array_equal(pos.vector, np.array([0, 0, 0, 0, 0]))
    assert pos.value == float(0.0)


def test_vector_changes():
    pos = Position([0, 0, 0, 0, 0])
    assert all(pos.vector == np.array([0, 0, 0, 0, 0]))

    pos.vector = [1, 2, 3, 4, 5]
    assert all(pos.vector == np.array([1, 2, 3, 4, 5]))


def test_obj_func_changes():
    schwefel = get_objective_function('schwefel1', n_dimensions=5)
    rosenbrock = get_objective_function('rosenbrock', n_dimensions=5)
    pos = Position([0, 0, 0, 0, 0], schwefel)

    assert pos.obj_func == schwefel
    pos.obj_func = rosenbrock
    assert pos.obj_func == rosenbrock


def test_copy():
    pos = Position([0, 0, 0, 0, 0])
    copy = pos.copy()

    assert all(x == y for x,y in zip(pos.vector, copy.vector))
    assert copy == pos


def test_equality():
    pos = Position([1, 2, 3, 4, 5])
    same_pos = pos

    assert pos == Position([1, 2, 3, 4, 5])
    assert same_pos == pos


def test_valid_comparisons():
    obj_func = get_objective_function('schwefel1', n_dimensions=5)
    pos1 = Position([1, 1, 1, 1, 1], obj_func)
    pos2 = Position([8, 8, 8, 8, 8], obj_func)
    assert pos1 < pos2
    assert pos1 <= pos2
    pos2.vector = [0, 0, 0, 0, 0]
    assert pos1 > pos2
    assert pos1 >= pos2


def test_invalid_comparisons():
    obj_func = get_objective_function('schwefel1', n_dimensions=5)
    pos1 = Position([1, 1, 1, 1, 1], obj_func)
    pos2 = Position([8, 8, 8, 8, 8])
    assert not pos1 < pos2
    assert not pos1 <= pos2
    assert pos1 > pos2
    assert pos1 >= pos2


# Mathematical Operations

def test_addition():
    pos1 = Position([1, 1, 1, 1, 1])
    pos2 = Position([2, 2, 2, 2, 2])
    pos3 = pos1 + pos2
    assert np.array_equal(pos3.vector, np.array([3, 3, 3, 3, 3]))
    assert type(pos3) == Position
    arr = pos1 + [2, 2, 2, 2, 2]
    assert all(arr.vector == 3)


def test_subtraction():
    pos1 = Position([1, 1, 1, 1, 1])
    pos2 = Position([2, 2, 2, 2, 2])
    pos3 = pos1 - pos2
    assert np.array_equal(pos3.vector, np.array([-1, -1, -1, -1, -1]))
    assert type(pos3) == Position
    arr = pos1 - [2, 2, 2, 2, 2]
    assert all(arr.vector == -1)


def test_multiplication():
    pos1 = Position([2, 2, 2, 2, 2])
    pos2 = Position([3, 3, 3, 3, 3])
    pos3 = pos1 * pos2
    assert np.array_equal(pos3.vector, np.array([6, 6, 6, 6, 6]))
    assert type(pos3) == Position
    arr = pos1 * [3, 3, 3, 3, 3]
    assert all(arr.vector == 6)


def test_true_division():
    pos1 = Position([8, 8, 8, 8, 8])
    pos2 = Position([4, 4, 4, 4, 4])
    pos3 = pos1 / pos2
    assert np.array_equal(pos3.vector, np.array([2, 2, 2, 2, 2]))
    assert type(pos3) == Position
    arr = pos1 / [4, 4, 4, 4, 4]
    assert all(arr.vector == 2)


def test_floor_division():
    pos1 = Position([8, 8, 8, 8, 8])
    pos2 = Position([4, 4, 4, 4, 4])
    pos3 = pos1 // pos2
    assert np.array_equal(pos3.vector, np.array([2, 2, 2, 2, 2]))
    assert type(pos3) == Position
    arr = pos1 // [4, 4, 4, 4, 4]
    assert all(arr.vector == 2)


def test_length():
    pos = Position([1, 1, 1, 1, 1])
    assert len(pos) == 5


def test_iter_over_vector():
    pos = Position([1, 2, 3, 4, 5])
    iter_list = iter(pos)
    assert next(iter_list) == 1
    assert next(iter_list) == 2
    assert next(iter_list) == 3
    assert next(iter_list) == 4
    assert next(iter_list) == 5


def test_set_and_get_item_from_vector():
    pos = Position([1., 2., 3., 4., 5.])
    assert pos[0] == 1.
    pos[0] = 42.5
    assert pos[0] == 42.5

