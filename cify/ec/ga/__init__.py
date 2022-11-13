"""
Genetic algorithms are evolutionary algorithms based on the process of natural selection.
Genetic algorithms start each iteration by performing crossover between parent :class:`Individual` s using a defined
``crossover_operator``. Following this, the offspring generated are mutated using a given ``mutation_operator``
and finally, the next generation is selected using the ``selection_operator``.

It is worth going through the provided operators to choose appropriate behaviours for the :class:`ObjectiveFunction`
you are attempting to optimize. Adjusting the control parameters of the chosen operators can also have a drastic
effect on the :class:`GA`'s search performance.
"""