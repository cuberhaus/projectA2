from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import math

directory_path = os.getcwd()

def connectedPlot(numbersx, numbersy, xlabel, nfigure, label, directory):
    label2 = str(label) + " Nodes"
    plt.plot(numbersx, numbersy, label= label2)
    plt.ylabel('Probability that network is connected')
    plt.xlabel(xlabel)
    # plt.show() // Show plot onscreen
    if not os.path.isdir(directory_path + directory) :
        os.mkdir(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "nfigure" + str(nfigure) + ".png")
    # plt.clf() // Clear plot each time

def readOption():
    print("Select your option:\n"
          "1- percolation\n"
          "2- binomial_graph\n"
          "3- random_geometric_graph")
    return int(input())

def readNnodes():
    print("Write the number of nodes:")
    return int(input())

def binomial_graph():
    print("Graph dirigit?: 0/1 ")
    dirigit = int(input())

    if not os.path.isdir(directory_path + "/binomial_graph") :
        os.mkdir(directory_path + "/binomial_graph")
    f = open(directory_path + "/binomial_graph/binomial_graph_analysis.txt", "w")

    times = 10
    f.write("Sample size: " + str(times) + "\n")
    nplot=0
    N = [5,10,20,50,100,500,1000]
    # for Nnodes in np.linspace(20,1000,5):
    for Nnodes in N:
        numbersx = []
        numbersy = []
        for prob in np.linspace(0,1,51):
            nconnected = 0
            for time in range(times):
                Nnodes2 = int(Nnodes)
                biGraph = nx.binomial_graph(Nnodes2,prob,directed = dirigit) # A.k.a. Erdos-Rényi graph
                if nx.is_connected(biGraph):
                    nconnected = nconnected +1
                # Draw plots
                # nx.draw(biGraph)
                # plt.savefig(directory_path + "/binomial_graph/" + str(x) + ".png")
                # plt.clf()
                biGraph.clear()
            pconnected = nconnected /times
            numbersx.append(prob)
            numbersy.append(pconnected)
            f.write("Nodes: " + str(Nnodes2) +  " Probability edge: " + str(prob) + " Connected probability: " + str(pconnected) + "\n")
        print(numbersx) 
        print(numbersy) 
        connectedPlot(numbersx, numbersy, "Probability that an edge is created", nplot, Nnodes,  "/binomial_graph/plots/")
        nplot += 1
    f.close()
    

def random_geometric_graph():
    if not os.path.isdir(directory_path + "/random_geometric_graph") :
        os.mkdir(directory_path + "/random_geometric_graph")
    f = open(directory_path + "/random_geometric_graph/random_geometric_graph_analysis.txt", "w")
    times = 10
    nplot=0
    f.write("Sample size: " + str(times) + "\n")
    N = [5,10,20,50,100,500,1000]
    # for Nnodes in np.linspace(20,100,5):
    for Nnodes in N:
        numbersx = []
        numbersy = []
        for radius in np.linspace(0,math.sqrt(2),51):
            nconnected = 0
            for time in range(times):
                Nnodes2 = int(Nnodes)
                geoGraph = nx.random_geometric_graph(Nnodes2, radius)
                if nx.is_connected(geoGraph):
                    nconnected = nconnected +1
                # Draw graph
                # nx.draw(geoGraph)
                # plt.savefig(directory_path + "/random_geometric_graph/" + "radi:"+str(radius) + "intent:"+str(time) + ".png")
                # plt.clf()
                geoGraph.clear()
            pconnected = nconnected /times
            numbersx.append(radius)
            numbersy.append(pconnected)
            f.write("Nodes: " + str(Nnodes2) +  " Minimum distance: " + str(radius) + " Connected probability: " + str(pconnected) + "\n")
        print(numbersx) 
        print(numbersy) 
        connectedPlot(numbersx, numbersy, "Radius where edges are created between nodes", nplot, Nnodes,  "/random_geometric_graph/plots/")
        nplot += 1
    f.close()

def node_percolation(G):
    print("p:")
    p = float(input())

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))
    
    print("----Node Percolation-----")
    for i in range(G.number_of_nodes()):
        if random.random()>p:
            G.remove_node(i)

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))


def edge_percolation(G):
    print("p:")
    p = float(input())

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))
    
    print("----Edge Percolation-----")
    for i in G.edges():
        if random.random()>p:
            G.remove_edge(*i)

    print("Nodes: " + str(G.nodes()))
    print("Edges: " + str(G.edges()))


def complex_connected_components(G):
    b = True
    for c in nx.connected_components(G):
        H = G.subgraph(c)
        print("Component connexa amb " + str(len(nx.cycle_basis(H))) + " cicles")
        b &= len(nx.cycle_basis(H))>1
    return b

def graella(n, p):
    G = np.empty((n,n))
    for i in range(n):
        for j in range(n):
            if random.random()<p:
                G[i][j] = 1
            else:
                G[i][j] = 0
    return G


selection = readOption()
if selection == 1:
    G = nx.binomial_graph(5,0.8)
    edge_percolation(G) 
elif selection == 2:
    binomial_graph()
elif selection == 3:
    random_geometric_graph()
else:
    print("That's not a valid option")

