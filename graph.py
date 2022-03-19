import copy
import math
import os
import random
import enum
import sys
from tqdm import tqdm

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

directory_path = os.getcwd()


class ReadGraphOption(enum.Enum):
    binomial = 1
    geometric = 2
    graella = 3


def gen_all_graphs():
    # binomial_graph_generation()
    # random_geometric_graph_generation()
    graella_nxn_generation()


def read_graph(directory, n_nodes, p_r, time, read_graph_option):
    graph_file = []
    if (read_graph_option == read_graph_option.binomial) or (read_graph_option == read_graph_option.geometric):
        graph_file = open(
            directory_path + directory + "graph_" + str(n_nodes) + '_' + str(p_r) + '_' + str(time) + ".txt", 'r')
    elif read_graph_option == read_graph_option.graella:
        graph_file = open(directory_path + directory + "graella_" + str(n_nodes) + ".txt", 'r')

    lines = graph_file.readlines()
    adjacency_list = []  # first item is node, next nodes are its neighbours
    for line in lines:
        nodo = [int(i) for i in line.split() if i.isdigit()]
        adjacency_list.append(nodo)
    g = nx.Graph()
    for node in adjacency_list:
        g.add_node(node[0])
        for i in range(1, len(node)):
            g.add_edge(node[0], node[i])
    # nx.draw_networkx(g, with_labels=True)
    # plt.savefig(directory_path + "/graella/" + "graella" + ".png")
    # plt.clf()
    return g


def graella_nxn_generation():
    nxn_values = [4, 7, 10, 23, 32, 45, 71, 100]
    if not os.path.isdir(directory_path + "/graella/graphs"):
        os.makedirs(directory_path + "/graella/graphs")
    for n_nodes in tqdm(nxn_values):
        graella_gen = nx.Graph()
        f = open(directory_path + "/graella/graphs/" + "graella_" + str(n_nodes * n_nodes) + ".txt", "w")
        for i in range(n_nodes * n_nodes):
            graella_gen.add_node(i)
        # Arestes horitzontals
        for i in range(n_nodes):
            for j in range(n_nodes - 1):
                graella_gen.add_edge((i * n_nodes) + j, (i * n_nodes) + j + 1)
        # Arestes verticals
        for i in range(n_nodes - 1):
            for j in range(n_nodes):
                graella_gen.add_edge((i * n_nodes) + j, ((i + 1) * n_nodes) + j)
        # Write graph to file
        for node in graella_gen:
            f.write(str(node) + " ")
            for neighbour in graella_gen[node]:
                f.write(str(neighbour) + " ")
            f.write("-1\n")
        f.close()


def binomial_graph_generation():
    if not os.path.isdir(directory_path + "/binomial_graph/graphs"):
        os.makedirs(directory_path + "/binomial_graph/graphs")
    times = 1  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    for Nnodes in tqdm(node_values, desc="Nodes:"):
        for prob in tqdm(np.linspace(0, 1, 11), desc="Probability:", leave=False):
            for time in range(times):
                f = open(
                    directory_path + "/binomial_graph/graphs/" + "graph_" + str(Nnodes) + "_" + str(prob) + "_" + str(
                        time) + ".txt", "w")
                bi_graph = nx.binomial_graph(Nnodes, prob, directed=0)  # A.k.a. Erdos-Rényi graph
                for node in bi_graph:
                    f.write(str(node) + " ")
                    for neighbour in bi_graph[node]:
                        f.write(str(neighbour) + " ")
                    f.write("-1\n")
                f.close()


