import numpy as np
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


def get_adjacency_matrix(n):
    """
    Get the adjacency matrix corresponding to the graph of permutations. The values in the matrix are the weights
    of the edges between two permutations (see util.distance_between)
    :param n: 1..n to define all permutations
    :return: adjacency matrix representation of graph
    """
    matrix = []
    permutations = get_permutations(n)
    for i, permutation in enumerate(permutations):
        connections = []
        for other_permutation in permutations:
            weight = distance_between(permutation, other_permutation)
            connections.append(weight) if weight > 0 else connections.append(np.inf)
        matrix.append(connections)
    return matrix


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


# @time_this
def greedy_tsp_search(matrix):
    """
    Greedy search for a Hamiltonian path through the graph (traveling salesman style)
    graph is represented as adjacency matrix
    :param matrix:
    :return: path in the form of a list of indices, visited in order
    """
    assert "matrix is None", matrix is not None
    assert "matrix is not 2d ", len(np.shape(matrix)) == 2
    assert "matrix is not square", np.shape(matrix)[0] == np.shape(matrix)[1]

    size = len(matrix)
    next_node = 0
    path = []

    visited = set()  # all indices are yet to be visited

    while len(visited) < size:
        #  find next node with shortest path
        current_node = next_node
        path.append(current_node)
        visited.add(current_node)
        try:
            next_node = next(node for node in np.argsort(matrix[current_node]) if node not in visited)
        except StopIteration:
            break  # generator empty

    return path


if __name__ == '__main__':

    n = 7
    start = time()
    matrix = get_adjacency_matrix(n)
    print("matrix formed in {} secs".format(time()-start))

    start = time()
    path = greedy_tsp_search(matrix)
    superperm = index_path_to_string(n, path)
    print("greedy search done in {} secs".format(time()-start))
    print(superperm)
