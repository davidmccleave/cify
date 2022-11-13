import numpy as np

from cify.core.optimization import Optimization
from cify.ec.individual import Individual
from cify.global_constants import get_rng
from cify.core.base_classes.collection import Collection

__all__ = ['random_target_vector', 'current_best_target_vector', 'best_target_vector']


def random_target_vector(population: list or Collection, individual: Individual, **kwargs) -> np.ndarray:
    """
    Returns a random target vector from the population. This operator will not return the same
    :class:`Individual` that was passed to it.

    :param population: The population to determine the target vector from.
    :type population: list, :class:`Collection`
    :param individual: The individual not to include when randomly selecting a target vector.
    :type individual: :class:`Individual`

    :return: The calculated target vector.
    :rtype: Numpy array
    """
    population.remove(individual)
    choice = get_rng().choice(population, size=1)[0]
    population.append(individual)
    return choice.chromosome


def current_best_target_vector(population: list or Collection, **kwargs) -> np.ndarray:
    """
    Returns the current best chromosome as a Numpy array.

    :param population: The population to determine the target vector from.
    :type population: list, :class:`Collection`

    :return: The calculated target vector.
    :rtype: Numpy array
    """
    curr_best = population[0].chromosome
    for idv in population:
        if idv.position.value < curr_best.value:
            curr_best = idv.position
    return curr_best


def best_target_vector(population: list or Collection = None, **kwargs) -> np.ndarray:
    """
    Returns the current global best chromosome as a Numpy array.

    :param population: The population to determine the target vector from.
    :type population: list, :class:`Collection`

    :return: The calculated target vector.
    :rtype: Numpy array
    """
    if population[0].obj_func.optimization == Optimization.Min:
        return min(population)
    else:
        return max(population)