def random_geometric_graph_generation():
    if not os.path.isdir(directory_path + "/random_geometric_graph/graphs"):
        os.makedirs(directory_path + "/random_geometric_graph/graphs")
    times = 1
    node_values = [10, 20, 50, 100, 500, 1000, 5000, 10000]
    # node_values = [5, 10, 20]
    for Nnodes in tqdm(node_values, desc="Nodes"):
        for radius in tqdm(np.linspace(0, math.sqrt(2), 11), desc="Radius", leave=False):
            for time in tqdm(range(times), desc="Times", leave=False):
                geo_graph = nx.random_geometric_graph(Nnodes, radius)
                f = open(
                    directory_path + "/random_geometric_graph/graphs/" + "graph_" + str(Nnodes) + "_" + str(
                        radius) + "_" + str(
                        time) + ".txt", "w")
                for node in geo_graph:
                    f.write(str(node) + " ")
                    for neighbour in geo_graph[node]:
                        f.write(str(neighbour) + " ")
                    f.write("-1\n")
                f.close()


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
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "figure_connected_" + str(nfigure) + ".png")
    # plt.clf() // Clear plot each time


def binomial_graph():
    if not os.path.isdir(directory_path + "/binomial_graph"):
        os.makedirs(directory_path + "/binomial_graph")
    f = open(directory_path + "/binomial_graph/binomial_graph_analysis.txt", "w")

    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    f.write("Sample size: " + str(times) + "\n")
    nplot = 0
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    for Nnodes in tqdm(node_values, desc="Nodes"):
        numbers_x = []
        numbers_y = []
        for prob in tqdm(np.linspace(0, 1, 11), desc="Probability", leave=False):
            n_connected = 0
            for _ in tqdm(range(times), desc="Times", leave=False):
                bi_graph = nx.binomial_graph(Nnodes, prob, directed=0)  # A.k.a. Erdos-Rényi graph
                if nx.is_connected(bi_graph):
                    n_connected = n_connected + 1
            p_connected = n_connected / times
            numbers_x.append(prob)
            numbers_y.append(p_connected)
            f.write("Nodes: " + str(Nnodes) + " Probability edge: " + str(prob) + " Connected probability: " + str(
                p_connected) + "\n")
        connected_plot(numbers_x, numbers_y, "Probability that an edge is created", nplot, Nnodes,
                       "/binomial_graph/plots/")
        nplot += 1
    f.close()


def binomial_graph_percolation(percolation_func, x_label, directory):
    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    # Les probabilitats han de coincidir amb el nom d'un arxiu
    p_gen_connected_graph = [0.5, 0.30000000000000004, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    p_gen = 0
    for Nnodes in tqdm(node_values, desc="Nodes"):
        numbers_x = []
        numbers_y = []
        numbers_y_complex = []
        numbers_y_complex_and_connected = []
        chosen_p_q = p_gen_connected_graph[p_gen]
        for probQ in tqdm(np.linspace(0, 1, 11), desc="Probability", leave=False):
            n_connected = 0
            n_complex = 0
            n_complex_and_connected = 0
            bi_graph = read_graph("/binomial_graph/graphs/", Nnodes, chosen_p_q, 0, ReadGraphOption.binomial)
            for _ in tqdm(range(times), desc="Time", leave=False):
                # bi_graph = nx.binomial_graph(Nnodes, chosen_p_q, directed=0)
                bi_graph_to_percolate = copy.deepcopy(bi_graph)
                perc_graph = percolation_func(bi_graph_to_percolate, probQ)
                if perc_graph.number_of_nodes() > 0:
                    if nx.is_connected(perc_graph):
                        n_connected = n_connected + 1
                        if complex_connected_components(perc_graph):
                            n_complex_and_connected += 1
                            # n_complex += 1
                    elif complex_connected_components(perc_graph):
                        n_complex += 1
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
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes, directory)
        # plot graph complex
        # print(numbers_y_complex)
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes, directory)
        # plot graph complex and connected
        # print(numbers_y_complex_and_connected)
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


