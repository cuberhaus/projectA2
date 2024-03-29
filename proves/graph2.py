import math
import os
import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

directory_path = os.getcwd()


def complex_and_connected_plot(numbersx, numbersy, xlabel, nfigure, label, directory):
    label2 = str(label) + " Nodes"
    plt.figure(0)
    plt.plot(numbersx, numbersy, label=label2)
    plt.ylabel('Probability that network is complex and connected')
    plt.xlabel(xlabel)
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "figure_complex_and_connected_" + str(nfigure) + ".png")


def complex_plot(numbersx, numbersy, xlabel, nfigure, label, directory):
    label2 = str(label) + " Nodes"
    plt.figure(1)
    plt.plot(numbersx, numbersy, label=label2)
    plt.ylabel('Probability that network is complex')
    plt.xlabel(xlabel)
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "figure_complex_" + str(nfigure) + ".png")


def connected_plot(numbersx, numbersy, xlabel, nfigure, label, directory):
    label2 = str(label) + " Nodes"
    plt.figure(2)
    plt.plot(numbersx, numbersy, label=label2)
    plt.ylabel('Probability that network is connected')
    plt.xlabel(xlabel)
    # plt.show() // Show plot onscreen
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "figure_connected	_" + str(nfigure) + ".png")
    # plt.clf() // Clear plot each time


def read_option():
    print("Select your option:\n"
          "1- Graella NxN with percolation\n"
          "2- Binomial graph\n"
          "3- Random geometric graph\n"
          "4- Graella NxN\n"
          "5- Binomial with percolation \n"
          "6- Random geometric with percolation")
    return int(input())


def read_n_nodes():
    print("Write the number of nodes:")
    return int(input())


def binomial_graph():
    print("Graph dirigit?: 0/1 ")
    dirigit = int(input())

    if not os.path.isdir(directory_path + "/binomial_graph"):
        os.makedirs(directory_path + "/binomial_graph")
    f = open(directory_path + "/binomial_graph/binomial_graph_analysis.txt", "w")

    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
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
        #print(numbers_x)
        #print(numbers_y)
        connected_plot(numbers_x, numbers_y, "Probability that an edge is created", nplot, Nnodes,
                       "/binomial_graph/plots/")
        nplot += 1
    f.close()

def binomial_graph_percolation(percolation_func, x_label, directory):
    # print("Graph dirigit?: 0/1 ")
    # dirigit = int(input())
    times = 100  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    # node_values = [5, 10, 20, 50, 100, 500, 1000]
    # p_gen_connected_graph = [0.8, 0.5,0.3, 0.15, 0.1, 0.05, 0.05]
    node_values = [5, 10, 20, 50, 100]
    p_gen_connected_graph = [0.8, 0.5, 0.3, 0.15, 0.1]
    p_gen = 0
    for Nnodes in node_values:
        numbers_x = []
        numbers_y = []
        numbers_y_complex = []
        numbers_y_complex_and_connected = []
        chosen_p_q = p_gen_connected_graph[p_gen]
        for probQ in np.linspace(0, 1, 51):
            n_connected = 0
            n_complex = 0
            n_complex_and_connected = 0
            for time in range(times):
                bi_graph = nx.binomial_graph(Nnodes, chosen_p_q, directed=0)
                perc_graph = percolation_func(bi_graph, probQ)
                if perc_graph.number_of_nodes() > 0:
                    if nx.is_connected(perc_graph):
                        n_connected = n_connected + 1
                        if complex_connected_components(perc_graph):
                            n_complex_and_connected += 1
                            n_complex += 1
                    elif complex_connected_components(perc_graph):
                        n_complex += 1
                        # Draw plots
                # nx.draw(perc_bi_graph)
                # plt.savefig(directory_path + "/binomial_graph/plots_percolate/" +str(probQ) + str(time) + ".png")
                # plt.clf()
                bi_graph.clear()
            p_connected = n_connected / times
            p_complex = n_complex / times
            p_complex_and_connected = n_complex_and_connected / times
            numbers_x.append(probQ)
            numbers_y.append(p_connected)
            numbers_y_complex.append(p_complex)
            numbers_y_complex_and_connected.append(p_complex_and_connected)
        # plot graph connected
        print(numbers_x)
        print(numbers_y)
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes, directory)
        # plot graph complex
        #print(numbers_y_complex)
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes, directory)
        # plot graph complex and connected
        #print(numbers_y_complex_and_connected)
        complex_and_connected_plot(numbers_x, numbers_y_complex_and_connected, x_label, nplot, Nnodes, directory)
        nplot += 1
        p_gen = p_gen + 1
    plt.clf()
    plt.figure(0)
    plt.clf()
    plt.figure(1)
    plt.clf()
    plt.figure(2)
    plt.clf()


