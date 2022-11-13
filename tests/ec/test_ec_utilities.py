from cify.ec.utils import *
from cify.core.utils import get_objective_function


def test_get_population_with_obj_func():
    population = get_population(50, obj_func=get_objective_function('mean-dimensions'))
    assert len(population) == 50


def test_get_population_no_bounds():
    population = get_population(50, upper_bounds=10, lower_bounds=-10)
    assert len(population) == 50


def test_get_population_bounds():
    population = get_population(50, obj_func=get_objective_function('mean-dimensions'),
                                upper_bounds=10, lower_bounds=-10)
    assert len(population) == 50


def test_get_populations_list_list():
    populations = get_populations(3, n_individuals=[10, 20, 30], n_dimensions=[3, 5, 7])
    assert len(populations[0]) == 10
    assert len(populations[1]) == 20
    assert len(populations[2]) == 30
    assert len(populations[0][0].vector) == 3
    assert len(populations[1][0].vector) == 5
    assert len(populations[2][0].vector) == 7


def test_get_populations_list_single():
    populations = get_populations(3, n_individuals=[10, 20, 30], n_dimensions=10)
    assert len(populations[0]) == 10
    assert len(populations[1]) == 20
    assert len(populations[2]) == 30
    assert len(populations[0][0].vector) == 10
    assert len(populations[1][0].vector) == 10
    assert len(populations[2][0].vector) == 10


def test_get_populations_single_list():
    populations = get_populations(3, n_individuals=30, n_dimensions=[3, 5, 7])
    assert len(populations[0]) == 30
    assert len(populations[1]) == 30
    assert len(populations[2]) == 30
    assert len(populations[0][0].vector) == 3
    assert len(populations[1][0].vector) == 5
    assert len(populations[2][0].vector) == 7


def test_get_populations_single_single():
    populations = get_populations(3, n_individuals=30, n_dimensions=8)
    assert len(populations[0]) == 30
    assert len(populations[1]) == 30
    assert len(populations[2]) == 30
    assert len(populations[0][0].vector) == 8
    assert len(populations[1][0].vector) == 8
    assert len(populations[2][0].vector) == 8
