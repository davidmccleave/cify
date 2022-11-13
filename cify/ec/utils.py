from typing import List

from cify.core.objective_function import ObjectiveFunction
from cify.core.base_classes.collection import Collection
from cify.core.position import Position
from cify.ec.individual import Individual
from cify.core.utils import get_position_vector
from cify.global_constants import get_rng

__all__ = ['get_population', 'get_populations']


def get_population(
        n_individuals: int = 50,
        obj_func: ObjectiveFunction = None,
        n_dimensions: int = None,
        upper_bounds=None,
        lower_bounds=None,
        **kwargs
) -> Collection:
    """
    Returns a :class:`Collection` of :class:`Individual` objects.

    :param n_individuals: The number of :class:`Individual` s in the population, defaults to 50
    :type n_individuals: int, optional
    :param obj_func: The :class:`ObjectiveFunction` to generate a population of :class:`Individual` s for.
    :type obj_func: :class:`ObjectiveFunction`
    :param n_dimensions: The number of dimensions of the :class:`ObjectiveFunction` search space, used when generating
                         position vectors for each :class:`Individual` in the population. If an
                         :class:`ObjectiveFunction` is provided and this field is not populated, defaults to the number
                         of dimensions of the :class:`ObjectiveFunction`. If no :class:`ObjectiveFunction` is provided,
                         defaults to 10
    :type n_dimensions: int, optional
    :param upper_bounds: An array or scalar value representing the upper bounds to initialize individuals within.
                         If an :class:`ObjectiveFunction` is provided, the individuals will be uniformly distributed
                         within the bounds of the :class:`ObjectiveFunction`.
    :type upper_bounds: float or array-like of floats, optional
    :param lower_bounds: An array or scalar value representing the lower bounds to initialize individuals within.
                         If an :class:`ObjectiveFunction` is provided, the individuals will be uniformly distributed
                         within the bounds of the :class:`ObjectiveFunction`.
    :type lower_bounds: float or array-like of floats, optional

    :return: A population of individuals.
    :rtype: :class:`Collection` of :class:`Individual` s
    """

    population = []
    if obj_func is not None:
        if n_dimensions is None:
            n_dimensions = obj_func.n_dimensions
        for i in range(0, n_individuals):
            population.insert(
                i,
                Individual(
                    chromosome=get_position_vector(obj_func=obj_func, as_position=True, n_dimensions=n_dimensions),
                    obj_func=obj_func
                )
            )
    else:
        if n_dimensions is None:
            n_dimensions = 10
        if lower_bounds is None or upper_bounds is None:
            for i in range(0, n_individuals):
                population.insert(
                    i,
                    Individual(
                        chromosome=Position(vector=get_rng().uniform(low=0, high=1, size=n_dimensions)),
                    ),
                )
        else:
            for i in range(0, n_individuals):
                population.insert(
                    i,
                    Individual(
                        chromosome=Position(vector=get_rng().uniform(
                            low=lower_bounds, high=upper_bounds, size=n_dimensions
                        ))
                    ),
                )
    return Collection(population, **kwargs)


def get_populations(
        n_populations: int = 3,
        n_individuals: int = 50,
        obj_func: ObjectiveFunction = None,
        n_dimensions: int = 10,
        upper_bounds=None,
        lower_bounds=None,
        **kwargs
) -> List[Collection]:
    """
    Returns a list of :class:`Collection` s of :class:`Individual` objects. In other words, a list of populations.

    :param n_populations: The number of populations to return, defaults to 3
    :type n_populations: int, optional
    :param n_individuals: The number of individuals in each population or all populations, defaults to 50
    :type n_individuals: int or list of ints, optional
    :param obj_func: The :class:`ObjectiveFunction` to generate populations of :class:`Individual` s for.
    :type obj_func: :class:`ObjectiveFunction`
    :param n_dimensions: The number of dimensions of the :class:`ObjectiveFunction` search space, used when
                         generating position vectors for each individual in the population.
                         If an :class:`ObjectiveFunction` is provided, this field will not be used.
    :type n_dimensions: int or list of ints, optional
    :param upper_bounds: An array or scalar value representing the upper bounds to initialize individuals within.
    :type upper_bounds: float or array_like of floats, optional
    :param lower_bounds: An array or scalar value representing the lower bounds to initialize individuals within.
    :type lower_bounds: float or array_like of floats, optional

    :return: A list of populations for the given :class:`ObjectiveFunction`.
    :rtype: list of :class:`Collection` objects
    """
    populations = []
    if type(n_individuals) is list:
        if type(n_dimensions) is list:
            for i in range(n_populations):
                populations.append(get_population(n_individuals[i], obj_func, n_dimensions[i],
                                                  upper_bounds, lower_bounds, **kwargs))
        else:
            for i in range(n_populations):
                populations.append(get_population(n_individuals[i], obj_func, n_dimensions,
                                                  upper_bounds, lower_bounds, **kwargs))
    else:
        if type(n_dimensions) is list:
            for i in range(n_populations):
                populations.append(get_population(n_individuals, obj_func, n_dimensions[i],
                                                  upper_bounds, lower_bounds, **kwargs))
        else:
            for i in range(n_populations):
                populations.append(get_population(n_individuals, obj_func, n_dimensions,
                                                  upper_bounds, lower_bounds, **kwargs))
    return populations
