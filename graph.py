import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import numpy as np
import math

directory_path = os.getcwd()

def readOption():
    print("Select your option:\n"
          "1- binomial_graph\n"
          "2- random_geometric_graph")
    return int(input())

def readNnodes():
    print("Write the number of nodes:")
    return int(input())

def binomial_graph():
    print("Probabilitat d'arestes:")
    # prob = float(input())
    print("Graph dirigit?: 0/1 ")
    dirigit = int(input())
    # To create an empty undirected graph
    # biGraph = nx.Graph()

    # By default seed=None uses global
    if not os.path.isdir(directory_path + "/binomial_graph") :
        os.mkdir(directory_path + "/binomial_graph") 
    
    times = 100
    for Nnodes in np.linspace(20,100,5):
        for prob in np.linspace(0,1,101):
            nconnected = 0
            for time in range(times):
                Nnodes2 = int(Nnodes)
                biGraph = nx.binomial_graph(Nnodes2,prob,directed = dirigit) # A.k.a. Erdos-Rényi graph

                if nx.is_connected(biGraph): 
                    nconnected = nconnected +1

                biGraph.clear()
                # nx.draw(biGraph)
                # plt.savefig(directory_path + "/binomial_graph/" + str(x) + ".png")
                # plt.clf()
            pconnected = nconnected /times
            print("Nodes: " + str(Nnodes2) +  " Probability edge: " + str(prob) + " Connected probability: " + str(pconnected))


def random_geometric_graph():
    # print("Graph's radius [0..2]")
    # radius = float(input())
    # radius = 2*random.random()
    # geoGraph = nx.Graph()
    if not os.path.isdir(directory_path + "/random_geometric_graph") :
        os.mkdir(directory_path + "/random_geometric_graph") 

    nconnected = 0
    times = 10
    for Nnodes in np.linspace(20,100,5):
        for radius in np.linspace(0,math.sqrt(2),20):
            nconnected = 0
            for time in range(times):
                Nnodes2 = int(Nnodes)
                geoGraph = nx.random_geometric_graph(Nnodes2, radius)
                if nx.is_connected(geoGraph): 
                    nconnected = nconnected +1
                geoGraph.clear()
                # nx.draw(geoGraph)
                # plt.savefig(directory_path + "/random_geometric_graph/" + str(x) + ".png")
                # plt.clf()
            pconnected = nconnected /times
            print("Nodes: " + str(Nnodes2) +  " Probability edge: " + str(radius) + " Connected probability: " + str(pconnected))


# while(True):
selection = readOption()
if selection == 1:
    binomial_graph()
elif selection == 2:
    random_geometric_graph()
else:
    print("That's not a valid option")

# Add nodes
# g.add_nodes_from([0,1,2,3,4,5,6,7,8])
