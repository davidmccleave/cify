from typing import List
from cify.core.objective_function import ObjectiveFunction
from cify.core.base_classes.collection import Collection
from cify.si.pso.particle import Particle
from cify.core.utils import get_position_vector
from cify.global_constants import get_rng

__all__ = ['get_swarm', 'get_swarms']


def get_swarm(
        n_particles: int = 50,
        obj_func: ObjectiveFunction = None,
        n_dimensions: int = None,
        upper_bounds=None,
        lower_bounds=None,
        **kwargs
) -> Collection:
    """
    Returns a :class:`Collection`, affectionately known as a swarm, of :class:`~cify.si.pso.particle.Particle` objects.

    :param n_particles: The number of :class:`Particle` s in the population, defaults to 50
    :type n_particles: int, optional
    :param obj_func: The :class:`ObjectiveFunction` to generate a population of :class:`Particle` s for.
    :type obj_func: :class:`ObjectiveFunction`
    :param n_dimensions: The number of dimensions of the :class:`ObjectiveFunction` search space, used when generating
                         position vectors for each :class:`Particle` in the population. If an
                         :class:`ObjectiveFunction` is provided and this field is not populated, defaults to the number
                         of dimensions of the :class:`ObjectiveFunction`. If no :class:`ObjectiveFunction` is provided,
                         defaults to 10
    :type n_dimensions: int, optional
    :param upper_bounds: An array or scalar value representing the upper bounds to initialize particles within.
                         If an :class:`ObjectiveFunction` is provided, the particles will be uniformly distributed
                         within the bounds of the :class:`ObjectiveFunction`.
    :type upper_bounds: float or array-like of floats, optional.
    :param lower_bounds: An array or scalar value representing the lower bounds to initialize particles within.
                         If an :class:`ObjectiveFunction` is provided, the particles will be uniformly distributed
                         within the bounds of the :class:`ObjectiveFunction`.
    :type lower_bounds: float or array-like of floats, optional.

    :return: A swarm of particles.
    :rtype: :class:`Collection` of :class:`Particle` s
    """
    swarm = []
    if obj_func is not None:
        if n_dimensions is None:
            n_dimensions = obj_func.n_dimensions
        for i in range(0, n_particles):
            swarm.insert(
                i, Particle(
                    position=get_position_vector(obj_func=obj_func, as_position=True, n_dimensions=n_dimensions),
                    obj_func=obj_func
                )
            )
    else:
        if n_dimensions is None:
            n_dimensions = 10
        if lower_bounds is None or upper_bounds is None:
            for i in range(0, n_particles):
                swarm.insert(i, Particle(position=get_rng().uniform(low=0, high=1, size=n_dimensions)))
        else:
            for i in range(0, n_particles):
                swarm.insert(i, Particle(position=get_rng().uniform(low=lower_bounds, high=upper_bounds, size=n_dimensions)))
    return Collection(swarm, **kwargs)


def get_swarms(
        n_swarms: int = 3,
        n_particles: int = 50,
        n_dimensions: int = 10,
        obj_func: ObjectiveFunction = None,
        upper_bounds=None,
        lower_bounds=None,
        **kwargs
) -> List[Collection]:
    """
    Returns a list of :class:`Collection` s of :class:`Particle` objects. In other words, a list of swarms.

    :param n_swarms: The number of swarms to return, defaults to 3
    :type n_swarms: int, optional
    :param n_particles: The number of particles in each swarm or all swarms, defaults to 50
    :type n_particles: int or list of ints, optional
    :param n_dimensions: The number of dimensions of the :class:`ObjectiveFunction` search space, used when
                         generating position vectors for each particle in the swarm.
                         If an :class:`ObjectiveFunction` is provided, this field will not be used.
    :type n_dimensions: int or list of ints, optional
    :param obj_func: The :class:`ObjectiveFunction` to generate swarms of :class:`Particle` s for.
    :type obj_func: :class:`ObjectiveFunction`
    :param upper_bounds: An array or scalar value representing the upper bounds to initialize particles within.
    :type upper_bounds: float or array-like of floats, optional
    :param lower_bounds: An array or scalar value representing the lower bounds to initialize particles within.
    :type lower_bounds: float or array-like of floats, optional

    :return: A list of swarms for the given :class:`ObjectiveFunction`.
    :rtype: list of :class:`Collection` objects
    """
    swarms = []
    if type(n_particles) is list:
        if type(n_dimensions) is list:
            for i in range(n_swarms):
                swarms.append(get_swarm(n_particles[i], obj_func, n_dimensions[i],
                                        upper_bounds, lower_bounds, **kwargs))
        else:
            for i in range(n_swarms):
                swarms.append(get_swarm(n_particles[i], obj_func, n_dimensions,
                                        upper_bounds, lower_bounds, **kwargs))
    else:
        if type(n_dimensions) is list:
            for i in range(n_swarms):
                swarms.append(get_swarm(n_particles, obj_func, n_dimensions[i],
                                        upper_bounds, lower_bounds, **kwargs))
        else:
            for i in range(n_swarms):
                swarms.append(get_swarm(n_particles, obj_func, n_dimensions,
                                        upper_bounds, lower_bounds, **kwargs))
    return swarms
