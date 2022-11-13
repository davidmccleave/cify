import numpy as np

from cify.core.objective_function import ObjectiveFunction, MultiObjectiveFunction
from cify.core.optimization import Optimization
from cify.core.position import Position
from cify.core.utils import get_objective_function


def test_position_value_change_on_func_change():
    obj_func = get_objective_function('schwefel', n_dimensions=5)
    pos = Position([0, 0, 0, 0, 0], obj_func)
    first = pos.value
    obj_func.function = get_objective_function('rosenbrock', n_dimensions=5).function
    second = pos.value
    assert first != second


def test_dynamic_constraints():
    obj_func = get_objective_function('schwefel', n_dimensions=5)
    pos = Position([0, 0, 0, 0, 0], obj_func)
    obj_func.vector_constraints = [lambda vector: all(-1 < x < 1 for x in vector)]
    assert pos.satisfies_constraints()
    pos.vector = np.array([-2, -2, -2, -2, -2])
    assert not pos.satisfies_constraints()


def test_dynamic_vector_constraints():
    obj_func = get_objective_function('schwefel', n_dimensions=5)
    pos = Position([0, 0, 0, 0, 0], obj_func)
    obj_func.vector_constraints = [lambda vector: all(-1 < x < 1 for x in vector)]
    assert pos.satisfies_constraints()
    obj_func.vector_constraints = [lambda vector: all(x > 1 for x in vector)]
    assert not pos.satisfies_constraints()


def test_init_behavior():
    obj_func = ObjectiveFunction(function=get_objective_function('schwefel', n_dimensions=5).function,
                                 optimization=Optimization.Min,
                                 n_dimensions=5,
                                 bounds=[-1, 1],
                                 vector_constraints=[lambda vector: all(x > 1 for x in vector)],
                                 name='testname',
                                 special_value=42)

    assert obj_func.function is not None
    assert obj_func.optimization is Optimization.Min
    assert obj_func.n_dimensions == 5
    assert obj_func.bounds == [[-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1]]
    assert obj_func.vector_constraints is not None
    assert obj_func.name == 'testname'
    assert obj_func.special_value == 42


def test_no_bounds():
    obj_func = ObjectiveFunction(function=get_objective_function('schwefel', n_dimensions=5).function,
                                 optimization=Optimization.Min,
                                 n_dimensions=2)
    assert obj_func.bounds == [[-1000, 1000], [-1000, 1000]]


def test_cmp():
    obj_func = get_objective_function('schwefel', optimization=Optimization.Max, n_dimensions=5)
    assert obj_func.optimization == Optimization.Max
    assert obj_func.cmp(1, 0)
    obj_func.optimization = Optimization.Min
    assert obj_func.cmp(0, 1)


def test_increment():
    obj_func = get_objective_function('schwefel', optimization=Optimization.Max, n_dimensions=5)
    obj_func.counter = 0
    obj_func.dynamic_variables = {'counter': lambda: 1}
    obj_func.increment()
    assert obj_func.counter == 1


def test_separate_bounds():
    obj_func = ObjectiveFunction(function=get_objective_function('schwefel', n_dimensions=5).function,
                                 optimization=Optimization.Min,
                                 n_dimensions=5,
                                 bounds=[-1, 1],
                                 vector_constraints=[lambda vector: all(x > 1 for x in vector)],
                                 special_value=42)

    assert all(x == -1 for x in obj_func.lower_bounds())
    assert all(x == 1 for x in obj_func.upper_bounds())


def test_str_representation():
    obj_func = get_objective_function('schwefel')
    assert type(str(obj_func)) is str


def test_equality():
    obj_func = get_objective_function('schwefel', optimization=Optimization.Max, n_dimensions=5)
    duplicate = obj_func.copy()
    pointer = obj_func
    assert obj_func != duplicate
    assert obj_func == pointer


def test_moo():
    functions=[get_objective_function('schwefel', name='hans-paul'),
               get_objective_function('rosenbrock'),
               get_objective_function('qing')]

    moo = MultiObjectiveFunction(functions=functions)
    assert moo.functions == functions
    assert moo.get_function(1) == functions[1]
    assert moo[1] == functions[1]
    assert moo.get_function('hans-paul') == functions[0]

    moo2 = MultiObjectiveFunction(functions=functions)
    assert moo == moo2

