import copy
from typing import List
import numpy as np

from cify.global_constants import get_rng
from cify.ec.ea.algorithm import EA
from cify.core.base_classes.collection import Collection
from cify.core.objective_function import ObjectiveFunction
from cify.ec.operators.mutation import uniform_mutation
from cify.ec import operators

__all__ = ['GA', 'HollandsCanonicalGA']


class GA(EA):
    """
    Defines a generic genetic algorithm.
    """

    def __init__(
            self,
            obj_func: ObjectiveFunction,
            populations: List[Collection] = None,
            n_individuals: int = None,
            crossover_operator=None,
            crossover_params: dict = None,
            selection_operator=None,
            selection_params: dict = None,
            mutation_operator=None,
            mutation_params: dict = None,
            **kwargs
    ):
        """
        :param obj_func: The objective function to optimize.
        :type obj_func: :class:`ObjectiveFunction`
        :param populations: A list of populations to use to optimize the :class:`ObjectiveFunction`,
                            defaults to a single population of 50 :class:`Individual` s.
        :type populations: list of :class:`Collection` objects, optional
        :param n_individuals: The number of individuals to use in the population, defaults to 50
        :type n_individuals: int, optional
        :param crossover_operator: The operator to use for crossover, defaults to uniform crossover.
        :type crossover_operator: function, optional
        :param crossover_params: Additional parameters for the crossover operator.
        :type crossover_params: dict, optional
        :param selection_operator: The operator to use for selection, defaults to random selection.
        :type selection_operator: function, optional
        :param selection_params: Additional parameters for the selection operator.
        :type selection_params: dict, optional
        :param mutation_operator: The operator to use for mutation, defaults to uniform mutation.
        :type mutation_operator: function, optional
        :param mutation_params: Additional parameters for the mutation operator.
        :type mutation_params: dict, optional
        """

        super().__init__(obj_func, populations, n_individuals,
                         crossover_operator, crossover_params,
                         selection_operator, selection_params,
                         **kwargs
                         )
        if mutation_operator is None:
            self.mutation_operator = uniform_mutation
        else:
            self.mutation_operator = mutation_operator
        if mutation_params is None:
            self.mutation_params = dict()
        else:
            self.mutation_params = mutation_params

    def do_iteration(self):
        """Performs a single iteration of the :class:`Algorithm`."""
        next_generations = []
        n_parents = 2
        replace = False
        if 'n_parents' in self.crossover_params:
            n_parents = self.crossover_params['n_parents']
        if 'replace' in self.crossover_params:
            replace = self.crossover_params['replace']

        # ------------ Process Populations ------------

        for population in self.populations:
            for individual in population:
                # Update global best
                if self.obj_func.cmp(individual.chromosome.value, self.global_optimum_pos.value):
                    self.global_optimum_pos = individual.chromosome

            # Get operators to use.
            crossover_operator, selection_operator, mutation_operator, \
                crossover_params, selection_params, mutation_params = self.__get_components(population)

            # Reproduce using crossover operator.
            offspring = []
            while len(offspring) < len(population):
                parents = get_rng().choice(population, size=n_parents, replace=replace)
                # if not isinstance(parents, np.ndarray):
                #     parents = [parents, parents]
                children = crossover_operator(parents, **crossover_params)
                for child in children:
                    offspring.append(child)

            # Mutate
            for i in range(len(offspring)):
                mutation_operator(offspring[i], **mutation_params)

            # Select new population using selection operator.
            next_generations.append(selection_operator(offspring, **selection_params))

        # -------------------- END --------------------

        stats_collections = copy.deepcopy(self.populations)
        self.populations = next_generations
        return stats_collections

    def __get_components(self, collection: Collection) -> tuple:
        """
        Returns the appropriate components to use based on whether the given collection contains any as attributes.

        :param collection: The :class:`Collection`, in other words population, to get components from.
        :type collection: :class:`Collection`
        """
        # Set defaults.
        crossover_operator = self.crossover_operator
        selection_operator = self.selection_operator
        mutation_operator = self.mutation_operator
        crossover_params = self.crossover_params
        selection_params = self.selection_params
        mutation_params = self.mutation_params

        # Set components in order of priority.
        if hasattr(collection, 'crossover_operator'):
            crossover_operator = collection.crossover_operator
        if hasattr(collection, 'selection_operator'):
            selection_operator = collection.selection_operator
        if hasattr(collection, 'mutation_operator'):
            mutation_operator = collection.mutation_operator

        if hasattr(collection, 'crossover_params'):
            crossover_params = collection.crossover_params
        if hasattr(collection, 'selection_params'):
            selection_params = collection.selection_params
        if hasattr(collection, 'mutation_params'):
            mutation_params = collection.mutation_params

        return (crossover_operator, selection_operator, mutation_operator,
                crossover_params, selection_params, mutation_params)


class HollandsCanonicalGA(GA):
    # bitstring representation (chromosome)
    # proportional selection
    # one-point cross-over
    # Uniform mutation
    def __init__(
            self,
            obj_func: ObjectiveFunction,
            populations: List[Collection] = None,
            n_individuals: int = None,
            selection_params=None,
            crossover_params=None,
            mutation_params=None,
            **kwargs
    ):
        if selection_params is None:
            self.selection_params = dict()
        else:
            self.selection_params = selection_params

        if crossover_params is None:
            self.crossover_params = dict()
        else:
            self.crossover_params = crossover_params

        if mutation_params is None:
            self.mutation_params = dict()
        else:
            self.mutation_params = mutation_params

        super().__init__(
            obj_func=obj_func,
            populations=populations,
            n_individuals=n_individuals,
            selection_operator=operators.proportional_selection,
            selection_params=self.selection_params,
            crossover_operator=operators.one_point_crossover,
            crossover_params=self.crossover_params,
            mutation_operator=uniform_mutation,
            mutation_params=self.mutation_params,
            **kwargs
        )
