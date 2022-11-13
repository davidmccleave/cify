"""
Differential evolution (DE) is a population-based metaheuristic search algorithm
that attempts to optimize an :class:`ObjectiveFunction` by iteratively improving :class:`Individual` s
representing candidate solutions based on an evolutionary process. DE is a subset of evolutionary computation
that is restricted in that the genotypes must be some form of a real-valued vector. Despite this, it performs
fairly well when control parameters are appropriately tuned.
"""

from cify.ec.de import trial_vectors
from cify.ec.de import target_vectors

