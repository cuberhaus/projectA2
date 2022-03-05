import networkx as nx
import matplotlib.pyplot as plt
import random

print("Write the number of nodes:")
Nnodes = int(input())
print("Probabilitat d'arestes:")
prob = float(input())
print("Graph dirigit?: 0/1 ")
dirigit = int(input())
seed = random.seed()
print("Graph's radius [0..2]")
radius = float(input())
# radius = 2*random.random()

# To create an empty undirected graph
biGraph = nx.Graph()
biGraph = nx.binomial_graph(Nnodes,prob,seed, dirigit) # A.k.a. Erdos-Rényi graph
geoGraph = nx.Graph()
geoGraph = nx.random_geometric_graph(Nnodes, radius,seed=seed)

# Add nodes

# g.add_nodes_from([0,1,2,3,4,5,6,7,8])

nx.draw(biGraph)
plt.savefig("random_geometric_graph.png")
nx.draw(geoGraph)
plt.savefig("binomial_graph.png")
