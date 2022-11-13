from cify.ec.individual import Individual
from cify.ec.operators.selection import elitism_selection
from cify.core.base_classes.collection import Collection
from cify.global_constants import get_rng

"""
NOTES:
    - asexual               (offspring from 1 parent)
    - sexual                (2 parents produce 1 or 2 offspring)
    - multi-recombination   (more than 2 parents produce 1 or 2 offspring)
"""

__all__ = ['uniform_crossover', 'npoint_crossover', 'one_point_crossover', 'two_point_crossover',
           'hillclimbing_crossover', 'linear_crossover',
           'binomial_crossover', 'exponential_crossover']


# ==============================================================================
#                              Discrete Crossover
# ==============================================================================

def uniform_crossover(parents: list or Collection,
                      n_offspring: int = 2,
                      crossover_probability: float = 0.5,
                      **kwargs) -> list or Collection:
    """
    Discrete uniform crossover. The elements in the same position are not blended in any way.

    :param parents: The parents whose chromosomes will be recombined.
    :type parents: list, :class:`Collection`
    :param n_offspring: The number of offspring to generate during crossover, defaults to 2
    :type n_offspring: int, optional
    :param crossover_probability: The probability of crossover for any position in the parents' chromosomes, defaults to 0.5
    :type crossover_probability: float, optional

    :return: The generated offspring.
    :rtype: list, :class:`Collection`
    """
    offspring = []
    vector_length = len(parents[0].vector)
    n_parents = len(parents)

    for _ in range(n_offspring):
        # Create mask
        child_vector = []
        prev_index = 0
        curr_index = prev_index
        for i in range(vector_length):
            if get_rng().uniform() < crossover_probability:
                curr_index = get_rng().choice(n_parents, replace=True)
                while curr_index == prev_index:
                    curr_index = get_rng().choice(n_parents, replace=True)
            child_vector.append(parents[curr_index].position[i])
        child = parents[0].copy()
        child.position = child_vector
        child.position.value = None
        offspring.append(child)

    return offspring


def npoint_crossover(parents: list or Collection,
                     n_offspring: int = 2,
                     n_points: int = 2,
                     **kwargs) -> list or Collection:
    """
    Discrete n-point crossover. The elements in the same position are not blended in any way.

    :param parents: The parents whose chromosomes will be recombined.
    :type parents: list, :class:`Collection`
    :param n_offspring: The number of offspring to generate during crossover, defaults to 2
    :type n_offspring: int, optional
    :param n_points: The number of recombination points, defaults to 2
    :type n_points: int, optional

    :return: The generated offspring.
    :rtype: list, :class:`Collection`
    """
    offspring = []
    vector_length = len(parents[0].vector)
    points = get_rng().choice(vector_length, size=n_points, replace=False).tolist()

    for i in range(n_offspring):
        child_vector = []
        parent_idx = min(i, len(parents) - 1)
        for index in range(vector_length):
            if index in points:
                parent_idx += 1
                if parent_idx > len(parents) - 1:
                    parent_idx = 0
            child_vector.append(parents[parent_idx].vector[index])
        child = parents[0].copy()
        child.position = child_vector
        child.position.value = None
        offspring.append(child)

    return offspring


def one_point_crossover(parents: list or Collection,
                        n_offspring: int = 2,
                        **kwargs) -> list or Collection:
    """
    Discrete one-point crossover. The elements in the same position are not blended in any way.

    :param parents: The parents whose chromosomes will be recombined.
    :type parents: list, :class:`Collection`
    :param n_offspring: The number of offspring to generate during crossover, defaults to 2
    :type n_offspring: int, optional

    :return: The generated offspring.
    :rtype: list, :class:`Collection`
    """
    return npoint_crossover(parents, n_offspring=n_offspring, n_points=1, **kwargs)


def two_point_crossover(parents: list or Collection,
                        n_offspring: int = 2,
                        **kwargs) -> list or Collection:
    """
    Discrete two-point crossover. The elements in the same position are not blended in any way.

    :param parents: The parents whose chromosomes will be recombined.
    :type parents: list, :class:`Collection`
    :param n_offspring: The number of offspring to generate during crossover, defaults to 2
    :type n_offspring: int, optional

    :return: The generated offspring.
    :rtype: list, :class:`Collection`
    """
    return npoint_crossover(parents, n_offspring=n_offspring, n_points=2, **kwargs)


