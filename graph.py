import copy
import enum
import math
import os
import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tqdm import tqdm

directory_path = os.getcwd()


class ReadGraphOption(enum.Enum):
    """
    Class to select which graph are we reading
    """
    binomial = 1
    geometric = 2
    graella = 3


def read_graph(directory, n_nodes, p_r, time, read_graph_option):
    """
    Read a graph from the given directory and return it

    :param directory: Directory to read from
    :param n_nodes: Number of nodes of the graph
    :param p_r: Probability / radius
    :param time: nth generation of the graph
    :param read_graph_option: Select which type of graph it is
    :return: returns the read graph
    """
    graph_file = None
    try:
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
    finally:
        graph_file.close()
    return g


def graella_nxn_generation():
    """
    Export graellas to a directory
    """
    nxn_values = [4, 7, 10, 23, 32, 45, 71, 100]
    if not os.path.isdir(directory_path + "/graella/graphs"):
        os.makedirs(directory_path + "/graella/graphs")
    for n_nodes in tqdm(nxn_values):
        graella_gen = graella_nxn(n_nodes)
        # Write graph to file
        with open(directory_path + "/graella/graphs/" + "graella_" + str(n_nodes * n_nodes) + ".txt", "w") as f:
            for node in graella_gen:
                f.write(str(node) + " ")
                for neighbour in graella_gen[node]:
                    f.write(str(neighbour) + " ")
                f.write("-1\n")


def binomial_graph_generation():
    """
    Export binomial generated graphs to a directory
    """
    if not os.path.isdir(directory_path + "/binomial_graph/graphs"):
        os.makedirs(directory_path + "/binomial_graph/graphs")
    times = 1  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    for Nnodes in tqdm(node_values, desc="Nodes:"):
        for prob in tqdm(np.linspace(0, 1, 11), desc="Probability:", leave=False):
            for time in range(times):
                with open(directory_path + "/binomial_graph/graphs/" + "graph_" + str(Nnodes) + "_" + str(
                        prob) + "_" + str(time) + ".txt", "w") as f:
                    bi_graph = nx.binomial_graph(Nnodes, prob, directed=0)  # A.k.a. Erdos-Rényi graph
                    for node in bi_graph:
                        f.write(str(node) + " ")
                        for neighbour in bi_graph[node]:
                            f.write(str(neighbour) + " ")
                        f.write("-1\n")


def random_geometric_graph_generation():
    """
    Export random geometric generated graphs to a directory
    """
    if not os.path.isdir(directory_path + "/random_geometric_graph/graphs"):
        os.makedirs(directory_path + "/random_geometric_graph/graphs")
    times = 1
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    for Nnodes in tqdm(node_values, desc="Nodes"):
        for radius in tqdm(np.linspace(0, math.sqrt(2), 11), desc="Radius", leave=False):
            for time in tqdm(range(times), desc="Times", leave=False):
                geo_graph = nx.random_geometric_graph(Nnodes, radius)
                with open(directory_path + "/random_geometric_graph/graphs/" + "graph_" + str(Nnodes) + "_" + str(
                        radius) + "_" + str(time) + ".txt", "w") as f:
                    for node in geo_graph:
                        f.write(str(node) + " ")
                        for neighbour in geo_graph[node]:
                            f.write(str(neighbour) + " ")
                        f.write("-1\n")


def complex_and_connected_plot(numbersx, numbersy, xlabel, nfigure, label, directory):
    """
    Generate a plot for complex and connected graphs
    :param numbersx: List in the x axis of the plot
    :param numbersy: List in the y axis of the plot
    :param xlabel: Label in the x axis of the plot
    :param nfigure: Number to assign to the name of the file
    :param label: Label for the legend of the plot
    :param directory: Directory where the plot will be exported to
    :return: None
    """
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
    """
    Generate a plot for complex graphs
    :param numbersx: List in the x axis of the plot
    :param numbersy: List in the y axis of the plot
    :param xlabel: Label in the x axis of the plot
    :param nfigure: Number to assign to the name of the file
    :param label: Label for the legend of the plot
    :param directory: Directory where the plot will be exported to
    :return: None
    """
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
    """
    Generate a plot for connected graphs
    :param numbersx: List in the x axis of the plot
    :param numbersy: List in the y axis of the plot
    :param xlabel: Label in the x axis of the plot
    :param nfigure: Number to assign to the name of the file
    :param label: Label for the legend of the plot
    :param directory: Directory where the plot will be exported to
    :return: None
    """
    label2 = str(label) + " Nodes"
    plt.figure(2)
    plt.plot(numbersx, numbersy, label=label2)
    plt.ylabel('Probability that network is connected')
    plt.xlabel(xlabel)
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    plt.legend()
    plt.savefig(directory_path + directory + "figure_connected_" + str(nfigure) + ".png")


