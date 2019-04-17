from superpermutations import *
from networkx_test import *

n = 7
print("n =", n)
# Thijs implementation
start = time()
thijs_graph = get_adjacency_matrix(n)
print('Thijs graph constructed in {} sec'.format(time()-start))

start = time()
thijs_superperm = path_to_string(greedy_tsp_search(thijs_graph))
print("Thijs greedy search completed in {} sec\n".format(time()-start))

assert "Not a valid superpermutation", check_string(n, thijs_superperm)


# Networkx implementaion
start = time()
permutations = get_permutations(n)
edges = get_edges(permutations)

graph = nx.DiGraph()
graph.add_weighted_edges_from(edges)
print("networkx graph constructed in {} sec".format(time()-start))

start = time()
superperm = path_to_string(greedy_networkx(graph))
print("networkx greedy search completed in {} sec".format(time() - start))
assert "Not a valid superpermutation", check_string(n, superperm)
