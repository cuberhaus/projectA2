import networkx as nx
import matplotlib.pyplot as plt
import random
import os

directory_path = os.getcwd()

def readOption():
    print("Select your option:\n"
          "1- binomial_graph\n"
          "2- random_geometric_graph")
    return int(input())

def readNnodes():
    print("Write the number of nodes:")
    return int(input())

def binomial_graph(Nnodes):
    print("Probabilitat d'arestes:")
    prob = float(input())
    print("Graph dirigit?: 0/1 ")
    dirigit = int(input())
    # To create an empty undirected graph
    # biGraph = nx.Graph()

    # By default seed=None uses global
    os.mkdir(directory_path + "/binomial_graph") 
    for x in range(3):
        biGraph = nx.binomial_graph(10,prob,directed = dirigit) # A.k.a. Erdos-Rényi graph

        # connected = nx.is_connected(biGraph)
    
        nx.draw(biGraph)
        plt.savefig(directory_path + "/binomial_graph/" + str(x) + ".png")


def random_geometric_graph(Nnodes):
    print("Graph's radius [0..2]")
    radius = float(input())
    # radius = 2*random.random()
    # geoGraph = nx.Graph()
    os.mkdir(directory_path + "/random_geometric_graph") 
    for x in range(3):
        geoGraph = nx.random_geometric_graph(Nnodes, radius)
        nx.draw(geoGraph)
        plt.savefig(directory_path + "/random_geometric_graph/" + str(x) + ".png")

while(True):
    print(directory_path)
    selection = readOption()
    Nnodes = readNnodes()
    if selection == 1:
        binomial_graph(Nnodes)
    elif selection == 2:
        random_geometric_graph(Nnodes)
    else:
        print("That's not a valid option")

# Add nodes
# g.add_nodes_from([0,1,2,3,4,5,6,7,8])