def random_geometric_graph():
    if not os.path.isdir(directory_path + "/random_geometric_graph"):
        os.makedirs(directory_path + "/random_geometric_graph")
    # f = open(directory_path + "/random_geometric_graph/random_geometric_graph_analysis.txt", "w")
    times = 10
    nplot = 0
    # f.write("Sample size: " + str(times) + "\n")
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    for Nnodes in tqdm(node_values, desc="Nodes"):
        numbers_x = []
        numbers_y = []
        for radius in tqdm(np.linspace(0, math.sqrt(2), 11), desc="Radius", leave=False):
            n_connected = 0
            for _ in tqdm(range(times), desc="Time", leave=False):
                geo_graph = nx.random_geometric_graph(Nnodes, radius)
                if nx.is_connected(geo_graph):
                    n_connected = n_connected + 1
            p_connected = n_connected / times
            numbers_x.append(radius)
            numbers_y.append(p_connected)
            # f.write("Nodes: " + str(Nnodes) + " Minimum distance: " + str(radius) + " Connected probability: " + str(
            #     p_connected) + "\n")
        print(numbers_x)
        print(numbers_y)
        connected_plot(numbers_x, numbers_y, "Radius where edges are created between nodes", nplot, Nnodes,
                       "/random_geometric_graph/plots/")
        nplot += 1


def random_geometric_graph_percolation(percolation_func, x_label, directory):
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    node_values = [5, 10, 20, 50, 100, 500, 1000]
    r_gen_connected_graph = [0.9, 0.55, 0.5, 0.35, 0.25, 0.15, 0.13]

    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    # r_gen_connected_graph = [0.55, 0.5, 0.35, 0.25, 0.15, 0.13, ?, ?, ?]

    # node_values = [5, 10, 20, 50, 100]
    # r_gen_connected_graph = [0.9, 0.55, 0.5, 0.35, 0.25]
    r_gen = 0
    for Nnodes in tqdm(node_values, desc="Nodes"):
        numbers_x = []
        numbers_y = []
        numbers_y_complex = []
        numbers_y_complex_and_connected = []
        chosen_r_q = r_gen_connected_graph[r_gen]
        for probQ in tqdm(np.linspace(0, 1, 11), desc="Probability", leave=False):
            n_connected = 0
            n_complex = 0
            n_complex_and_connected = 0
            # n_connected_edge = 0
            geo_graph = read_graph("/random_geometric_graph/graphs/", Nnodes, chosen_r_q, 0,
                                   ReadGraphOption.geometric)
            for _ in tqdm(range(times), desc="Time", leave=False):
                # geo_graph = nx.random_geometric_graph(Nnodes, chosen_r_q)
                geo_graph_to_percolate = copy.deepcopy(geo_graph)
                perc_graph = percolation_func(geo_graph_to_percolate, probQ)
                if perc_graph.number_of_nodes() > 0:
                    if nx.is_connected(perc_graph):
                        n_connected = n_connected + 1
                        if complex_connected_components(perc_graph):
                            n_complex_and_connected += 1
                            # n_complex += 1
                    elif complex_connected_components(perc_graph):
                        n_complex += 1
            p_connected = n_connected / times
            p_complex = n_complex / times
            p_complex_and_connected = n_complex_and_connected / times
            numbers_x.append(probQ)
            numbers_y.append(p_connected)
            numbers_y_complex.append(p_complex)
            numbers_y_complex_and_connected.append(p_complex_and_connected)
        # plot graph connected
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes,
                       directory)
        # plot graph complex
        # print(numbers_y_complex)
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes, directory)
        # plot graph complex and connected
        # print(numbers_y_complex_and_connected)
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
        # print("Component connexa amb " + str(len(nx.cycle_basis(h))) + " cicles")
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
    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    # nxn_values = [4, 7, 10, 23, 32]
    nxn_values = [4, 7, 10, 23, 32, 45, 71, 100]
    # nxn_values = [4, 7, 10]
    for Nnodes in tqdm(nxn_values, desc="Nodes"):
        numbers_x = []
        numbers_y = []
        numbers_y_complex = []
        numbers_y_complex_and_connected = []
        for probQ in tqdm(np.linspace(0, 1, 11), desc="Probability", leave=False):
            n_connected = 0
            n_complex = 0
            n_complex_and_connected = 0
            graella = read_graph("/graella/graphs/", Nnodes * Nnodes, probQ, 0, ReadGraphOption.graella)
            for _ in tqdm(range(times), desc="Time", leave=False):
                graella_a_percolar = copy.deepcopy(graella)  # We do not want a shallow copy of graella otherwise we
                # would have to read the graph lots of times
                perc_bi_graph = percolation_func(graella_a_percolar, probQ)
                if perc_bi_graph.number_of_nodes() > 0:
                    if nx.is_connected(perc_bi_graph):
                        n_connected = n_connected + 1
                        if complex_connected_components(perc_bi_graph):
                            n_complex_and_connected += 1
                            # n_complex += 1
                    elif complex_connected_components(perc_bi_graph):
                        n_complex += 1
            p_connected = n_connected / times
            p_complex = n_complex / times
            p_complex_and_connected = n_complex_and_connected / times
            numbers_x.append(probQ)
            numbers_y.append(p_connected)
            numbers_y_complex.append(p_complex)
            numbers_y_complex_and_connected.append(p_complex_and_connected)
        # plot graph connected
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


