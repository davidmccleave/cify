import copy
from typing import List

from cify.core.base_classes.algorithm import Algorithm
from cify.core.base_classes.collection import Collection
from cify.core.objective_function import ObjectiveFunction
from cify.ec.utils import get_population
from cify.ec.operators.selection import tournament_selection
from cify.ec.operators.crossover import uniform_crossover
from cify.global_constants import get_rng


class EA(Algorithm):
    """
    Defines a generic evolutionary :class:`Algorithm`.
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
        :param crossover_operator: The operator to use for crossover, defaults to discrete uniform crossover.
        :type crossover_operator: function, optional
        :param crossover_params: Additional parameters for the crossover operator.
        :type crossover_params: dict, optional
        :param selection_operator: The operator to use for selection, defaults to random selection.
        :type selection_operator: function, optional
        :param selection_params: Additional parameters for the selection operator.
        :type selection_params: dict, optional
        """

        # must supply obj_func and (population or n_individuals)
        super().__init__(obj_func, **kwargs)

        self.populations = []
        if populations is not None:
            self.populations = populations
            self.n_individuals = len(populations)
        elif n_individuals is not None:
            self.n_individuals = n_individuals
            self.populations.append(get_population(n_individuals=self.n_individuals, n_dimensions=obj_func.n_dimensions,
                                                   obj_func=obj_func))
        else:
            self.populations.append(get_population(50, n_dimensions=obj_func.n_dimensions, obj_func=obj_func))

        # define default operators
        if crossover_operator is None:
            self.crossover_operator = uniform_crossover
        else:
            self.crossover_operator = crossover_operator
        if crossover_params is None:
            self.crossover_params = {'replace': False}
        else:
            self.crossover_params = crossover_params

        if selection_operator is None:
            self.selection_operator = tournament_selection
        else:
            self.selection_operator = selection_operator
        if selection_params is None:
            self.selection_params = {'t_size': 5}
        else:
            self.selection_params = selection_params

        # Set initial global optimum.
        self.global_optimum_pos = self.populations[0][0].chromosome
        for population in self.populations:
            for i in range(len(population)):
                if self.obj_func.cmp(population[i].chromosome.value, self.global_optimum_pos.value):
                    self.global_optimum_pos = population[i].chromosome

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
                # individual.evaluate()
                # Update global best
                if self.obj_func.cmp(individual.chromosome.value, self.global_optimum_pos.value):
                    self.global_optimum_pos = individual.chromosome

            # Get operators to use.
            crossover_operator, selection_operator, crossover_params, selection_params = \
                self.__get_components(population)

            # Reproduce using crossover operator.
            offspring = []
            while len(offspring) < len(population):
                parents = get_rng().choice(population, size=n_parents, replace=replace)
                children = crossover_operator(parents, **crossover_params)
                for child in children:
                    offspring.append(child)

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
        crossover_params = self.crossover_params
        selection_params = self.selection_params

        # Set components in order of priority.
        if hasattr(collection, 'crossover_operator'):
            crossover_operator = collection.crossover_operator
        if hasattr(collection, 'crossover_params'):
            crossover_params = collection.crossover_params

        if hasattr(collection, 'selection_operator'):
            selection_operator = collection.selection_operator
        if hasattr(collection, 'selection_params'):
            selection_params = collection.selection_params

        return crossover_operator, selection_operator, crossover_params, selection_params
