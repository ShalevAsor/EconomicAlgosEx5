import networkx as nx
import numpy as np


# part a
def create_replacements_graph(valuations, allocation):
    players = len(valuations)
    resources = len(valuations[0])
    graph = nx.DiGraph()
    graph.add_nodes_from(range(players))  # the nodes of the graph are the players

    for i in range(players):
        for j in range(players):
            if i != j:
                min_ratio = np.inf
                for k in range(resources):
                    if allocation[i][k] > 0:  # if this player get something from this resource
                        ratio = valuations[i][k] / max(valuations[j][k], 1)  # avoid division by zero
                        min_ratio = min(min_ratio, ratio)

                    graph.add_edge(i, j, weight=min_ratio)  # add directed edge to the graph with this min_ratio as
                    # weight of the edge

    return graph


# Return list with the products of the weights of each cycle
def cycles_weight(graph, cycles):
    weights = []
    for cycle in cycles:
        cycle_weight = calculate_cycle_weight(graph, cycle)
        weights.append(cycle_weight)
    return weights


# This function return the weight of a cycle in the graph
def calculate_cycle_weight(graph, cycle):
    weight = 1
    for i in range(len(cycle) - 1):
        source, target = cycle[i], cycle[i + 1]
        weight *= graph[source][target]['weight']
    weight *= graph[cycle[-1]][cycle[0]]['weight']  # multiply with the weight of the last edge in the cycle
    return weight


# return true iff exists a cycle with weight smaller then 1
def exists_small_weight(weights, threshold=1):
    return any(weight < threshold for weight in weights)


# The main algorithm from class for item (a)
def is_pareto_efficient(valuations, allocation) -> bool:
    g = create_replacements_graph(valuations, allocation)  # create the graph according to the partition
    cycles = list(nx.simple_cycles(g))  # get all the cycles in the graph
    weights = cycles_weight(g, cycles)  # get the weight of the cycles in the replacements graph

    return not exists_small_weight(
        weights)  # if there is a cycle with weight < 1 then this partition cannot be pareto efficient


# part b
def create_bipartite_graph(valuations, allocation) -> nx.Graph:
    players = len(valuations)
    resources = len(valuations[0])
    graph = nx.Graph()

    # Nodes on the first side represent players
    graph.add_nodes_from(range(players), bipartite=0)

    # Nodes on the second side represent resources
    graph.add_nodes_from(range(players, players + resources), bipartite=1)

    for i in range(players):
        for j in range(resources):  # edges between players to the resources they get
            if valuations[i][j] * allocation[i][j] > 0:
                graph.add_edge(i, players + j)

    return graph


def find_corresponding_cycles(rep_graph_cycles, original_cycle):
    # Find the vertices in the original cycle
    vertices = set(original_cycle)

    # Find the first cycle in the replacement graph that covers the same vertices
    matching_cycle = None
    for rep_cycle in rep_graph_cycles:
        rep_cycle_set = set(rep_cycle)
        if vertices == rep_cycle_set:
            matching_cycle = rep_cycle
            break  # Exit the loop when the first matching cycle is found

    if matching_cycle:
        # Construct the second cycle with the opposite direction of edges
        reversed_cycle = list(reversed(matching_cycle))
        return matching_cycle, reversed_cycle


# main algorithm for pat b , this is a recursive function that works according to the proof from the lecture
# This function not working
def pareto_improvement(valuations, allocation) -> list[list[float]]:
    players = len(valuations)
    resources = len(valuations[0])
    if is_pareto_efficient(valuations, allocation):
        return allocation  # its already pareto efficient , return this allocation
    else:  # this partition is not pareto efficient , we need to transfer values from the players
        bipartite_graph = create_bipartite_graph(valuations, allocation)
        cycles = list(nx.simple_cycles(bipartite_graph))  # all the cycles in the bipartite graph
        if len(cycles) == 0:  # if there are no cycles , its already pareto efficient
            return allocation
        cycle = cycles[0]  # take arbitrary cycle
        smaller_cycle = get_smaller_cycle(cycle, bipartite_graph)
        rep_graph = create_replacements_graph(valuations, allocation)  # create the replacements graph
        rep_graph_cycles = list(nx.simple_cycles(rep_graph))  # get all the cycles from this graph
        c1, c2 = find_corresponding_cycles(rep_graph_cycles,
                                           smaller_cycle)  # there are exactly two cycles corresponding to the cycle fro, rep_graph
        w1, w2 = calculate_cycle_weight(rep_graph, c1), calculate_cycle_weight(rep_graph,
                                                                               c2)  # calculate the weight and check the smaller weight
        e = 0.01
        first_round = True
        if w1 < w2:
            selected_cycle = c1
        else:
            selected_cycle = c2
        # the problem is here when iam trying to transfer values
        for i in range(len(selected_cycle) - 1):
            if i in bipartite_graph.nodes:
                for k in range(resources):
                    if first_round:
                        r = 1
                    else:
                        r = allocation[i][k]
                    if allocation[i][k] > 0 and allocation[i + 1][k] > 0:
                        small_part = valuations[i][k] * (e / r)
                        allocation[i][k] -= small_part
                        allocation[i + 1][k] += small_part

        return pareto_improvement(valuations, allocation)


def get_smaller_cycle(cycle, bipartite_graph):
    # Get the set of vertices in the first side of the bipartite graph
    first_side_vertices = set(node for node, side in bipartite_graph.nodes(data='bipartite') if side == 0)

    # filter the vertices of the cycle that are in the first side
    smaller_cycle = [vertex for vertex in cycle if vertex in first_side_vertices]

    return smaller_cycle


if __name__ == '__main__':
    """
    TODO : add tests  
    """

    # the example from class :
    val = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    alloc = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    print("Case 1:",is_pareto_efficient(val, alloc))
    val = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    alloc = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    print("Case 2 (dictator - should be true:", is_pareto_efficient(val, alloc))
    val = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    alloc = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    print("Case 3 each player get 6:", is_pareto_efficient(val, alloc))

    values1 = [[10, 20, 30, 40], [40, 30, 20, 10]]
    alloc1 = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]
    print("Case 4: the example from the assignment:",is_pareto_efficient(values1, alloc1))
    # print(is_pareto_efficient(values1, alloc1))

    # part b not working
    val = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    alloc = [[0.7, 0.7, 0], [0.3, 0.3, 0], [0, 0, 1]]
    alloc_tmp = [[0.7, 0.7, 0], [0.3, 0.3, 0], [0, 0, 1]]
    print("Case 5:","before:",alloc,"after:",pareto_improvement(val, alloc_tmp),"now its pareto efficient?",is_pareto_efficient(val,alloc_tmp))
