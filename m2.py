# This is the solution of assignment 2 in economic algorithms
from typing import Dict
from typing import List


class Agent:
    def __int__(self):
        self.options: Dict[int, float] = dict()

    def value(self, option: int) -> float:
        """
        INPUT: The index of an option
        OUTPUT: The value of the option to the agent
         """
        if self.options.get(option) is None:  # option doesnt exist
            return -1
        return self.options[option]


def isParetoImprovement(agents: List[Agent], option1: int, option2: int) -> bool:
    """

    :param agents: list of the agents
    :param option1: the index of option 1
    :param option2: the index of option 2
    :return: true iff option1 is Pareto improvement of option 2
    """
    if (option1 == option2):
        return False
    equals_counter = 0
    for agent in agents:  # check if option 1 is Pareto improvement of option 2
        if agent.value(option2) == agent.value(option1):
            equals_counter += 1
        elif agent.value(option2) > agent.value(option1):
            # if exists an agent such that option 2 value is greate then option 1 then its not Pareto improvement
            return False

    if equals_counter == len(agents):  # there is no improvement for any of the agents
        return False

    return True


def isParetoOptimal(agents: List[Agent], option: int, allOptions: List[int]) -> bool:
    """

    :param agents: list of all the agents
    :param option: index of the option
    :param allOptions:list of all available options indexes
    :return:true iff this option is pareto efficient
    """
    for curr_option in allOptions:
        if isParetoImprovement(agents, curr_option, option):  # exists Pareto improvement
            return False
    return True


if __name__ == '__main__':
    """
    TODO : add tests  
    """

