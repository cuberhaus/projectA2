# Cool but inefficient function ahead ->
# def binomial_graph_percolation():
#     print("percolation")
#     print("Graph dirigit?: 0/1 ")
#     dirigit = int(input())
#
#     if not os.path.isdir(directory_path + "/binomial_graph"):
#         os.makedirs(directory_path + "/binomial_graph")
#     f = open(directory_path + "/binomial_graph/binomial_graph_analysis.txt", "w")
#
#     times = 10  # We try for every probability 10 times Ex: if two times the graph is connected then we have a 20%
#     # probability that it is indeed connected
#     f.write("Sample size: " + str(times) + "\n")
#     nplot = 0
#     # node_values = [5, 10, 20, 50, 100]
#     node_values = [5]
#     # for Nnodes in np.linspace(20,1000,5):
#     for Nnodes in node_values:
#         numbers_x = []
#         numbers_y = []
#         numbers_xq = []
#         numbers_yq = []
#         chosen_p_q = 0
#         for prob in np.linspace(0, 1, 51):
#             n_connected = 0
#             for time in range(times):
#                 bi_graph = nx.binomial_graph(Nnodes, prob, directed=dirigit)  # A.k.a. Erdos-Rényi graph
#                 if nx.is_connected(bi_graph):
#                     n_connected = n_connected + 1
#                 bi_graph.clear()
#             p_connected = n_connected / times
#             if p_connected == 1 and chosen_p_q != 1: chosen_p_q = prob
#             if p_connected < 1 and chosen_p_q == 1: chosen_p_q = prob
#             numbers_x.append(prob)
#             numbers_y.append(p_connected)
#             f.write("Nodes: " + str(Nnodes) + " Probability edge: " + str(prob) + " Connected probability: " + str(
#                 p_connected) + "\n")
#         for probQ in np.linspace(0, 1, 51):
#             n_connected = 0
#             for time in range(times):
#                 bi_graph = nx.binomial_graph(Nnodes, chosen_p_q, directed=dirigit)
#                 perc_bi_graph = node_percolation(bi_graph, probQ)
#                 if perc_bi_graph.number_of_nodes() > 0 and nx.is_connected(perc_bi_graph):
#                     n_connected = n_connected + 1
#                 # Draw plots
#                 nx.draw(perc_bi_graph)
#                 plt.savefig(directory_path + "/binomial_graph/plots_percolate/" + str(probQ) + str(time) + ".png")
#                 plt.clf()
#                 bi_graph.clear()
#             p_connected = n_connected / times
#             numbers_xq.append(probQ)
#             numbers_yq.append(p_connected)
#             f.write("Nodes: " + str(Nnodes) + " Probability edge: " + str(probQ) + " Connected probability: " + str(
#                 p_connected) + "\n")
#
#         print(numbers_xq)
#         print(numbers_yq)
#         connected_plot(numbers_xq, numbers_yq, "Percolation edge", nplot, Nnodes,
#                        "/binomial_graph/plots_percolate/")
#         nplot += 1
#     f.close()