def hillclimbing_crossover(parents: list or Collection,
                           n_offspring: int = 2,
                           crossover_probability: float = 0.5,
                           max_attempts: int = 5,
                           **kwargs) -> list or Collection:
    """
    Discrete hillclimbing crossover. The elements in the same position are not blended in any way.

    :param parents: The parents whose chromosomes will be recombined.
    :type parents: list, :class:`Collection`
    :param n_offspring: The number of offspring to generate during crossover, defaults to 2
    :type n_offspring: int, optional
    :param crossover_probability: The probability of crossover for any position in the parents' chromosomes, defaults to 0.5
    :type crossover_probability: float, optional
    :param max_attempts: The maximum number of attempts at recombination after which the best generated offspring
    will be returned, defaults to 5
    :type max_attempts: int, optional

    :return: The generated offspring.
    :rtype: list, :class:`Collection`
    """
    found_better = False
    count = 0
    children = parents.copy()
    while not found_better and count < max_attempts:
        children = uniform_crossover(parents, n_offspring=n_offspring, crossover_probability=crossover_probability)
        for parent in parents:
            for child in children:
                if child.obj_func.cmp(child, parent):
                    found_better = True
        count += 1
    return children

# ==============================================================================
#                      Floating-Point Crossover Operators
# ==============================================================================


# linear recombination - two parents (pp. 55)
def linear_crossover(parents: list or Collection, **kwargs):
    """
    Linear crossover for floating-point representations. This operator only accepts two parents.

    :param parents: The parents whose chromosomes will be recombined.
    :type parents: list, :class:`Collection` of length 2.

    :return: The generated offspring.
    :rtype: list, :class:`Collection`
    """
    p1 = parents[0]
    p2 = parents[1]
    o1, o2, o3 = p1.copy(), p1.copy(), p1.copy()
    o1.position.vector = p1.position.vector + p2.position.vector
    o2.position.vector = 1.5 * p1.position.vector - .5 * p2.position.vector
    o3.position.vector = -.5 * p1.position.vector + 1.5 * p2.position.vector
    return elitism_selection([o1, o2, o3], n_agents=2)


# ==============================================================================
#                                  DE Operators
# ==============================================================================


def binomial_crossover(parents: list or Collection, crossover_probability=0.5, **kwargs) -> Individual:
    """
    Performs binomial crossover between two parents. In differential evolution, the parents would be a list
    or `Collection` of iterables representing the individual (`parents[0]`) and trial vector (`parents[1]`).

    :param parents: The two parents to perform crossover on.
    :type parents: any iterable, list or Collection
    :param crossover_probability: The probability threshold for performing crossover.
    :type crossover_probability: float

    :return: A single individual that represents the combination of the two input parents.
    :rtype: :class:`Individual`
    """
    individual = parents[0]
    vector = parents[1]

    new_vector = []
    for i in range(0, len(individual.chromosome)):
        calc = get_rng().random()
        if calc <= crossover_probability:
            if isinstance(vector, Individual):
                new_vector.append(vector.chromosome[i])
            else:
                new_vector.append(vector[i])
        else:
            new_vector.append(individual.chromosome[i])

    # guarantees a random index will undergo crossover.
    vector_index = get_rng().integers(low=0, high=len(individual.chromosome))
    if isinstance(vector, Individual):
        new_vector[vector_index] = vector.chromosome[vector_index]
    else:
        new_vector[vector_index] = vector[vector_index]

    return Individual(chromosome=new_vector, obj_func=individual.obj_func)


def exponential_crossover(parents: list or Collection, crossover_probability=0.5, **kwargs) -> Individual:
    """
    Performs exponential crossover between two parents. In differential evolution, the parents would be a list
    or `Collection` of iterables representing the individual (`parents[0]`) and trial vector (`parents[1]`).

    :param parents: The two parents to perform crossover on.
    :type parents: any iterable, list or Collection
    :param crossover_probability: The probability threshold for performing crossover.
    :type crossover_probability: float

    :return: A single individual that represents the combination of the two input parents.
    :rtype: :class:`Individual`
    """
    individual = parents[0]
    vector = parents[1]

    new_vector = individual.chromosome.copy()  # J
    nx = len(individual.chromosome)
    j = (nx - 1) * get_rng().random()

    if isinstance(vector, Individual):
        while get_rng().random() < crossover_probability or len(new_vector) < nx:
            new_vector[j + 1] = vector.chromosome[j + 1]
            j = (j + 1) % nx
    else:
        while get_rng().random() < crossover_probability or len(new_vector) < nx:
            new_vector[j + 1] = vector[j + 1]
            j = (j + 1) % nx

    return Individual(chromosome=new_vector, obj_func=individual.obj_func)