def binomial_graph():
    """
    Generates a plot which shows how probable it is that a binomial generated graph is connected
    """
    if not os.path.isdir(directory_path + "/binomial_graph"):
        os.makedirs(directory_path + "/binomial_graph")
    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
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
        connected_plot(numbers_x, numbers_y, "Probability that an edge is created", nplot, Nnodes,
                       "/binomial_graph/plots/")
        nplot += 1


def binomial_graph_percolation(percolation_func, x_label, directory):
    """
    Generates plots given a percolation function about their connectivity and complexity

    :param percolation_func: Percolation function that will be used
    :param x_label: Label located in the x axis of the plot
    :param directory: Directory where the plot will be saved
    :return: None
    """
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
            # bi_graph = nx.binomial_graph(Nnodes, chosen_p_q, directed=0)
            for _ in tqdm(range(times), desc="Time", leave=False):
                n_complex, n_complex_and_connected, n_connected = percolate_graph_info(bi_graph, n_complex,
                                                                                       n_complex_and_connected,
                                                                                       n_connected,
                                                                                       percolation_func, probQ)
            calculate_prob_connex_complex(n_complex, n_complex_and_connected, n_connected, numbers_x, numbers_y,
                                          numbers_y_complex,
                                          numbers_y_complex_and_connected, probQ, times)
        # plot graph connected
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes, directory)
        # plot graph complex
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes, directory)
        # plot graph complex and connected
        complex_and_connected_plot(numbers_x, numbers_y_complex_and_connected, x_label, nplot, Nnodes, directory)
        nplot += 1
        p_gen = p_gen + 1
    reset_plots()


def calculate_prob_connex_complex(n_complex, n_complex_and_connected, n_connected, numbers_x, numbers_y,
                                  numbers_y_complex, numbers_y_complex_and_connected, prob_q, times):
    """
    Appends probQ to numbers_x and appends the probability that a graph is connected given a probQ to numbers_y.
    Also, appends to numbers_y_complex the probability that a graph is complex given probQ. Finally, appends to
    numbers_y_complex_and_connected the probability that a graph is complex and connected given probQ.

    :param n_complex: Number of complex graphs
    :param n_complex_and_connected: Number of complex and connected graphs
    :param n_connected: Number of connected graphs
    :param numbers_x: Values for the x axis
    :param numbers_y: Values for the y axis
    :param numbers_y_complex: Values for the y axis
    :param numbers_y_complex_and_connected: Values for the y axis
    :param prob_q: Probability of percolation on the graph
    :param times: Times that the graph has been percolated
    :return: None, just appends to numbers_x, numbers_y, numbers_y_complex and numbers_y_complex_and_connected
    """
    p_connected = n_connected / times
    p_complex = n_complex / times
    p_complex_and_connected = n_complex_and_connected / times
    numbers_x.append(prob_q)
    numbers_y.append(p_connected)
    numbers_y_complex.append(p_complex)
    numbers_y_complex_and_connected.append(p_complex_and_connected)


def reset_plots():
    """
    Clears all plots
    """
    plt.clf()
    plt.figure(0)
    plt.clf()
    plt.figure(1)
    plt.clf()
    plt.figure(2)
    plt.clf()


