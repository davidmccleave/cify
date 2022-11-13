"""
Evolutionary computation (EC) is a family of metaheuristics used for optimization of an :class:`ObjectiveFunction`
that are inspired by the process of biological evolution. The algorithms all rely on trial and error and are driven
towards optimal solutions through imitating natural selection. Currently, there are three major paradigms provided
by CIFY:

* Differential Evolution (DE)
* Evolutionary Algorithms (EA)
* Genetic Algorithms (GA)

It is important to note, however, that CIFY components support the logic necessary to implement other EC algorithms,
and you are welcome to post issues if you are struggling to implement an algorithm that may not be well-supported.

This package contains the evolutionary algorithms mentioned previously as well as their major component,
evolutionary operators.
"""

from cify.ec.de import *
from cify.ec.utils import *
from cify.ec.individual import *
from cify.ec import operators
