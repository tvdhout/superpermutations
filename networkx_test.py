import networkx as nx
from util import *
from time import time


def get_edges(perms):
    """
    get weighted edges in the form (v1, v2, weight) between all permutations
    :param perms: permutations to compute edges for
    :return: list of edges
    """
    edges = []
    for p in perms:
        for p_other in perms:
            if p != p_other:
                edges.append((p, p_other, distance_between(p, p_other)))
    return edges


def greedy_networkx(graph: nx.DiGraph):
    """
    Greedy search for a Hamiltonian path through the graph (traveling salesman style)
    :param graph:
    :return:
    """
    current = list(graph.nodes)[0]  # start with first permutation
    next_node = None
    path = []

    while graph.number_of_nodes() > 0:
        path.append(current)  # add current permutation to path
        #  find next node with shortest path
        try:
            next_node = min(graph.edges(current, data=True), key=lambda e: e[2].get('weight'))[1]
        except ValueError:  # The last node has no more edges, so min() will be empty
            pass  # still add the node to the path though, so continue the code
        graph.remove_node(current)  # remove current from the graph
        current = next_node

    path.append(current)  # add final node to graph
    return path


if __name__ == '__main__':
    n = 6

    permutations = get_permutations(n)
    edges = get_edges(permutations)
