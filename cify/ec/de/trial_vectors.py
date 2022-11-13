import numpy as np
from cify.ec.individual import Individual
from cify.global_constants import get_rng
from cify.core.base_classes.collection import Collection
from cify.ec.de.target_vectors import *

__all__ = ['default_trial_vector', 'current_to_best_trial_vector']


def default_trial_vector(
        population: list or Collection,
        individual: Individual,
        target_vector: list or np.ndarray = None,
        scale_factor: float = None,
        diff_vector: list or np.ndarray = None,
        **kwargs
):
    """
    The default trial vector operator.
    .. math::

        target\\:vector + scale\\:factor + difference\\:vector

    :param population: The population to determine the trial vector from.
    :type population: list, :class:`Collection`
    :param individual: The individual to determine the coupling trial vector for.
    :type individual: :class:`Individual`
    :param target_vector: The target vector to use during calculation of the trial vector.
    :type target_vector: list, Numpy array, optional
    :param scale_factor: The scale factor to use.
    :type scale_factor: float, optional
    :param diff_vector: The difference vector to use.
    :type diff_vector: list, Numpy array, optional

    :return: The trial vector.
    :rtype: Numpy array
    """
    # set defaults
    if not target_vector:
        target_vector = random_target_vector(population=population, individual=individual)
    else:
        target_vector = target_vector
    if not scale_factor:
        scale_factor = 0.5
    else:
        scale_factor = scale_factor
    if not diff_vector:
        population.remove(individual)
        matching_individual = None
        for indv in population:
            if np.array_equal(indv.chromosome.vector, target_vector):
                matching_individual = indv
        if matching_individual:
            population.remove(matching_individual)
        vectors = get_rng().choice(population, size=2, replace=False)
        population.append(individual)
        if matching_individual:
            population.append(matching_individual)
        diff_vector = vectors[0].chromosome.vector - vectors[1].chromosome.vector

    return target_vector + scale_factor * diff_vector


def current_to_best_trial_vector(population: list or Collection,
                                 individual: Individual,
                                 alpha: float = 0.5,
                                 diff_vector: list or np.ndarray = None,
                                 **kwargs
                                 ) -> np.ndarray:
    """
    The current to best trial vector operator.

    .. math::
        \\alpha \\times current\\:best + (1 - \\alpha) \\times global\\: best + difference\\: vector

    :param population: The population to determine the trial vector from.
    :type population: list, :class:`Collection`
    :param individual: The individual to determine the coupling trial vector for.
    :type individual: :class:`Individual`
    :param alpha: The alpha value that determines weightings between
    :type alpha: float, optional
    :param diff_vector: The difference vector to use.
    :type diff_vector: list, Numpy array, optional

    :return: The trial vector.
    :rtype: Numpy array
    """
    # get current iterations best position
    obj_func = population[0].obj_func
    curr_best = population[0].chromosome
    for idv in population:
        if obj_func.cmp(idv.chromosome.value, curr_best.value):
            curr_best = idv.chromosome

    if not diff_vector:
        population.remove(individual)
        vectors = get_rng().choice(population, size=2, replace=False)
        population.append(individual)
        diff_vector = vectors[0].chromosome - vectors[1].position

    # TODO: change back to (1 - alpha) * global_best_vector + diff_vector
    return np.array(alpha * curr_best.vector + (1 - alpha) * curr_best.vector + diff_vector)

