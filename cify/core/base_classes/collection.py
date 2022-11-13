import copy

import pandas as pd
from abc import ABC
from typing import List
from cify.core.base_classes.agent import Agent, fields

__all__ = ['Collection']


class Collection(ABC):
    """
    A :class:`Collection` stores a list of :class:`Agent` s with possible additional parameters.
    Storing :class:`Agent` s in a :class:`Collection` allows for containerising parameters that are to be
    used by all the :class:`Agent` s in the :class:`Collection`. For example, a swarm of particles, represented
    as a :class:`Collection` of :class:`Particle` 's, can have a custom velocity update function with its own set
    of parameters to be used in a multi-population optimization algorithm. All collection based algorithms
    such as those found in evolutionary computation and swam intelligence make use of :class:`Collection` s of
    :class:`Agent` s.
    """

    def __init__(self, agents: List[Agent] = None, **kwargs):
        """
        :param agents: A list of :class:`Agent` s stored in this :class:`Collection`.
        :type agents: list of :class:`Agent` s
        :param **kwargs: Additional parameters such as custom components.
        """
        if agents is None:
            self.agents = list()
        else:
            self.agents = agents
        self.__dict__.update(kwargs)

    # --------------------------------- Methods --------------------------------

    def copy(self):
        """Returns a deep copy of the :class:`Collection`."""
        return copy.deepcopy(self)

    def to_list(self) -> list:
        """
        Returns a list representation of the :class:`Collection`.

        :return: A list of the :class:`Agent` s stored in this :class:`Collection`.
        :rtype: list
        """
        return self.agents

    def to_dataframe(self) -> pd.DataFrame:
        """
        Returns the :class:`Collection` represented as a Pandas :class:`DataFrame` where each row is an :class:`Agent`
        and each column is an :class:`Agent`'s attribute.

        :return: A Pandas :class:`DataFrame` representing the :class:`Collection`.
        :rtype: Pandas :class:`DataFrame`
        """
        df = pd.DataFrame(columns=fields)
        for agent in self.agents:
            df = pd.concat([df, agent.to_series().to_frame().T], ignore_index=True)
        return df

    def set_agents(self, agents: List[Agent]):
        """
        Adds all agents to the :class:`Collection`.

        :param agents: The :class:`Agent` s to place in this :class:`Collection`.
        :type agents: A list of :class:`Agent` s
        """
        for agent in agents:
            self.add_agent(agent)

    def add_agent(self, agent):
        """
        Adds an :class:`Agent` to the list of agents belonging to this :class:`Collection`.

        :param agent: The :class:`Agent` to add.
        :type agent: `Agent`
        """
        self.agents.append(agent)

    def remove_agent(self, agent):
        """
        Removes an :class:`Agent` from the list of agents belonging to this :class:`Collection`.

        :param agent: The :class:`Agent` to remove.
        :type agent: :class:`Agent`
        """
        self.agents.remove(agent)

    def append(self, agent):
        """A wrapper for the ``add_agent`` method."""
        if isinstance(agent, Agent):
            self.add_agent(agent)
        else:
            for a in agent:
                self.add_agent(a)

    def remove(self, agent):
        """A wrapper for the ``remove_agent`` method."""
        if isinstance(agent, Agent):
            self.remove_agent(agent)
        else:
            for a in agent:
                self.remove_agent(a)

    def empty(self):
        """Empties the :class:`Collection` of all :class:`Agent` s"""
        self.agents = list()

    def sum(self) -> float:
        """
        Returns the sum of the current values of all :class:`Agent` s in the :class:`Collection`.

        :return: The sum
        :rtype: float
        """
        values = 0.
        for agent in self.agents:
            if agent.value is not None:
                values += agent.value
        return values

    def max(self) -> Agent:
        """
        Returns the maximum valued :class:`Agent` in the :class:`Collection`.

        :return: The max :class:`Agent` value.
        :rtype: :class:`Agent`
        """
        max_value = 0
        max_agent = self.agents[0]
        for agent in self.agents:
            if agent.value is not None and agent.value > max_value:
                max_agent = agent
                max_value = agent.value
        return max_agent

    def min(self) -> Agent:
        """
        Returns the minimum valued :class:`Agent` in the :class:`Collection`.

        :return: The min :class:`Agent` value.
        :rtype: :class:`Agent`
        """
        min_value = 0
        min_agent = self.agents[0]
        for agent in self.agents:
            if agent.value is not None and agent.value < min_value:
                min_agent = agent
                min_value = agent.value
        return min_agent

    # ----------------------------- Special Methods ----------------------------

    def __setitem__(self, index, data):
        if isinstance(index, str):
            for i in range(len(self.agents)):
                if self.agents[i].name == index:
                    self.agents[i] = data
        self.agents[index] = data

    def __getitem__(self, index):
        if isinstance(index, str):
            for agent in self.agents:
                if agent.name == index:
                    return agent
        return self.agents[index]

    def __len__(self):
        return len(self.agents)

    def __add__(self, other):
        agents = self.agents.copy()
        for agent in other:
            agents.append(agent)
        concat = self.copy()
        concat.agents = agents
        return concat

    def __eq__(self, other):
        if self.agents == other.agents and self.__dict__ == other.__dict__:
            return True
        return False

    def __str__(self):
        string = ''
        for agent in self.agents:
            string += agent.__str__()
        return string

    def __next__(self):
        return next(iter(self.agents))
