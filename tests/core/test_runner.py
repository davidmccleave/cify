from cify.core.runner import Runner
from cify.core.task import Task
from cify.core.utils import get_objective_function
from cify.si.pso.algorithm import PSO


def test_init():
    obj_func = get_objective_function('schwefel')
    runner = Runner()
    assert len(runner.algorithm_pool) == 0
    assert len(runner.objective_function_pool) == 0
    assert len(runner.tasks) == 0
    assert type(runner.name) is not None
    assert len(runner.results) == 0
    assert runner.total_running_time is None
    task = Task(algorithm=PSO(obj_func), obj_func=obj_func)
    runner = Runner([task])
    assert len(runner.tasks) == 1
    assert runner.tasks[0] == task


def test_add_and_remove():
    obj_func = get_objective_function('schwefel')
    task = Task(algorithm=PSO(obj_func), obj_func=obj_func)
    pso = PSO(obj_func)

    runner = Runner()
    runner.add(pso)
    runner.add(obj_func)
    runner.add(task)
    assert len(runner.algorithm_pool) == 1
    assert len(runner.objective_function_pool) == 1
    assert len(runner.tasks) == 1

    runner.remove(pso)
    runner.remove(obj_func)
    runner.remove(task)
    assert len(runner.algorithm_pool) == 0
    assert len(runner.objective_function_pool) == 0
    assert len(runner.tasks) == 0


def test_compile():
    obj_func = get_objective_function('schwefel')
    pso = PSO(obj_func)

    runner = Runner()
    runner.add(pso)
    runner.add(obj_func)
    runner.compile()
    assert len(runner.tasks) == 1
    assert runner.tasks[0].obj_func == obj_func
    assert runner.tasks[0].algorithm == pso
    runner.compile(relationship='one-to-one')
    assert len(runner.tasks) == 1
    assert runner.tasks[0].obj_func == obj_func
    assert runner.tasks[0].algorithm == pso
    runner.compile(relationship='many-to-one')
    assert len(runner.tasks) == 1
    assert runner.tasks[0].obj_func == obj_func
    assert runner.tasks[0].algorithm == pso


def test_summary():
    runner = Runner()
    assert type(runner.summary()) == str


def test_execute():
    obj_func = get_objective_function('schwefel')
    pso = PSO(obj_func)
    runner = Runner()
    runner.add(pso)
    runner.add(obj_func)
    runner.compile()
    runner.execute()
    assert len(runner.results) > 0
