import numpy as np
import random
# bisect_left(list, element) gives index of first occurence of element in list
# bisect_right(list, element) gives index+1 of last occurence of element in list
from bisect import bisect_left, bisect_right


class Ant:
    # static
    graph = None  # graph on which to create a tour: list of [start_node, end_node, distance, pheromone]
    start_nodes = None  # list of all first elements of the graph [x[0] for x in graph]
    alpha = None  # paramater to control influence of pheromone
    beta = None  # parameter to control influence of heuristic information (distance)

    # instance
    current_node = None
    visited = None
    edge_list = None
    tour_distance = None  # total accumulative distance of tour

    def __init__(self):
        # assert global variables are set
        assert Ant.graph is not None, "graph is None"
        assert Ant.alpha is not None, "alpha is None"
        assert Ant.beta is not None, "beta is None"
        if Ant.start_nodes is None:
            Ant.start_nodes = [edge.start_node for edge in self.graph]

        self.reset()

    def __str__(self):
        return "length {}, tour {}".format(self.tour_distance, self.visited)

    def reset(self):
        self.current_node = random.choice(self.graph).start_node  # random starting point
        self.visited = [self.current_node]
        self.edge_list = []
        self.tour_distance = 0

    def create_tour(self):
        # initialize neighbours of current node: slice from graph where starting node is current node
        neighbours = self.graph[bisect_left(self.start_nodes, self.current_node):
                                bisect_right(self.start_nodes, self.current_node)]
        # exclude visited destinations
        neighbours = [edge for edge in neighbours if edge.end_node not in self.visited]
        # print(self.graph)
        # while there are still nodes to be visited, continue creating the tour
        while len(neighbours) > 0:
            # define probabilities for each connected edge
            probs = [(edge.pheromone ** self.alpha * (1/edge.distance) ** self.beta) for edge in neighbours]
            probs = list(np.true_divide(probs, sum(probs)))
            # print('current', self.current_node)
            # print('neighbours', neighbours)
            # print('probs', probs)

            next_idx = np.random.choice(range(len(neighbours)), 1, p=probs)[0]
            self.current_node = neighbours[next_idx].end_node

            self.visited.append(self.current_node)
            self.edge_list.append(neighbours[next_idx])
            self.tour_distance += neighbours[next_idx].distance

            neighbours = self.graph[bisect_left(self.start_nodes, self.current_node):
                                    bisect_right(self.start_nodes, self.current_node)]
            neighbours = [edge for edge in neighbours if edge.end_node not in self.visited]

        # print(self.visited)


def pheromone_update(graph, ants, p):
    """
    update the pheromone levels of the ants in the graph
    :param graph: adjacency list
    :param ants: list of all ants traversing the graph
    :param p: pheromone decay 0 < p <= 1
    :return:
    """
    assert 0 < p <= 1, "Illegal value for pheromone decay"
    # decay
    for edge in graph:
        edge.pheromone *= (1-p)
    # increase
    for ant in ants:
        for edge in ant.edge_list:
            edge.pheromone += 1/ant.tour_distance
    return graph