def random_geometric_graph_percolation(percolation_func, x_label, directory):
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    times = 100  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    # node_values = [5, 10, 20, 50, 100, 500, 1000]
    # r_gen_connected_graph = [0.9, 0.55, 0.5, 0.35, 0.25,0.15, 0.13]
    node_values = [5, 10, 20, 50, 100]
    r_gen_connected_graph = [0.9, 0.55, 0.5, 0.35, 0.25]
    r_gen = 0
    for Nnodes in node_values:
        numbers_x = []
        numbers_y = []
        numbers_y_complex = []
        numbers_y_complex_and_connected = []
        chosen_r_q = r_gen_connected_graph[r_gen]
        for probQ in np.linspace(0, 1, 51):
            n_connected = 0
            n_complex = 0
            n_complex_and_connected = 0
            # n_connected_edge = 0
            for time in range(times):
                geo_graph = nx.random_geometric_graph(Nnodes, chosen_r_q)
                perc_graph = percolation_func(geo_graph, probQ)
                if perc_graph.number_of_nodes() > 0:
                    if nx.is_connected(perc_graph):
                        n_connected = n_connected + 1
                        if complex_connected_components(perc_graph):
                            n_complex_and_connected += 1
                            n_complex += 1
                    elif complex_connected_components(perc_graph):
                        n_complex += 1
                geo_graph.clear()
            p_connected = n_connected / times
            p_complex = n_complex / times
            p_complex_and_connected = n_complex_and_connected / times
            numbers_x.append(probQ)
            numbers_y.append(p_connected)
            numbers_y_complex.append(p_complex)
            numbers_y_complex_and_connected.append(p_complex_and_connected)
        # plot graph connected
        # print(numbers_x)
        # print(numbers_y)
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes,
                       directory)
        # plot graph complex
        #print(numbers_y_complex)
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes, directory)
        # plot graph complex and connected
        #print(numbers_y_complex_and_connected)
        complex_and_connected_plot(numbers_x, numbers_y_complex_and_connected, x_label, nplot, Nnodes, directory)
        nplot += 1
        r_gen = r_gen + 1
    plt.clf()
    plt.figure(0)
    plt.clf()
    plt.figure(1)
    plt.clf()
    plt.figure(2)
    plt.clf()


def random_geometric_graph():
    if not os.path.isdir(directory_path + "/random_geometric_graph"):
        os.makedirs(directory_path + "/random_geometric_graph")
    f = open(directory_path + "/random_geometric_graph/random_geometric_graph_analysis.txt", "w")
    times = 10
    nplot = 0
    f.write("Sample size: " + str(times) + "\n")
    node_values = [5, 10, 20, 50, 100, 500, 1000]
    for Nnodes in node_values:
        numbers_x = []
        numbers_y = []
        for radius in np.linspace(0, math.sqrt(2), 51):
            n_connected = 0
            for time in range(times):
                geo_graph = nx.random_geometric_graph(Nnodes, radius)
                if nx.is_connected(geo_graph):
                    n_connected = n_connected + 1
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


def node_percolation(g, p):
    for i in range(g.number_of_nodes()):
        if random.random() > p:
            g.remove_node(i)
    return g


def edge_percolation(g, p):
    for i in g.edges():
        if random.random() > p:
            g.remove_edge(*i)
    return g


def complex_connected_components(g):
    b = True
    for c in nx.connected_components(g):
        h = g.subgraph(c)
        #print("Component connexa amb " + str(len(nx.cycle_basis(h))) + " cicles")
        b &= len(nx.cycle_basis(h)) > 1
    return b


