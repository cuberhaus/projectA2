import math
import os
import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

directory_path = os.getcwd()

def connected_plot(numbersx, numbersy, xlabel, nfigure, label, directory):
    label2 = str(label) + " Nodes"
    plt.plot(numbersx, numbersy, label=label2)
    plt.ylabel('Probability that network is connected')
    plt.xlabel(xlabel)
    # plt.show() // Show plot onscreen
    if not os.path.isdir(directory_path + directory):
        os.mkdir(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "figure_" + str(nfigure) + ".png")
    # plt.clf() // Clear plot each time


def read_option():
    print("Select your option:\n"
          "1- Percolation\n"
          "2- Binomial graph\n"
          "3- Random geometric graph\n"
          "4- Graella NxN")
    return int(input())


def read_n_nodes():
    print("Write the number of nodes:")
    return int(input())


def binomial_graph():
    print("Graph dirigit?: 0/1 ")
    dirigit = int(input())

    if not os.path.isdir(directory_path + "/binomial_graph"):
        os.mkdir(directory_path + "/binomial_graph")
    f = open(directory_path + "/binomial_graph/binomial_graph_analysis.txt", "w")

    times = 10
    f.write("Sample size: " + str(times) + "\n")
    nplot = 0
    node_values = [5, 10, 20, 50, 100, 500, 1000]
    # for Nnodes in np.linspace(20,1000,5):
    for Nnodes in node_values:
        numbers_x = []
        numbers_y = []
        for prob in np.linspace(0, 1, 51):
            n_connected = 0
            for time in range(times):
                bi_graph = nx.binomial_graph(Nnodes, prob, directed=dirigit)  # A.k.a. Erdos-Rényi graph
                if nx.is_connected(bi_graph):
                    n_connected = n_connected + 1
                # Draw plots
                # nx.draw(biGraph)
                # plt.savefig(directory_path + "/binomial_graph/" + str(x) + ".png")
                # plt.clf()
                bi_graph.clear()
            p_connected = n_connected / times
            numbers_x.append(prob)
            numbers_y.append(p_connected)
            f.write("Nodes: " + str(Nnodes) + " Probability edge: " + str(prob) + " Connected probability: " + str(
                p_connected) + "\n")
        print(numbers_x)
        print(numbers_y)
        connected_plot(numbers_x, numbers_y, "Probability that an edge is created", nplot, Nnodes,
                       "/binomial_graph/plots/")
        nplot += 1
    f.close()


def random_geometric_graph():
    if not os.path.isdir(directory_path + "/random_geometric_graph"):
        os.mkdir(directory_path + "/random_geometric_graph")
    f = open(directory_path + "/random_geometric_graph/random_geometric_graph_analysis.txt", "w")
    times = 10
    nplot = 0
    f.write("Sample size: " + str(times) + "\n")
    node_values = [5, 10, 20, 50, 100, 500, 1000]
    # for Nnodes in np.linspace(20,100,5):
    for Nnodes in node_values:
        numbers_x = []
        numbers_y = []
        for radius in np.linspace(0, math.sqrt(2), 51):
            n_connected = 0
            for time in range(times):
                geo_graph = nx.random_geometric_graph(Nnodes, radius)
                if nx.is_connected(geo_graph):
                    n_connected = n_connected + 1
                # Draw graph
                # nx.draw(geoGraph)
                # plt.savefig(directory_path + "/random_geometric_graph/" + "radi:"+str(radius) + "intent:"+str(time) + ".png")
                # plt.clf()
                geo_graph.clear()
            p_connected = n_connected / times
            numbers_x.append(radius)
            numbers_y.append(p_connected)
            f.write("Nodes: " + str(Nnodes) + " Minimum distance: " + str(radius) + " Connected probability: " + str(
                p_connected) + "\n")
        print(numbers_x)
        print(numbers_y)
        connected_plot(numbers_x, numbers_y, "Radius where edges are created between nodes", nplot, Nnodes,
                       "/random_geometric_graph/plots/")
        nplot += 1
    f.close()


def node_percolation(g):
    print("p:")
    p = float(input())

    print("Nodes: " + str(g.nodes()))
    print("Edges: " + str(g.edges()))

    print("----Node Percolation-----")
    for i in range(g.number_of_nodes()):
        if random.random() > p:
            g.remove_node(i)

    print("Nodes: " + str(g.nodes()))
    print("Edges: " + str(g.edges()))


def edge_percolation(g):
    print("p:")
    p = float(input())

    print("Nodes: " + str(g.nodes()))
    print("Edges: " + str(g.edges()))

    print("----Edge Percolation-----")
    for i in g.edges():
        if random.random() > p:
            g.remove_edge(*i)

    print("Nodes: " + str(g.nodes()))
    print("Edges: " + str(g.edges()))


def complex_connected_components(g):
    b = True
    for c in nx.connected_components(g):
        h = g.subgraph(c)
        print("Component connexa amb " + str(len(nx.cycle_basis(h))) + " cicles")
        b &= len(nx.cycle_basis(h)) > 1
    return b


# def graella(n, p):
#     g = np.empty((n, n))
#     for i in range(n):
#         for j in range(n):
#             if random.random() < p:
#                 g[i][j] = 1
#             else:
#                 g[i][j] = 0
#     return g

def graellaN(n):
    graella = nx.Graph()
    for i in range(n*n):
        graella.add_node(i)
    # Arestes horitzontals
    for i in range(n):
        for j in range(n-1):
            graella.add_edge((i*n)+j, (i*n) + j+1)
    # Arestes verticals
    for i in range(n-1):
        for j in range(n):
            graella.add_edge((i*n)+j, ((i+1)*n) + j)
    return graella

selection = read_option()
if selection == 1:
    print("Select your option:\n"
          "1- node percolation\n"
          "2- edge percolation\n")
    option = int(input())
    G = nx.binomial_graph(5, 0.8)
    if option == 1: node_percolation(G)
    else : edge_percolation(G)
elif selection == 2:
    binomial_graph()
elif selection == 3:
    random_geometric_graph()
elif selection == 4:
    print("Choose an N to generate an NxN grid")
    n = int(input())
    g = graellaN(n)
    if not os.path.isdir(directory_path + "/graella"):
        os.mkdir(directory_path + "/graella")
    nx.draw_networkx(g, with_labels = True)
    plt.savefig(directory_path + "/graella/" + "graella" + str(n) + ".png")
    plt.clf()


else:
    print("That's not a valid option")