def percolate_graph_info(graph, n_complex, n_complex_and_connected, n_connected, percolation_func, prob_q):
    """
    Obtain information about a random percolation of a given graph.

    :param graph: Graph to percolate
    :param n_complex: Number of times the graph is complex
    :param n_complex_and_connected: Number of times the graph is complex and connected
    :param n_connected: Number of times the graph is connected
    :param percolation_func: Percolation function used
    :param prob_q: Probability used to percolate the graph
    :return: n_complex, n_complex_and_connected, n_connected
    """
    graph_to_percolate = copy.deepcopy(graph)  # We do not want a shallow copy of graella otherwise we
    # would have to read the graph lots of times
    perc_graph = percolation_func(graph_to_percolate, prob_q)
    if perc_graph.number_of_nodes() > 0:
        if nx.is_connected(perc_graph):
            n_connected = n_connected + 1
            if complex_connected_components(perc_graph):
                n_complex_and_connected += 1
                n_complex += 1
        elif complex_connected_components(perc_graph):
            n_complex += 1
    return n_complex, n_complex_and_connected, n_connected


def random_geometric_graph():
    """
    Generate a plot about how connected a graph is given a radius to generate the graph
    """
    if not os.path.isdir(directory_path + "/random_geometric_graph"):
        os.makedirs(directory_path + "/random_geometric_graph")
    times = 10
    nplot = 0
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
        connected_plot(numbers_x, numbers_y, "Radius where edges are created between nodes", nplot, Nnodes,
                       "/random_geometric_graph/plots/")
        nplot += 1


def random_geometric_graph_percolation(percolation_func, x_label, directory):
    """
    Generates plots given a percolation function about their connectivity and complexity

    :param percolation_func: Percolation function that will be used
    :param x_label: Label located in the x axis of the plot
    :param directory: Directory where the plot will be saved
    :return: None
    """
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    # node_values = [5, 10, 20, 50, 100, 500, 1000]
    # r_gen_connected_graph = [0.9, 0.55, 0.5, 0.35, 0.25, 0.15, 0.13]
    node_values = [10, 20, 50, 100, 500, 1000, 2000, 5000, 10000]
    r_gen_connected_graph = [0.565685424949238, 0.565685424949238, 0.565685424949238, 0.282842712474619,
                             0.282842712474619, 0.282842712474619, 0.282842712474619, 0.282842712474619,
                             0.282842712474619]
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
            # geo_graph = nx.random_geometric_graph(Nnodes, chosen_r_q)
            for _ in tqdm(range(times), desc="Time", leave=False):
                n_complex, n_complex_and_connected, n_connected = percolate_graph_info(geo_graph, n_complex,
                                                                                       n_complex_and_connected,
                                                                                       n_connected,
                                                                                       percolation_func, probQ)
            calculate_prob_connex_complex(n_complex, n_complex_and_connected, n_connected, numbers_x, numbers_y,
                                          numbers_y_complex,
                                          numbers_y_complex_and_connected, probQ, times)
        # plot graph connected
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes,
                       directory)
        # plot graph complex
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes, directory)
        # plot graph complex and connected
        complex_and_connected_plot(numbers_x, numbers_y_complex_and_connected, x_label, nplot, Nnodes, directory)
        nplot += 1
        r_gen = r_gen + 1
    reset_plots()


def node_percolation(g, p):
    """
    For all nodes in g if a random generated number is greater than given value p then we remove the node

    :param g: Graph to be percolated
    :param p: If p is < random then node is removed from the graph
    :return: Percolated graph
    """
    for i in range(g.number_of_nodes()):
        if random.random() > p:
            g.remove_node(i)
    return g


def edge_percolation(g, p):
    """
    For all edges in g if a random generated number is greater than given value p then we remove the edge

    :param g: Graph to be percolated
    :param p: If p is < random then edge is removed from the graph
    :return: Percolated graph
    """
    for i in g.edges():
        if random.random() > p:
            g.remove_edge(*i)
    return g


def complex_connected_components(g):
    """
    Returns true if all the connected components are complex (have at least two cycles)

    :param g: Graph to be percolated
    :return: True if all the CC are complex
    """
    b = True
    for c in nx.connected_components(g):
        h = g.subgraph(c)
        b &= len(nx.cycle_basis(h)) > 1
        if not b:
            return b
    return b


