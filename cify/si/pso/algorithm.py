import copy
from typing import List

from cify.global_constants import get_rng
from cify.core.base_classes.collection import Collection
from cify.core.base_classes.agent import Agent
from cify.core.objective_function import ObjectiveFunction
from cify.core.base_classes import Algorithm
from cify.si.pso.particle import Particle
from cify.si.pso.utils import get_swarm
from cify.si.pso.velocity_updates import *
from cify.core.topologies import star_topology

__all__ = ['PSO', 'InertiaWeightPSO', 'NichePSO', 'BinaryPSO']


def default_pos_update(particle: Particle, **kwargs):
    particle.position = particle.position + particle.velocity


def binary_pos_update(particle: Particle, **kwargs):
    for i in range(len(particle.position.vector)):
        if get_rng().uniform() < particle.velocity[i]:
            particle.position.vector[i] = 1
        else:
            particle.position.vector[i] = 0


class PSO(Algorithm):
    """
    Defines a general PSO algorithm.

    The only required parameters are an objective function (`obj_func`) of the type
    :class:`~cify.core.obj_func.ObjectiveFunction` and either, a list of swarms or a single swarm, or
    a number of particles (`n_particles`) to use in a swarm. If no swarms or number of particles is provided,
    a default swarm with 50 particles uniformly distributed within the objective function bounds will be created.
    """

    def __init__(
        self,
        obj_func: ObjectiveFunction,
        swarms: List[Collection] = None,
        n_particles: int = 50,
        velocity_update=None,
        velocity_params: dict = None,
        position_update=None,
        position_params: dict = None,
        topology=None,
        topology_params: dict = None,
        **kwargs
    ):
        """
        :param obj_func: The :class:`~cify.core.objectivefunction.ObjectiveFunction` to be optimized.
        :type obj_func: :class:`ObjectiveFunction`
        :param swarms: The swarms with which to optimize the :class:`~cify.core.objectivefunction.ObjectiveFunction`,
        defaults to 1 swarm containing 50 particles.
        :type swarms: list of :class:`Collection` s, optional
        :param n_particles: The number of particles to use in a swarm for the supplied
                            :class:`~cify.core.objectivefunction.ObjectiveFunction` if no swarms are provided,
                            defaults to 50
        :param n_particles: int, optional
        :param velocity_update: A velocity update function to use, defaults to ``default_vel_update``.
        :type velocity_update: function, optional
        :param velocity_params: Any additional parameters for the velocity update function.
        :type velocity_params: dict, optional
        :param position_update: A position update function to use, defaults to ``default_pos_update``.
        :type position_update: function, optional
        :param position_params: Any additional parameters for the position update function.
        :type position_params: dict, optional
        :param topology: A topology function for social best updates to be used, defaults to ``star_topology``.
        :type topology: function, optional
        :param topology_params: Any additional parameters for the topology function.
        :type topology_params: dict, optional
        """

        super().__init__(obj_func, **kwargs)

        # Create swarms
        self.swarms = []
        if swarms is not None and len(swarms) > 0:
            self.swarms = swarms
        else:
            self.swarms.append(get_swarm(n_particles, n_dimensions=obj_func.n_dimensions, obj_func=obj_func))

        # Set velocity update.
        if velocity_update is not None:
            self.velocity_update = velocity_update
        else:
            self.velocity_update = default_vel_update
        if velocity_params is not None:
            self.velocity_params = velocity_params
        else:
            self.velocity_params = {'c1': 1.4, 'c2': 1.4}

        # Set position update.
        if position_update is not None:
            self.position_update = position_update
        else:
            self.position_update = default_pos_update
        if position_params is not None:
            self.position_params = position_params
        else:
            self.position_params = dict()

        # Set topology for social best updates.
        if topology is not None:
            self.topology = topology
        else:
            self.topology = star_topology
        if topology_params is not None:
            self.topology_params = topology_params
        else:
            self.topology_params = dict()

        # Set initial global optimum.
        self.global_optimum_pos = self.swarms[0][0].position
        for swarm in self.swarms:
            for i in range(len(swarm)):
                if self.obj_func.cmp(swarm[i].position.value, self.global_optimum_pos.value):
                    self.global_optimum_pos = swarm[i].position.copy()
        for swarm in self.swarms:
            for i in range(len(swarm)):
                swarm[i].social_best_pos = self.global_optimum_pos

    def do_iteration(self):
        """Performs a single iteration of the :class:`Algorithm`."""
        for swarm in self.swarms:
            for particle in swarm:
                _, _, topology, _, _, topology_params = self.get_components(particle, swarm)
                if particle.satisfies_constraints():
                    if self.obj_func.cmp(particle.position.value, particle.p_best_position.value):
                        particle.p_best_position = particle.position.copy()
                else:
                    particle.reinit_uniform_position()

                # Call social best updates using provided topology.
                topology(agent=particle, collection=swarm, **topology_params)

        # update global optimum position
        for swarm in self.swarms:
            for particle in swarm:
                if self.obj_func.cmp(particle.position.value, self.global_optimum_pos.value):
                    self.global_optimum_pos = particle.position.copy()

        # Set swarms to return for statistics at end of iteration.
        stats_collections = copy.deepcopy(self.swarms)

        # Prep for next iteration.
        for swarm in self.swarms:
            for particle in swarm:
                velocity_update, position_update, _, velocity_params, position_params, _ \
                    = self.get_components(particle, swarm)
                velocity_update(particle, **velocity_params)
                position_update(particle, **position_params)

        return stats_collections

    def get_components(self, agent: Agent, collection: Collection) -> tuple:
        """
        Returns the appropriate components to use based on whether the given agent or collection contains
        any as attributes.

        :param agent: The :class:`Agent`, or :class:`Particle`, to get components from.
        :type agent: :class:`Agent`
        :param collection: The :class:`Collection`, aka population, to get components from.
        :type collection: :class:`Collection`
        """
        # Set defaults.
        velocity_update = self.velocity_update
        velocity_params = self.velocity_params

        position_update = self.position_update
        position_params = self.position_params

        topology = self.topology
        topology_params = self.topology_params

        # Set components in order of priority.
        if hasattr(agent, 'velocity_update'):
            velocity_update = agent.velocity_update
        elif hasattr(collection, 'velocity_update'):
            velocity_update = collection.velocity_update
        if hasattr(agent, 'velocity_params'):
            velocity_params = agent.velocity_params
        elif hasattr(collection, 'velocity_params'):
            velocity_params = collection.velocity_params

        if hasattr(agent, 'position_update'):
            position_update = agent.position_update
        elif hasattr(collection, 'position_update'):
            position_update = collection.position_update
        if hasattr(agent, 'position_params'):
            position_params = agent.position_params
        elif hasattr(collection, 'position_params'):
            position_params = collection.position_params

        if hasattr(agent, 'topology'):
            topology = agent.topology
        elif hasattr(collection, 'topology'):
            topology = collection.topology
        if hasattr(agent, 'topology_params'):
            topology_params = agent.topology_params
        elif hasattr(collection, 'topology_params'):
            topology_params = collection.topology_params

        return velocity_update, position_update, topology, velocity_params, position_params, topology_params


