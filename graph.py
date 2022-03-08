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
    # print("Probabilitat d'arestes:")
    # prob = float(input())
    print("Graph dirigit?: 0/1 ")
    dirigit = int(input())
    # To create an empty undirected graph
    # biGraph = nx.Graph()

    # By default seed=None uses global
    if not os.path.isdir(directory_path + "/binomial_graph") :
        os.mkdir(directory_path + "/binomial_graph")
    f = open(directory_path + "/binomial_graph/binomial_graph_analysis.txt", "w")

    times = 100
    f.write("Sample size: " + str(times) + "\n")
    for Nnodes in np.linspace(20,100,5):
        for prob in np.linspace(0,1,51):
            nconnected = 0
            for time in range(times):
                Nnodes2 = int(Nnodes)
                biGraph = nx.binomial_graph(Nnodes2,prob,directed = dirigit) # A.k.a. Erdos-Rényi graph

                if nx.is_connected(biGraph):
                    nconnected = nconnected +1

                # nx.draw(biGraph)
                # plt.savefig(directory_path + "/binomial_graph/" + str(x) + ".png")
                # plt.clf()
                biGraph.clear()
            pconnected = nconnected /times
            f.write("Nodes: " + str(Nnodes2) +  " Probability edge: " + str(prob) + " Connected probability: " + str(pconnected) + "\n")
    f.close()

def random_geometric_graph():
    # print("Graph's radius [0..2]")
    # radius = float(input())
    # radius = 2*random.random()
    # geoGraph = nx.Graph()
    if not os.path.isdir(directory_path + "/random_geometric_graph") :
        os.mkdir(directory_path + "/random_geometric_graph")
    f = open(directory_path + "/random_geometric_graph/random_geometric_graph_analysis.txt", "w")
    times = 100
    f.write("Sample size: " + str(times) + "\n")
    for Nnodes in np.linspace(20,100,5):
        for radius in np.linspace(0,math.sqrt(2),51):
            nconnected = 0
            for time in range(times):
                Nnodes2 = int(Nnodes)
                geoGraph = nx.random_geometric_graph(Nnodes2, radius)
                if nx.is_connected(geoGraph):
                    nconnected = nconnected +1
                # nx.draw(geoGraph)
                # plt.savefig(directory_path + "/random_geometric_graph/" + "radi:"+str(radius) + "intent:"+str(time) + ".png")
                # plt.clf()
                geoGraph.clear()
            pconnected = nconnected /times
            f.write("Nodes: " + str(Nnodes2) +  " Minimum distance: " + str(radius) + " Connected probability: " + str(pconnected) + "\n")
    f.close()

def node_percolation(G):
    print("p:")
    p = float(input())
    if not os.path.isdir(directory_path + "/percolation") :
        os.mkdir(directory_path + "/percolation")

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))
    nx.draw(G)
    plt.savefig(directory_path + "/percolation/" + "graph1" + ".png")
    plt.clf()
    
    print("----Node Percolation-----")
    for i in range(G.number_of_nodes()):
        if random.random()>p:
            G.remove_node(i)

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))
    nx.draw(G)
    plt.savefig(directory_path + "/percolation/" + "graph2" + ".png")
    plt.clf()


def edge_percolation(G):
    print("p:")
    p = float(input())
    if not os.path.isdir(directory_path + "/percolation") :
        os.mkdir(directory_path + "/percolation")

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))
    nx.draw(G)
    plt.savefig(directory_path + "/percolation/" + "graph1" + ".png")
    plt.clf()
    
    print("----Edge Percolation-----")
    for i in G.edges():
        if random.random()>p:
            G.remove_edge(*i)

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))
    nx.draw(G)
    plt.savefig(directory_path + "/percolation/" + "graph2" + ".png")
    plt.clf()

selection = readOption()
if selection == 1:
    binomial_graph()
elif selection == 2:
    random_geometric_graph()
else:
    print("That's not a valid option")

# Add nodes
# g.add_nodes_from([0,1,2,3,4,5,6,7,8])
