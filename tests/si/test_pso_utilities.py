from cify.si.pso.utils import *
from cify.core.utils import get_objective_function


def test_get_swarm_with_obj_func():
    swarm = get_swarm(50, obj_func=get_objective_function('mean-dimensions'))
    assert len(swarm) == 50


def test_get_swarm_no_bounds():
    swarm = get_swarm(50, upper_bounds=10, lower_bounds=-10)
    assert len(swarm) == 50


def test_get_swarm_bounds():
    swarm = get_swarm(50, obj_func=get_objective_function('mean-dimensions'),
                                upper_bounds=10, lower_bounds=-10)
    assert len(swarm) == 50


def test_get_swarms_list_list():
    swarms = get_swarms(3, n_particles=[10, 20, 30], n_dimensions=[3, 5, 7])
    assert len(swarms[0]) == 10
    assert len(swarms[1]) == 20
    assert len(swarms[2]) == 30
    assert len(swarms[0][0].vector) == 3
    assert len(swarms[1][0].vector) == 5
    assert len(swarms[2][0].vector) == 7


def test_get_swarms_list_single():
    swarms = get_swarms(3, n_particles=[10, 20, 30], n_dimensions=10)
    assert len(swarms[0]) == 10
    assert len(swarms[1]) == 20
    assert len(swarms[2]) == 30
    assert len(swarms[0][0].vector) == 10
    assert len(swarms[1][0].vector) == 10
    assert len(swarms[2][0].vector) == 10


def test_get_swarms_single_list():
    swarms = get_swarms(3, n_particles=30, n_dimensions=[3, 5, 7])
    assert len(swarms[0]) == 30
    assert len(swarms[1]) == 30
    assert len(swarms[2]) == 30
    assert len(swarms[0][0].vector) == 3
    assert len(swarms[1][0].vector) == 5
    assert len(swarms[2][0].vector) == 7


def test_get_swarms_single_single():
    swarms = get_swarms(3, n_particles=30, n_dimensions=8)
    assert len(swarms[0]) == 30
    assert len(swarms[1]) == 30
    assert len(swarms[2]) == 30
    assert len(swarms[0][0].vector) == 8
    assert len(swarms[1][0].vector) == 8
    assert len(swarms[2][0].vector) == 8
