import numpy as np
from math import factorial
import pickle
from itertools import permutations as permute
from time import time
from util import *


def time_this(f):
    """
    Decorator to time the execution of a fuction
    :param f: function to time
    :return:
    """
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        print('Execution time: {:.4f} sec'.format(time()-start))
        return result
    return wrapper


def get_graph(n):
    """
    Get the weighted, directed graph representation of all permutations of length n in the form of a nested dictionary
    {perm1 : {perm2 : distance_1_2, perm3 : distance_1_3, ...},
     perm2 : {perm1 : distance_2_1, ... etc}
    :param n: 1..n to define all permutations
    :return: graph representation
    """
    graph = {}
    permutations = get_permutations(n)
    for i, permutation in enumerate(permutations):
        connections = {}
        for other_permutation in permutations[:i] + permutations[i+1:]:
            connections[other_permutation] = distance_between(permutation, other_permutation)
        graph[permutation] = connections
    return graph


def distance_between(p1, p2):
    """
    compute distance between permutation 1 and 2, in the sense of how many characters to append to permutation 1
    to have the string contain permutation 2
    example: '123' -> '321': we can add '21' to the first permutation to include the second, therefore distance = 2
    :param p1: permutation 1
    :param p2: permutation 2
    :return: distance between 1 and 2
    """
    assert len(p1) == len(p2)
    for i in range(len(p1)):
        if p1[i:] == p2[:len(p1)-i]:
            return i
    return len(p1)


def recursive_superpermutation(n):
    """
    Common recursive algorithm to find superpermutation of length n
    :param n:
    :return:
    """
    if n == 1:  # base case
        return SYMBOLS[0]
    n_min_1 = recursive_superpermutation(n-1)  # previous superpermutation
    superperm = ''  # initialise current superpermutation
    visited = 0  # keep track of how many of the previous n's permutations have been visited
    i = 0
    nr_permutations = factorial(n-1)
    while visited < nr_permutations:  # need to contain all permutations
        split = n_min_1[i:i+(n-1)]
        if is_permutation(split, n-1):
            visited += 1
            superperm = merge(superperm, split + SYMBOLS[n-1] + split)
        i += 1  # iterate to next permutation in previous superpermutation
    return superperm


@time_this
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
            del graph[p][current]
        current = next_vertex

    path.append(current)  # add final node to graph
    return path


def path_to_string(path):
    """
    Create a Superpermutation string from a graph path
    :param path: list of permutations in order of visiting
    :return: Superpermutation string by collapsing the path with the most overlap
    """
    string = path[0]
    for perm in path[1:]:
        string = merge(string, perm)
    return string


if __name__ == '__main__':

    # n = 7
    # print('Loading or creating graph for n =', n)
    #
    # try:
    #     with open('Graphs/n{}_graph.p'.format(n), 'rb') as f:
    #         g_n = pickle.load(f)
    # except FileNotFoundError:
    #     g_n = get_graph(n)
    #     with open('Graphs/n{}_graph.p'.format(n), 'wb') as f:
    #         pickle.dump(g_n, f)
    #
    # print('Applying greedy search to graph')
    # n_path = greedy_tsp_search(g_n)
    # n_string = path_to_string(n_path)
    # assert check_string(n, n_string)
    # print('Superpermutation for n = {} found with length {}.\
    # \n{}'.format(n, len(n_string), n_string))

    start = time()
    recursive_n8 = recursive_superpermutation(9)
    print(time()-start)
    # print(is_palindrome(recursive_n8))
    print('n=? from recursive algorithm: {}\nlength: {}'.format(recursive_n8, len(recursive_n8)))
