import copy
from typing import List

from cify.core.objective_function import ObjectiveFunction
from cify.core.base_classes.collection import Collection
from cify.core.base_classes import Algorithm
from cify.ec.utils import get_population
from cify.ec.de.trial_vectors import default_trial_vector
from cify.ec.operators.crossover import binomial_crossover
from cify.ec.operators.selection import elitism_selection


class DE(Algorithm):
    """
    Defines a generic differential evolution :class:`Algorithm`.
    """

    def __init__(
            self,
            obj_func: ObjectiveFunction,
            populations: List[Collection] = None,
            n_individuals: int = 50,
            trial_vector_operator=None,
            trial_vector_params: dict = None,
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
        :param trial_vector_operator: The operator to use for calculating trial vectors,
                                      defaults to ``default_trial_vector``.
        :type trial_vector_operator: function, optional
        :param trial_vector_params: Additional parameters for the trial vector operator.
        :type trial_vector_params: dict, optional
        :param crossover_operator: The operator to use for crossover, defaults to binomial crossover.
        :type crossover_operator: function, optional
        :param crossover_params: Additional parameters for the crossover operator.
        :type crossover_params: dict, optional
        :param selection_operator: The operator to use for selection, defaults to elitism selection.
        :type selection_operator: function, optional
        :param selection_params: Additional parameters for the selection operator.
        :type selection_params: dict, optional
        """

        # must supply obj_func and (population or n_individuals)
        super().__init__(obj_func, **kwargs)

        # Create populations
        self.populations = []
        if populations is not None:
            self.populations = populations
        else:
            self.populations.append(
                get_population(n_individuals, n_dimensions=obj_func.n_dimensions, obj_func=obj_func)
            )

        # Trial vector
        if trial_vector_operator is None:
            self.trial_vector_operator = default_trial_vector
        else:
            self.trial_vector_operator = trial_vector_operator
        if trial_vector_params is None:
            self.trial_vector_params = dict()
        else:
            self.trial_vector_params = trial_vector_params

        # Crossover
        if crossover_operator is None:
            self.crossover_operator = binomial_crossover
        else:
            self.crossover_operator = crossover_operator
        if crossover_params is None:
            self.crossover_params = dict()
        else:
            self.crossover_params = crossover_params

        # Selection
        if selection_operator is None:
            self.selection_operator = elitism_selection
        else:
            self.selection_operator = selection_operator
        if selection_params is None:
            self.selection_params = dict()
        else:
            self.selection_params = selection_params

        self.global_optimum_pos = self.populations[0][0].chromosome

    def do_iteration(self):
        """Performs a single iteration of the :class:`Algorithm`."""
        next_generations = []
        for population in self.populations:
            next_generation = []
            trial_vector_operator, crossover_operator, selection_operator, \
                trial_vector_params, crossover_params, selection_params = self.__get_components(population)
            for i in range(len(population)):

                # create trial vector
                trial_vector = trial_vector_operator(population, population[i], **trial_vector_params)

                # crossover
                offspring = crossover_operator([population[i], trial_vector], **crossover_params)

                # selection
                offspring = selection_operator([population[i], offspring], **selection_params)[0]
                if self.obj_func.cmp(offspring.chromosome.value, population[i].chromosome.value):
                    next_generation.append(offspring)
                else:
                    next_generation.append(population[i])

            next_generations.append(next_generation)

        stats_collections = copy.deepcopy(self.populations)
        self.populations = next_generations
        return stats_collections

    def __get_components(self, collection: Collection) -> tuple:
        """
        Returns the appropriate components to use based on whether the given collection contains any as attributes.

        :param collection: The :class:`Collection`, in other words population, to get components from.
        :type collection: :class:`Collection`
        """
        trial_vector_operator = self.trial_vector_operator
        trial_vector_params = self.trial_vector_params
        crossover_operator = self.crossover_operator
        crossover_params = self.crossover_params
        selection_operator = self.selection_operator
        selection_params = self.selection_params

        # Set components in order of priority.
        if hasattr(collection, 'trial_vector_operator'):
            trial_vector_operator = collection.trial_vector_operator
        if hasattr(collection, 'trial_vector_params'):
            trial_vector_params = collection.trial_vector_params

        if hasattr(collection, 'crossover_operator'):
            crossover_operator = collection.crossover_operator
        if hasattr(collection, 'crossover_params'):
            crossover_params = collection.crossover_params

        if hasattr(collection, 'selection_operator'):
            selection_operator = collection.selection_operator
        if hasattr(collection, 'selection_params'):
            selection_params = collection.selection_params

        return trial_vector_operator, crossover_operator, selection_operator, \
               trial_vector_params, crossover_params, selection_params
