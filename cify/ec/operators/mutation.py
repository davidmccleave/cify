from cify.core.utils import get_position_vector
from cify.ec.individual import Individual
from cify.ec.operators import uniform_crossover
from cify.global_constants import get_rng

# mutation operators
# NOTE: mutation happens in place.

__all__ = ['uniform_mutation', 'random_mutation', 'inorder_mutation', 'headless_chicken_mutation']


# ==============================================================================
#                               Supplied Operators
# ==============================================================================


def uniform_mutation(individual: Individual,
                     mutation_probability: float = 0.5,
                     mutation_range: float = 1.0,
                     discrete_values: list = None,
                     **kwargs):
    """
    Performs uniform mutation.

    :param individual: The individual to mutate.
    :type individual: :class:`Individual`
    :param mutation_probability: The probability of mutation at any point in the individual's chromosome,
    defaults to 0.5
    :type mutation_probability: float, optional
    :param mutation_range: The upper limit of the mutation that can be applied in either direction to a feature of the
    individual's chromosome, defaults to 1.0
    :type mutation_range: float, optional
    :param discrete_values: A list of discrete values with equal likelihood of being chosen to use in place of a
    random floating point value. Mutation will not result in the current value being replaced by itself, it will always
    pick a value different to the value at the current position in the individual's chromosome.
    :type discrete_values: list, optional

    :return: The mutated individual.
    :rtype: :class:`Individual`
    """
    if discrete_values:
        for idx in range(len(individual.chromosome.vector)):
            if get_rng().uniform() < mutation_probability:
                value = get_rng().choice(discrete_values, replace=True)
                while value == individual.vector[idx]:
                    value = get_rng().choice(discrete_values, replace=True)
                individual.chromosome.vector[idx] = value
        return individual
    else:
        for idx in range(len(individual.chromosome.vector)):
            if get_rng().uniform() < mutation_probability:
                decision = get_rng().choice([0, 1], replace=True)
                if decision == 0:
                    individual.chromosome.vector[idx] = individual.chromosome.vector[idx] \
                                                        + mutation_range * get_rng().random()
                elif decision == 1:
                    individual.chromosome.vector[idx] = individual.chromosome.vector[idx] \
                                                        - mutation_range * get_rng().random()
        return individual


def random_mutation(individual: Individual,
                    mutation_probability: float = 0.5,
                    mutation_range: float = 0.5,
                    discrete_values: list = None,
                    **kwargs):
    """
    Performs random uniform mutation. A wrapper for the uniform mutation operator.

    :param individual: The individual to mutate.
    :type individual: :class:`Individual`
    :param mutation_probability: The probability of mutation at any point in the individual's chromosome,
    defaults to 0.5
    :type mutation_probability: float, optional
    :param mutation_range: The upper limit of the mutation that can be applied in either direction to a feature of the
    individual's chromosome, defaults to 1.0
    :type mutation_range: float, optional
    :param discrete_values: A list of discrete values with equal likelihood of being chosen to use in place of a
    random floating point value. Mutation will not result in the current value being replaced by itself, it will always
    pick a value different to the value at the current position in the individual's chromosome.
    :type discrete_values: list, optional

    :return: The mutated individual.
    :rtype: :class:`Individual`
    """
    return uniform_mutation(individual, mutation_probability, mutation_range, discrete_values, **kwargs)


def inorder_mutation(individual: Individual,
                     mutation_probability: float = 0.5,
                     mutation_range: float = 1.0,
                     range_: tuple = None,
                     discrete_values: list = None,
                     **kwargs):
    """
    Performs random inorder mutation.

    :param individual: The individual to mutate.
    :type individual: :class:`Individual`
    :param mutation_probability: The probability of mutation at any point in the individual's chromosome, defaults to 0.5
    :type mutation_probability: float, optional
    :param mutation_range: The upper limit of the mutation that can be applied in either direction to a feature of the individual's chromosome, defaults to 1.0
    :type mutation_range: float, optional
    :param range_: The range within the chromosome to mutate, defaults to the entire chromosome. For example,
    supplying (3, 8) will result in only the genes within this range having a chance of being mutated.
    :type range_: tuple, optional
    :param discrete_values: A list of discrete values with equal likelihood of being chosen to use in place of a
    random floating point value. Mutation will not result in the current value being replaced by itself, it will always
    pick a value different to the value at the current position in the individual's chromosome.
    :type discrete_values: list, optional
    :return: The mutated individual.
    :rtype: :class:`Individual`
    """
    if range_ is None:
        range_ = (0, individual.obj_func.n_dimensions - 1)
    if discrete_values:
        for idx in range(range_[0], range_[1]):
            if get_rng().uniform() < mutation_probability:
                value = get_rng().choice(discrete_values, replace=True)
                while value == individual.vector[idx]:
                    value = get_rng().choice(discrete_values, replace=True)
                individual.chromosome.vector[idx] = value
        return individual
    else:
        for idx in range(range_[0], range_[1]):
            if get_rng().uniform() < mutation_probability:
                decision = get_rng().choice([0, 1], replace=True)
                if decision == 0:
                    individual.chromosome.vector[idx] = individual.chromosome.vector[idx] \
                                                        + mutation_range * get_rng().random()
                elif decision == 1:
                    individual.chromosome.vector[idx] = individual.chromosome.vector[idx] \
                                                        - mutation_range * get_rng().random()
        return individual


def headless_chicken_mutation(individual: Individual,
                              crossover_operator=uniform_crossover,
                              crossover_params: dict = None,
                              discrete_values: list = None,
                              **kwargs):
    """
    Performs headless chicken mutation.

    :param individual: The individual to mutate.
    :type individual: :class:`Individual`
    :param crossover_operator: The crossover operator to use, defaults to ``uniform_crossover``.
    :type crossover_operator: function, optional
    :param crossover_params: Any additional parameters to pass to the crossover operator, defaults to None.
    :type crossover_params: dict, optional
    :param discrete_values: A list of discrete values with equal likelihood of being chosen to use in place of a
    random floating point value. Mutation will not result in the current value being replaced by itself, it will always
    pick a value different to the value at the current position in the individual's chromosome.
    :type discrete_values: list, optional

    :return: The mutated individual.
    :rtype: :class:`Individual`
    """
    if crossover_params is None:
        crossover_params = dict()

    # generate random individual
    random_individual = []
    if discrete_values is not None:
        for i in range(len(individual.chromosome.vector)):
            random_individual.append(get_rng().choice(discrete_values))
    else:
        random_individual = Individual(get_position_vector(individual.obj_func, as_position=False),
                                       obj_func=individual.obj_func)
    individual.chromosome.vector = crossover_operator([random_individual, individual], **crossover_params)[0].vector
    return individual