def graella_nxn(n):
    """
    Generate a graella graph

    :param n: number of nodes to make an NxN graph
    :return: Returns a "graella" graph
    """
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
    """
    Generates plots given a percolation function about their connectivity and complexity

    :param percolation_func: Percolation function that will be used
    :param x_label: Label located in the x axis of the plot
    :param directory: Directory where the plot will be saved
    :return: None
    """
    if not os.path.isdir(directory_path + directory):
        os.makedirs(directory_path + directory)
    times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
    # probability that it is indeed connected
    nplot = 0
    nxn_values = [4, 7, 10, 23, 32, 45, 71, 100]
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
                n_complex, n_complex_and_connected, n_connected = percolate_graph_info(graella, n_complex,
                                                                                       n_complex_and_connected,
                                                                                       n_connected,
                                                                                       percolation_func, probQ)
            calculate_prob_connex_complex(n_complex, n_complex_and_connected, n_connected, numbers_x, numbers_y,
                                          numbers_y_complex, numbers_y_complex_and_connected, probQ, times)
        # plot graph connected
        connected_plot(numbers_x, numbers_y, x_label, nplot, Nnodes * Nnodes,
                       directory)
        # plot graph complex
        complex_plot(numbers_x, numbers_y_complex, x_label, nplot, Nnodes * Nnodes, directory)
        # plot graph complex and connected
        complex_and_connected_plot(numbers_x, numbers_y_complex_and_connected, x_label, nplot, Nnodes * Nnodes,
                                   directory)
        nplot += 1
    reset_plots()


def compose_graph(percolation1, percolation2):
    """
    Given two percolation operations returns a function that applies the composition of both with same p

    :param percolation1: Percolation function that will be performed aftwerwards
    :param percolation2: Percolation function that will be applied first
    :return:
    """
    return lambda x, prob: percolation1(percolation2(x, prob), prob)


def read_option():
    """
    Shows available options and reads the users input
    """
    print("Select your option:\n"
          "1- Binomial graph\n"
          "2- Random geometric graph\n"
          "3- Binomial graph percolation by node or by edge\n"
          "4- Random geometric graph percolation by node or by edge\n"
          "5- Graella NxN with percolation by node or by edge\n"
          "6- Graella NxN node and edge percolation\n"
          "7- Export graella NxN graphs as .txt\n"
          "8- Export binomial graphs as .txt\n"
          "9- Export geometric graphs as .txt"
          )
    return int(input())


if __name__ == '__main__': # Executed when invoked directly, not when imported
    selection = read_option()
    if selection == 1:
        binomial_graph()
    elif selection == 2:
        random_geometric_graph()
    elif selection == 3:
        print("Choose percolation by: [node/edge]")
        choice = input()
        if choice == "node":
            binomial_graph_percolation(node_percolation, "Percolation nodes", "/binomial_graph/plots_percolate_nodes/")
        if choice == "edge":
            binomial_graph_percolation(edge_percolation, "Percolation edges", "/binomial_graph/plots_percolate_edges/")
    elif selection == 4:
        print("Choose percolation by: [node/edge]")
        choice = input()
        if choice == "node":
            random_geometric_graph_percolation(node_percolation, "Percolation node",
                                               "/random_geometric_graph/plots_percolate_nodes/")
        if choice == "edge":
            random_geometric_graph_percolation(edge_percolation, "Percolation edges",
                                               "/random_geometric_graph/plots_percolate_edges/")
    elif selection == 5:
        print("Choose percolation by: [node/edge]")
        choice = input()
        if choice == "node":
            percolate_graella(node_percolation, "Percolation nodes", "/graella/plots_percolate_nodes/")
        if choice == "edge":
            percolate_graella(edge_percolation, "Percolation edges", "/graella/plots_percolate_edges/")
    elif selection == 6:
        print("Choose an N to generate an NxN grid")
        n_nodes = int(input())
        print("Choose a p to percolate")
        p = float(input())
        graella = graella_nxn(n_nodes)
        node_then_edge_percolation = compose_graph(edge_percolation, node_percolation)
        graella = node_then_edge_percolation(graella, p)
        if not os.path.isdir(directory_path + "/graella"):
            os.makedirs(directory_path + "/graella")
        nx.draw_networkx(graella, with_labels=True)
        plt.savefig(directory_path + "/graella/" + "graella" + str(n_nodes) + ".png")
        plt.clf()
    elif selection == 7:
        graella_nxn_generation()
    elif selection == 8:
        binomial_graph_generation()
    elif selection == 9:
        random_geometric_graph_generation()
    else:
        print("That's not a valid option")
    print("Program finished successfully")
