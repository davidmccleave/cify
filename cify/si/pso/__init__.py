"""
Particle swarm optimization (PSO) is a stochastic optimization metaheuristic that is inspired by the movement of
animals in swarms. A classic analogy to PSO metaheuristics is that of a flock of birds. Particles in PSO
algorithms utilize social interaction to move towards the global optima. With this in mind, the most important
components to investigate when customizing or designing your own PSO :class:`Algorithm` s are the position and
velocity update components.

CIFY does not provide a huge array of PSO :class:`Algorithm` s, however, it provides the necessary functionality to
implement many varieties of PSO :class:`Algorithm` s. All provided PSO :class:`Algorithm` s have default components
and control parameters. When designing an :class:`Algorithm` to optimize your chosen :class:`ObjectiveFunction`,
try different velocity update functions and adjust their control parameters to improve performance.
"""

from cify.si.pso.particle import *
from cify.si.pso.utils import *
from cify.si.pso import velocity_updates
