import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

print("Write the number of nodes:")
Nnodes = int(input())
print("Probabilitat d'arestes:")
prob = float(input())
print("Graph dirigit?: 0/1 ")
dirigit = int(input())
seed = random.seed()
# seed = 1

# To create an empty undirected graph
g = nx.Graph()
g = nx.binomial_graph(Nnodes,prob,seed, dirigit)
# Add nodes

# g.add_nodes_from([0,1,2,3,4,5,6,7,8])

nx.draw(g)
plt.savefig("graph.png")
