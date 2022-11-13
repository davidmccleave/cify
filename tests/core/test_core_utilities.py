import numpy as np
from cify.core.optimization import Optimization
from cify.core.utils import *


def test_schwefel():
    schwefel = get_objective_function('schwefel1', n_dimensions=2)
    assert schwefel.bounds == [[-100, 100], [-100, 100]]
    assert schwefel.function is not None


def test_rosenbrock():
    rosenbrock = get_objective_function('rosenbrock', n_dimensions=3)
    assert rosenbrock.bounds == [[-2.048, 2.048], [-2.048, 2.048], [-2.048, 2.048]]
    assert rosenbrock.function is not None


def test_exponential():
    exponential = get_objective_function('exponential', Optimization.Max)
    assert exponential.optimization == Optimization.Max
    assert exponential.cmp(10, 0) is True
    assert exponential.function is not None


def test_brown():
    brown = get_objective_function('brown', n_dimensions=3)
    assert brown.optimization == Optimization.Min
    assert brown.cmp(10, 0) is False
    assert brown.function is not None


def test_qing():
    qing = get_objective_function('qing')
    assert qing.optimization == Optimization.Min
    assert qing.cmp(10, 0) is False
    assert qing.function is not None


def test_vector_constraints():
    def constraint(vector):
        return vector[0] > 0 and vector[1] > 0

    schwefel = get_objective_function('schwefel1', n_dimensions=2, vector_constraints=[constraint])
    assert schwefel.satisfies_constraints(np.array([1., 1.]))
    assert schwefel.satisfies_constraints(np.array([-1., 1.])) is False


def test_get_position_vector():
    schwefel = get_objective_function('schwefel1')
    assert schwefel.satisfies_constraints(get_position_vector(schwefel))
    assert schwefel.satisfies_constraints(get_position_vector(schwefel, as_position=True).vector)
