import math
import numpy as np
from cify.si.pso.particle import Particle
from cify.global_constants import get_rng

__all__ = ['default_vel_update', 'cognition_only_vel_update', 'inertia_weight_vel_update',
           'deterministic_iw_vel_update', 'constriction_coefficient_vel_update', 'binary_vel_update']


def default_vel_update(particle: Particle,
                       c1: float = 1.4,
                       c2: float = 1.4,
                       **kwargs
                       ):
    """
    The default velocity update function.

    :param particle: The particle whose velocity is to be updated.
    :type particle: :class:`Particle`
    :param c1: The first acceleration coefficient. Affects the weighting of the cognition component, defaults to 1.4
    :type c1: float
    :param c2: The second acceleration coefficient. Affects the weighting of the social component, defaults to 1.4
    :type c2: float
    """
    r1 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    r2 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    particle.velocity = (
            particle.velocity
            + c1 * r1 * (particle.p_best_position - particle.position)
            + c2 * r2 * (particle.social_best_pos - particle.position)
    )


def cognition_only_vel_update(particle: Particle,
                              c1: float = 1.4,
                              **kwargs
                              ):
    """
    Uses only the cognition component of a :class:`Particle` (its ``p_best_position``) to influence
    its velocity.

    :param particle: The particle whose velocity is to be updated.
    :type particle: :class:`Particle`
    :param c1: The first acceleration coefficient that affects the weighting applied to the cognition component,
    defaults to 1.4
    :type c1: float
    """
    r1 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    particle.velocity = (
            particle.velocity
            + c1 * r1 * (particle.p_best_position - particle.position)
    )


def inertia_weight_vel_update(particle: Particle,
                              w: float = .72,
                              c1: float = 1.4,
                              c2: float = 1.4,
                              **kwargs
                              ):
    """
    Inertia weight velocity update.

    :param particle: The particle whose velocity is to be updated.
    :type particle: :class:`Particle`
    :param w: The weight component of the inertia weight update, defaults to 0.72
    :type w: float
    :param c1: The first acceleration coefficient. Affects the weighting of the cognition component, defaults to 1.4
    :type c1: float
    :param c2: The second acceleration coefficient. Affects the weighting of the social component, defaults to 1.4
    :type c2: float
    """
    r1 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    r2 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    particle.velocity = (
            w * particle.velocity
            + c1 * r1 * (particle.p_best_position - particle.position)
            + c2 * r2 * (particle.social_best_pos - particle.position)
    )


def deterministic_iw_vel_update(particle: Particle,
                                w: float = .72,
                                c1: float = 1.4,
                                c2: float = 1.4,
                                **kwargs
                                ):
    """
    Inertia weight velocity update without stochastic variables.

    :param particle: The particle whose velocity is to be updated.
    :type particle: :class:`Particle`
    :param w: The weight component of the inertia weight update, defaults to 0.72
    :type w: float
    :param c1: The first acceleration coefficient. Affects the weighting of the cognition component, defaults to 1.4
    :type c1: float
    :param c2: The second acceleration coefficient. Affects the weighting of the social component, defaults to 1.4
    :type c2: float
    """
    particle.velocity = (
            w * particle.velocity
            + np.full(len(particle.position), c1) * (particle.p_best_position - particle.position)
            + np.full(len(particle.position), c2) * (particle.social_best_pos - particle.position)
    )


def constriction_coefficient_vel_update(particle: Particle,
                                        k: float = 1.,
                                        c1: float = 1.4,
                                        c2: float = 1.4,
                                        **kwargs
                                        ):
    """
    Velocity update function based on using a constriction coefficient.
    Uses the control parameter `k` to represent the constriction coefficient.

    :param particle: The particle whose velocity is to be updated.
    :type particle: :class:`Particle`
    :param k: The weight component of the inertia weight update, defaults to 1.0
    :type k: float
    :param c1: The first acceleration coefficient. Affects the weighting of the cognition component, defaults to 1.4
    :type c1: float
    :param c2: The second acceleration coefficient. Affects the weighting of the social component, defaults to 1.4
    :type c2: float
    """
    r1 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    r2 = get_rng().uniform(low=0, high=1, size=particle.obj_func.n_dimensions)
    x = 2 * k / (2 - (c1 + c2) - math.sqrt(abs((c1 + c2) * ((c1 + c2) - 4))))
    particle.velocity = (
            x * (particle.velocity
                 + c1 * r1 * (particle.p_best_position - particle.position)
                 + c2 * r2 * (particle.social_best_pos - particle.position))
    )


def binary_vel_update(particle: Particle, **kwargs):
    """
    The binary velocity update. This update interprets velocity for binary position representations
    as a probability calculated as follows:

    ..math::

        p_{ij}(t) = \frac{1}{1 + e^{-V_{ij}(t)}}

    :param particle: The particle whose velocity is to be updated.
    :type particle: :class:`Particle`
    """
    new_vel = [1 / (1 + math.e ** (-v)) for v in particle.velocity]
    particle.velocity = new_vel
