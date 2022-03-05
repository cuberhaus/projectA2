import networkx as nx
import matplotlib.pyplot as plt

# To create an empty undirected graph
g = nx.Graph()

# Add nodes

g.add_nodes_from([0,1,2,3,4,5,6,7,8])

nx.draw(g)
plt.savefig("graph.png")
