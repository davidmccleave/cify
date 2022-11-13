from cify.ec.de.algorithm import DE
from cify.core.utils import get_objective_function
from cify.ec.utils import get_population
from cify.ec.de.trial_vectors import *


def test_de():
    obj_func = get_objective_function('mean-dimensions')
    DE(obj_func=obj_func)
    algo = DE(obj_func=obj_func, populations=[get_population(obj_func=obj_func)])
    algo.execute(10, 10000, lambda: True)


def test_trial_vectors():
    obj_func = get_objective_function('mean-dimensions')
    algo = DE(obj_func=obj_func, populations=[get_population(obj_func=obj_func)],
              trial_vector_operator=current_to_best_trial_vector)
    algo.execute(1)
