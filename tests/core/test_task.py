from cify.core.task import Task
from cify.core.utils import get_objective_function
from cify.si.pso.algorithm import PSO


def test_init():
    obj_func = get_objective_function('schwefel')
    task = Task(algorithm=PSO(obj_func), obj_func=obj_func)
    assert task.algorithm is not None
    assert task.obj_func is not None
    assert task.n_iterations == 1
    assert task.n_evaluations == 0
    assert task.stopping_condition is None
    assert len(task.executables) == 0
    assert task.name is not None
    assert task.log is False


def test_get_statistics():
    obj_func = get_objective_function('schwefel')
    task = Task(algorithm=PSO(obj_func), obj_func=obj_func)
    task.execute()
    assert task.get_statistics() is not None


def test_add_executables():
    obj_func = get_objective_function('schwefel')
    task = Task(algorithm=PSO(obj_func), obj_func=obj_func)
    task.add_executable(lambda: 1)
    assert len(task.executables) == 1


def test_str_representation():
    obj_func = get_objective_function('schwefel')
    task = Task(algorithm=PSO(obj_func), obj_func=obj_func)
    assert type(str(task)) == str