class InertiaWeightPSO(PSO):
    """
    The inertia weight PSO algorithm. Uses the `inertia_weight_vel_update` velocity update function.
    """
    def __init__(
        self,
        obj_func: ObjectiveFunction,
        swarms: List[Collection] = None,
        n_particles: int = 50,
        velocity_params: dict = None,
        position_update=None,
        position_params: dict = None,
        topology=None,
        topology_params: dict = None,
        **kwargs
    ):
        """
        :param obj_func: The :class:`~cify.core.objectivefunction.ObjectiveFunction` to be optimized.
        :type obj_func: :class:`ObjectiveFunction`
        :param swarms: The swarms with which to optimize the :class:`~cify.core.objectivefunction.ObjectiveFunction`,
        defaults to 1 swarm containing 50 particles.
        :type swarms: list of :class:`Collection` s, optional
        :param n_particles: The number of particles to use in a swarm for the supplied
                            :class:`~cify.core.objectivefunction.ObjectiveFunction` if no swarms are provided,
                            defaults to 50
        :param n_particles: int, optional
        :param velocity_params: Any additional parameters for the velocity update function.
        :type velocity_params: dict, optional
        :param position_update: A position update function to use, defaults to ``default_pos_update``.
        :type position_update: function, optional
        :param position_params: Any additional parameters for the position update function.
        :type position_params: dict, optional
        :param topology: A topology function for social best updates to be used, defaults to ``star_topology``.
        :type topology: function, optional
        :param topology_params: Any additional parameters for the topology function.
        :type topology_params: dict, optional
        """
        if velocity_params is None:
            velocity_params = {'w': 0.72, 'c1': 1.4, 'c2': 1.4}

        super().__init__(
            obj_func=obj_func,
            swarms=swarms,
            n_particles=n_particles,
            velocity_update=inertia_weight_vel_update,
            velocity_params=velocity_params,
            position_update=position_update,
            position_params=position_params,
            topology=topology,
            topology_params=topology_params,
            **kwargs
        )


