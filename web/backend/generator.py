from __future__ import annotations

import math
import networkx as nx

from .models import NodeData, GraphData


def binomial_graph(n: int, p: float, seed: int | None = None) -> tuple[nx.Graph, GraphData]:
    """Generate Erdos-Renyi G(n,p). Positions via spring layout."""
    g = nx.binomial_graph(n, p, seed=seed)
    pos = nx.spring_layout(g, seed=seed, iterations=50)
    nodes = [NodeData(id=i, x=float(pos[i][0]), y=float(pos[i][1])) for i in range(n)]
    edges = [(u, v) for u, v in g.edges()]
    return g, GraphData(nodes=nodes, edges=edges, n=n)


def geometric_graph(n: int, r: float, seed: int | None = None) -> tuple[nx.Graph, GraphData]:
    """Generate random geometric graph on unit square."""
    g = nx.random_geometric_graph(n, r, seed=seed)
    nodes = [
        NodeData(id=i, x=float(g.nodes[i]["pos"][0]), y=float(g.nodes[i]["pos"][1]))
        for i in range(n)
    ]
    edges = [(u, v) for u, v in g.edges()]
    return g, GraphData(nodes=nodes, edges=edges, n=n)


def grid_graph(side: int) -> tuple[nx.Graph, GraphData]:
    """Generate an n x n grid graph with grid positions."""
    n = side * side
    g = nx.grid_2d_graph(side, side)
    mapping = {}
    nodes: list[NodeData] = []
    for idx, (r, c) in enumerate(sorted(g.nodes())):
        mapping[(r, c)] = idx
        nodes.append(NodeData(id=idx, x=c / max(side - 1, 1), y=r / max(side - 1, 1)))
    g = nx.relabel_nodes(g, mapping)
    edges = [(u, v) for u, v in g.edges()]
    return g, GraphData(nodes=nodes, edges=edges, n=n)
