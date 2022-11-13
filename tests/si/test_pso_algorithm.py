from cify.si.pso.algorithm import PSO, InertiaWeightPSO
from cify.core.utils import get_objective_function
from cify.si.pso.utils import get_swarm
from cify.si.pso.velocity_updates import *


def test_pso():
    obj_func = get_objective_function('mean-dimensions')
    PSO(obj_func=obj_func)
    PSO(obj_func=obj_func, n_individuals=35)
    algo = PSO(obj_func=obj_func, swarms=[get_swarm(obj_func=obj_func)])
    algo.execute(10, 10000, lambda: True)


def test_pso_inertia_weight_vel_update():
    obj_func = get_objective_function('mean-dimensions')
    algo = PSO(obj_func=obj_func, swarms=[get_swarm(obj_func=obj_func)],
               velocity_update=inertia_weight_vel_update)
    algo.execute(1)


def test_pso_deterministic_iw_vel_update():
    obj_func = get_objective_function('mean-dimensions')
    algo = PSO(obj_func=obj_func, swarms=[get_swarm(obj_func=obj_func)],
               velocity_update=deterministic_iw_vel_update)
    algo.execute(1)


def test_pso_constriction_coefficient_vel_update():
    obj_func = get_objective_function('mean-dimensions')
    algo = PSO(obj_func=obj_func, swarms=[get_swarm(obj_func=obj_func)],
               velocity_update=constriction_coefficient_vel_update)
    algo.execute(1)
