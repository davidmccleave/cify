import operator
import numpy as np
from cify.core.optimization import Optimization


def test_cmp():
    opt = Optimization.Min
    assert opt.value == 1
    assert opt.cmp(1, 2) is True
    opt = Optimization.Max
    assert opt.value == 2
    assert opt.cmp(1, 2) is False
    assert opt.cmp(2, 1) is True


def test_verb():
    opt = Optimization.Min
    assert opt.verb() == 'Minimizing'
    opt = Optimization.Max
    assert opt.verb() == 'Maximizing'
