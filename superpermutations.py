from time import time
from bisect import insort
from util import *
from edge import *
import numpy as np
from ant import *


def time_this(f):
    """
    Decorator to time the execution of a fuction
    :param f: function to time
    :return:
    """

    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        print('Execution time: {:.4f} sec'.format(time() - start))
        return result

    return wrapper


def get_adjacency_matrix(n):
    """
    Get the adjacency matrix corresponding to the graph of permutations. The values in the matrix are the weights
    of the edges between two permutations (see util.distance_between)
    :param n: 1..n to define all permutations
    :return: adjacency matrix representation of graph
    """
    matrix = {}
    permutations = get_permutations(n)
    for permutation in permutations:
        connections = {}
        for other_permutation in permutations:
            if proper_edge(permutation, other_permutation):
                weight = distance_between(permutation, other_permutation)
                connections[other_permutation] = (weight, 0)
        matrix[permutation] = connections
    return matrix


def get_adjacency_list(n):
    """
    Get adjacency list of all proper edges between permutations of length n
    :param n:
    :return:
    """
    adjacency_list = []
    permutations = get_permutations(n)
    for permutation in permutations:
        for other_permutation in permutations:
            # if proper_edge(permutation, other_permutation):
                weight = distance_between(permutation, other_permutation)
                edge = Edge(permutation, other_permutation, weight, 1)
                insort(adjacency_list, edge)
    return adjacency_list


def recursive_superpermutation(n):
    """
    Common recursive algorithm to find superpermutation of length n
    :param n:
    :return:
    """
    if n == 1:  # base case
        return SYMBOLS[0]
    n_min_1 = recursive_superpermutation(n - 1)  # previous superpermutation
    superperm = ''  # initialise current superpermutation
    visited = 0  # keep track of how many of the previous n's permutations have been visited
    i = 0
    nr_permutations = factorial(n - 1)
    while visited < nr_permutations:  # need to contain all permutations
        split = n_min_1[i:i + (n - 1)]
        if is_permutation(split, n - 1):
            visited += 1
            superperm = merge(superperm, split + SYMBOLS[n - 1] + split)
        i += 1  # iterate to next permutation in previous superpermutation
    return superperm


# @time_this
def greedy_tsp_search(graph):
    """
    Greedy search for a Hamiltonian path through the graph (traveling salesman style)
    :param graph:
    :return:
    """
    current = list(graph.keys())[0]  # start with first permutation
    path = []
    while len(graph) > 1:
        path.append(current)  # add current permutation to path
        #  find next node with shortest path
        next_vertex = min(graph[current], key=graph[current].get)
        del graph[current]  # remove current from the graph
        for p in list(graph.keys()):
            if current in graph[p]:
                del graph[p][current]
        current = next_vertex
    path.append(current)  # add final node to graph
    return path


def solve_ACO(adj_list):
    epochs = 10
    Ant.graph = adj_list
    Ant.alpha = .8
    Ant.beta = .3
    ants = []

    for _ in range(50):
        ants.append(Ant())

    for i in range(epochs):
        for ant in ants:
            ant.create_tour()
        pheromone_update(Ant.graph, ants, 0.025)

    ants.sort(key=lambda a: a.tour_distance)

    return ants


if __name__ == '__main__':
    n = 4
    print("n =", n)
    start = time()
    adj_list = get_adjacency_list(n)
    print("list formed in {} secs".format(time() - start))
    # print(adj_list[0] < adj_list[1])
    ants = solve_ACO(adj_list)
    print(ants[0])
    # superperm = path_to_string(path)
    # print(superperm)
    # print(len(superperm))
    # assert check_string(n, superperm)

