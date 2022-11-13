from cify.core.base_classes.collection import Collection
from cify.core.utils import get_objective_function
from cify.si.pso.particle import Particle
import pandas as pd


def get_func_and_agents():
    obj_func = get_objective_function('mean-dimensions', n_dimensions=3)
    agents = [Particle([1, 1, 1], obj_func=obj_func),
              Particle([2, 2, 2], obj_func=obj_func),
              Particle([3, 3, 3], obj_func=obj_func)]
    return obj_func, agents


def test_copy():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert type(collection.copy()) == Collection


def test_to_dataframe():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    df = collection.to_dataframe()
    assert type(df) == pd.DataFrame


def test_set_agents():
    obj_func, agents = get_func_and_agents()
    collection = Collection()
    collection.set_agents(agents)
    assert len(collection) == 3


def test_append():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    collection.append(Particle([4, 4, 4], obj_func=obj_func))
    assert len(collection) == 4


def test_remove():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    new_agent = Particle([4, 4, 4], obj_func=obj_func)
    collection.append(new_agent)
    collection.remove(new_agent)
    assert len(collection) == 3


def test_empty():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert len(collection) == 3
    collection.empty()
    assert len(collection) == 0


def test_sum():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert collection.sum() == 6.


def test_max():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert collection.max().value == 3.


def test_min():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert collection.min().value == 1.


def test_indexing():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    new_agent = Particle([4, 4, 4], obj_func=obj_func)
    assert collection[0].value == 1.
    assert collection[1].value == 2.
    assert collection[2].value == 3.
    collection[0] = new_agent
    assert collection[0].value == 4.


def test_summation():
    obj_func, agents = get_func_and_agents()
    collection1 = Collection(agents)
    new_agent = Particle([4, 4, 4], obj_func=obj_func)
    collection2 = Collection([new_agent])
    summation = collection1 + collection2
    assert len(summation) == 4
    assert summation[0].value == 1.


def test_equality():
    obj_func, agents = get_func_and_agents()
    collection1 = Collection(agents)
    collection2 = Collection(agents)
    assert collection1 == collection2


def test_str():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert type(str(collection)) is str


def test_next():
    obj_func, agents = get_func_and_agents()
    collection = Collection(agents)
    assert next(collection) == collection[0]
