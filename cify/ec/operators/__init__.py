"""
There are three types of operators used in evolutionary computation:

* crossover
* mutation
* selection

Operators across all three types take different parameters and all operators have default parameters if you do
not wish to tune them further. It is worth looking at the possible control parameters for your chosen
operators as tuning the control parameters can have a significant positive effect on the performance of your
chosen evolutionary :class:`Algorithm`.
"""

from cify.ec.operators.crossover import *
from cify.ec.operators.mutation import *
from cify.ec.operators.selection import *