def compose_graph(percolation1, percolation2):
    return lambda x, prob: percolation1(percolation2(x, prob), prob)


def read_option():
    print("Select your option:\n"
          "1- Binomial graph\n"
          "2- Random geometric graph\n"
          "3- Binomial graph percolation by node or by edge\n"
          "4- Random geometric graph percolation by node or by edge\n"
          "5- Graella NxN with percolation by node or by edge\n"
          "6- Graella NxN node and edge percolation\n"
          "7- Generate and export all graphs as .txt"
          )
    return int(input())


selection = read_option()
if selection == 1:
    binomial_graph()
elif selection == 2:
    random_geometric_graph()
elif selection == 3:
    print("Choose percolation by: [node/edge]")
    choice = input()
    if choice == "node":
        percolation = node_percolation
        binomial_graph_percolation(percolation, "Percolation nodes", "/binomial_graph/plots_percolate_nodes/")
    if choice == "edge":
        percolation = edge_percolation
        binomial_graph_percolation(percolation, "Percolation edges", "/binomial_graph/plots_percolate_edges/")
elif selection == 4:
    print("Choose percolation by: [node/edge]")
    choice = input()
    if choice == "node":
        percolation = node_percolation
        random_geometric_graph_percolation(percolation, "Percolation node",
                                           "/random_geometric_graph/plots_percolate_nodes/")
    if choice == "edge":
        percolation = edge_percolation
        random_geometric_graph_percolation(percolation, "Percolation edges",
                                           "/random_geometric_graph/plots_percolate_edges/")
elif selection == 5:
    print("Choose percolation by: [node/edge]")
    choice = input()
    if choice == "node":
        percolation = node_percolation
        percolate_graella(percolation, "Percolation nodes", "/graella/plots_percolate_nodes/")
    if choice == "edge":
        percolation = edge_percolation
        percolate_graella(percolation, "Percolation edges", "/graella/plots_percolate_edges/")
elif selection == 6:
    print("Choose an N to generate an NxN grid")
    n_nodes = int(input())
    print("Choose a p to percolate")
    p = float(input())
    graella = graella_nxn(n_nodes)
    node_then_edge_percolation = compose_graph(edge_percolation, node_percolation)
    graella = node_then_edge_percolation(graella, p)

    # if not os.path.isdir(directory_path + "/graella"):
    #     os.makedirs(directory_path + "/graella")
    # nx.draw_networkx(graella, with_labels=True)
    # plt.savefig(directory_path + "/graella/" + "graella" + str(n_nodes) + ".png")
    # plt.clf()
elif selection == 7:
    gen_all_graphs()
# elif selection == 8:
#     nodes = 10
#     prob = 0.2
#     time = 1
#     print(sys.getrefcount(time))
#     read_graph("/binomial_graph/graphs/", nodes, prob, time, ReadGraphOption.binomial)
#     print(sys.getrefcount(time))
else:
    print("That's not a valid option")
print("Program finished successfully")