class NichePSO(PSO):
    """
    Defines a Niche PSO algorithm.
    """

    def __init__(
            self,
            obj_func: ObjectiveFunction,
            sub_swarms: List[Collection] = None,
            n_particles: int = 50,
            velocity_params: dict = None,
            position_update=None,
            position_params: dict = None,
            topology=None,
            topology_params: dict = None,
            **kwargs
    ):
        """
        :param obj_func: The :class:`~cify.core.objectivefunction.ObjectiveFunction` to be optimized.
        :type obj_func: :class:`ObjectiveFunction`
        :param sub_swarms: The swarms with which to optimize the :class:`~cify.core.objectivefunction.ObjectiveFunction`.
        :type sub_swarms: list of :class:`Collection` s
        :param n_particles: The number of particles to use in a sub_swarm for the supplied
                            :class:`~cify.core.objectivefunction.ObjectiveFunction` if no sub_swarms are provided,
                            defaults to 50
        :param n_particles: int, optional
        :param velocity_params: Any additional parameters for the velocity update function.
        :type velocity_params: dict, optional
        :param position_update: A position update function to use, defaults to ``default_pos_update``.
        :type position_update: function, optional
        :param position_params: Any additional parameters for the position update function.
        :type position_params: dict, optional
        :param topology: A topology function for social best updates to be used, defaults to ``star_topology``.
        :type topology: function, optional
        :param topology_params: Any additional parameters for the topology function.
        :type topology_params: dict, optional
        """
        if 'swarms' in kwargs.keys():
            kwargs.pop('swarms')

        super().__init__(
            obj_func=obj_func,
            swarms=sub_swarms,
            n_particles=n_particles,
            velocity_params=velocity_params,
            position_update=position_update,
            position_params=position_params,
            topology=topology,
            topology_params=topology_params,
            **kwargs
        )

    def do_iteration(self):
        """Performs a single iteration of the :class:`Algorithm`."""
        # 1. Train main swarm using cognition only velocity update.
        for swarm in self.swarms:
            for particle in swarm:
                if particle.satisfies_constraints():
                    if self.obj_func.cmp(particle.position.value, particle.p_best_position.value):
                        particle.p_best_position = particle.position.copy()
                else:
                    particle.reinit_uniform_position()

        for swarm in self.swarms:
            for particle in swarm:
                _, position_update, _, velocity_params, position_params, _ \
                    = self.get_components(particle, swarm)
                cognition_only_vel_update(particle, **velocity_params)
                position_update(particle, **position_params)

        # 2. Train sub-swarms independently
        return super().do_iteration()


class BinaryPSO(PSO):
    """
    Defines a binary PSO algorithm. Based on the metaheuristic originally introduced by Kennedy and Eberhart.
    """

    def __init__(
            self,
            obj_func: ObjectiveFunction,
            swarms: List[Collection] = None,
            n_particles: int = 50,
            **kwargs
    ):
        """
        :param obj_func: The :class:`~cify.core.objectivefunction.ObjectiveFunction` to be optimized.
        :type obj_func: :class:`ObjectiveFunction`
        :param swarms: The swarms with which to optimize the :class:`~cify.core.objectivefunction.ObjectiveFunction`,
        defaults to 1 swarm containing 50 particles.
        :type swarms: list of :class:`Collection` s, optional
        :param n_particles: The number of particles to use in a swarm for the supplied
                            :class:`~cify.core.objectivefunction.ObjectiveFunction` if no swarms are provided,
                            defaults to 50
        :param n_particles: int, optional
        """

        if 'swarms' in kwargs.keys():
            kwargs.pop('swarms')

        super().__init__(
            obj_func=obj_func,
            swarms=swarms,
            n_particles=n_particles,
            velocity_update=binary_vel_update,
            position_update=binary_pos_update,
            **kwargs
        )
