from cify.core.topologies import *
from cify.core.utils import get_objective_function
from cify.si.pso.utils import get_swarm


def test_star_topology():
    obj_func = get_objective_function('mean-dimensions')
    swarm = get_swarm(obj_func=obj_func)
    best_value = swarm[0].value
    for particle in swarm:
        if obj_func.cmp(particle.value, best_value):
            best_value = particle.value
    star_topology(swarm[0], swarm)
    assert swarm[0].social_best_pos.value == best_value


def test_ring_topology():
    obj_func = get_objective_function('mean-dimensions')
    swarm = get_swarm(obj_func=obj_func)
    ring_topology(swarm[0], swarm)
