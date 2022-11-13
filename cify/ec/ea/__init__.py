"""
An evolutionary algorithm (EA) is a generic population-based metaheuristic algorithm. Evolutionary algorithms are
a subset of evolutionary computation, however, forms a collection of other subsets of common metaheuristics.
For example, genetic algorithms (GAs), genetic programs (GPs) and evolutionary programs (GPs) are all subsets
of evolutionary algorithms.

The evolutionary algorithms contained in CIFY are easily customizable by changing the components used by any of the
algorithms or their parameters. All algorithms have default operators and parameters and can be used as they are,
however, to improve performance on your chosen objective functions, it is best to try different operators and
control parameters for these operators.

In this package, the generic :class:`EA` is given, which does not make use of mutation. If you are looking for a comparable
:class:`Algorithm` that does, try the genetic algorithm, :class:`GA`.
"""