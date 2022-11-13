from cify.core.base_classes.collection import Collection
from cify.global_constants import get_rng

__all__ = ['elitism_selection', 'random_selection', 'tournament_selection', 'proportional_selection']


def elitism_selection(population: list or Collection, n_agents: int = 1, **kwargs):
    """
    Performs elitism selection on the given population.

    :param population: The population to select from.
    :type population: list, :class:`Collection`
    :param n_agents: The number of agents to return, defaults to 1
    :type n_agents: int, optional

    :return: The selected individual(s).
    :rtype: list, :class:`Collection`
    """
    if population[0].obj_func.cmp(0, 1):
        return sorted(population, key=lambda individual: individual.value)[:n_agents]
    else:
        return sorted(population, key=lambda individual: individual.value, reverse=True)[:n_agents]


def random_selection(population: list or Collection,
                     n_agents: int = None, replace: bool = False, **kwargs):
    """
    Performs random selection on the given population.

    :param population: The population to select from.
    :type population: list, :class:`Collection`
    :param n_agents: The number of agents to return, defaults to the length of the population.
    :type n_agents: int, optional
    :param replace: Whether to sample with replacement or not, defaults to False. (does not replace selected individuals)
    :type replace: bool, optional

    :return: The selected individual(s).
    :rtype: list, :class:`Collection`
    """
    if n_agents is None:
        n_agents = len(population)

    if isinstance(population, Collection):
        choice = get_rng().choice(population, size=n_agents, replace=replace).tolist()
        population.empty()
        population.set_agents(choice)
        return population
    return get_rng().choice(population, size=n_agents, replace=replace)


def proportional_selection(population: list or Collection,
                           n_agents: int = None, replace: bool = False, **kwargs):
    """
    Performs proportional selection on the given population.
    Proportional selection is similar to random selection, except that a probability distribution
    proportional to the fitness of each individual is used to determine the likelihood of sampling an individual.
    The formula used to determine this distribution is given below:

    .. math::

        \\varphi(\\mathbf{x_i}(t)) = \\frac{f_{\\Upsilon}(\\mathbf{x_it}(t))}{\\sum_{I=1}^{n_s} f_{\\Upsilon}(\\mathbf{x_i}(t))}

    :param population: The population to select from.
    :type population: list, :class:`Collection`
    :param n_agents: The number of agents to return, defaults to the length of the population.
    :type n_agents: int, optional
    :param replace: Whether to sample with replacement or not, defaults to False. (does not replace selected individuals)
    :type replace: bool, optional

    :return: The selected individual(s).
    :rtype: list, :class:`Collection`
    """
    if n_agents is None:
        n_agents = len(population)

    vals = list()
    for individual in population:
        vals.append(individual.chromosome.value)
    _sum = sum(vals)
    probs = [x / _sum for x in vals]

    return get_rng().choice(population, size=n_agents, replace=replace, p=probs)


def tournament_selection(population: list or Collection, n_agents: int = None, t_size: int = 3,
                         replace: bool = False, **kwargs):
    """
    Performs tournament selection on the given population. This operator is recommended for good overall performance.

    :param population: The population to select from.
    :type population: list, :class:`Collection`
    :param n_agents: The number of agents to return, defaults to the length of the population.
    :type n_agents: int, optional
    :param t_size: The size of the tournament, defaults to 3
    :type t_size: int, optional
    :param replace: Whether to sample with replacement or not, defaults to False.
    (does not replace selected individuals)
    :type replace: bool, optional

    :return: The selected individual(s).
    :rtype: list, :class:`Collection`
    """
    if n_agents is None:
        n_agents = len(population)

    selected_population = []
    while len(selected_population) < n_agents:
        tournament = get_rng().choice(population, size=t_size, replace=replace)
        selected_population.append(elitism_selection(tournament, n_agents=1)[0])

    if isinstance(population, Collection):
        sp = population.copy()
        sp.empty()
        sp.set_agents(selected_population)
        return sp
    return selected_population