def graella_nxn(n):
    graella = nx.Graph()
    for i in range(n * n):
        graella.add_node(i)
    # Arestes horitzontals
    for i in range(n):
        for j in range(n - 1):
            graella.add_edge((i * n) + j, (i * n) + j + 1)
    # Arestes verticals
    for i in range(n - 1):
        for j in range(n):
            graella.add_edge((i * n) + j, ((i + 1) * n) + j)
    return graella


def percolate_graella(percolation_func, x_label, directory):
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    times = 100  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    nxn_values = [4, 7, 10, 23, 32]
    # nxn_values = [4, 7, 10]
    for Nnodes in nxn_values:
        numbers_x = []
        numbers_y = []
        numbers_y_complex = []
        numbers_y_complex_and_connected = []
        for probQ in np.linspace(0, 1, 51):
            n_connected = 0
            n_complex = 0
            n_complex_and_connected = 0
            for time in range(times):
                graella = graella_nxn(Nnodes)
                perc_bi_graph = percolation_func(graella, probQ)
                if perc_bi_graph.number_of_nodes() > 0:
                    if nx.is_connected(perc_bi_graph):
                        n_connected = n_connected + 1
                        if complex_connected_components(perc_bi_graph):
                            n_complex_and_connected += 1
                            n_complex += 1
                    elif complex_connected_components(perc_bi_graph):
                        n_complex += 1
                graella.clear()
            p_connected = n_connected / times
            p_complex = n_complex / times
            p_complex_and_connected = n_complex_and_connected / times
            numbers_x.append(probQ)
            numbers_y.append(p_connected)
            numbers_y_complex.append(p_complex)
            numbers_y_complex_and_connected.append(p_complex_and_connected)
        # plot graph connected
        # print(numbers_x)
        # print(numbers_y)
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes * Nnodes,
                       directory)
        # plot graph complex
        # print(numbers_y_complex)
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes * Nnodes, directory)
        # plot graph complex and connected
        # print(numbers_y_complex_and_connected)
        complex_and_connected_plot(numbers_x, numbers_y_complex_and_connected, x_label, nplot, Nnodes * Nnodes,
                                   directory)
        nplot += 1
    plt.clf()
    plt.figure(0)
    plt.clf()
    plt.figure(1)
    plt.clf()
    plt.figure(2)
    plt.clf()


def compose_graph(percolation1, percolation2, p):
    return lambda x, p: percolation1(percolation2(x, p), p)


selection = read_option()
if selection == 1:
    percolation = node_percolation
    percolate_graella(percolation, "Percolation nodes", "/graella/plots_percolate_nodes/")
    percolation = edge_percolation
    percolate_graella(percolation, "Percolation edges", "/graella/plots_percolate_edges/")
elif selection == 2:
    binomial_graph()
elif selection == 3:
    random_geometric_graph()
elif selection == 4:
    print("Choose an N to generate an NxN grid")
    n = int(input())
    print("Choose a p to percolate")
    p = float(input())
    graella = graella_nxn(n)
    # graella = node_percolation(graella,p)
    # graella = edge_percolation(graella, p)
    node_then_edge_percolation = compose_graph(edge_percolation, node_percolation, p)
    graella = node_then_edge_percolation(graella, p)

    if not os.path.isdir(directory_path + "/graella"):
        os.makedirs(directory_path + "/graella")
    nx.draw_networkx(graella, with_labels=True)
    plt.savefig(directory_path + "/graella/" + "graella" + str(n) + ".png")
    plt.clf()
elif selection == 5:
    percolation = node_percolation
    binomial_graph_percolation(percolation, "Percolation nodes", "/binomial_graph/plots_percolate_nodes/")
    percolation = edge_percolation
    binomial_graph_percolation(percolation, "Percolation edges", "/binomial_graph/plots_percolate_edges/")
elif selection == 6:
    percolation = node_percolation
    random_geometric_graph_percolation(percolation, "Percolation node",
                                       "/random_geometric_graph/plots_percolate_nodes/")
    percolation = edge_percolation
    random_geometric_graph_percolation(percolation, "Percolation edges",
                                       "/random_geometric_graph/plots_percolate_edges/")
else:
    print("That's not a valid option")
print("Program finished successfully")
