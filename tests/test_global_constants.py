import numpy as np
from cify.global_constants import *


def test_get_rng():
    rng = get_rng()
    assert type(rng) == np.random.Generator


def test_set_seed():
    """
    if no exception is raised, set seed worked.
    There is no way of reliably accessing the seed as
    an attribute of the numpy Generator.
    """
    set_seed(1234)
