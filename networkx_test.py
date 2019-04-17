import networkx as nx
from util import *

graph = nx.DiGraph()
graph.add_nodes_from(get_permutations(3))

print(graph.nodes)