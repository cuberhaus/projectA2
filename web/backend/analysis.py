from __future__ import annotations

import random
import networkx as nx

from .models import NodeData, GraphData, SweepPoint, SweepResult
from . import generator


def annotate(g: nx.Graph, data: GraphData) -> GraphData:
    """Fill in connectivity, complexity, and component labels."""
    data.connected = nx.is_connected(g) if g.number_of_nodes() > 0 else True
    components = list(nx.connected_components(g))
    data.n_components = len(components)
    data.is_complex = _is_complex(g, components)
    comp_map = {}
    for ci, comp in enumerate(components):
        for v in comp:
            comp_map[v] = ci
    for nd in data.nodes:
        nd.component = comp_map.get(nd.id, -1)
    return data


def _is_complex(g: nx.Graph, components: list[set[int]] | None = None) -> bool:
    """Every connected component must have >=2 independent cycles."""
    if components is None:
        components = list(nx.connected_components(g))
    for comp in components:
        sub = g.subgraph(comp)
        if len(nx.cycle_basis(sub)) < 2:
            return False
    return True


def node_percolation(g: nx.Graph, q: float, rng: random.Random | None = None) -> nx.Graph:
    """Keep each node with probability q."""
    if rng is None:
        rng = random.Random()
    remove = [v for v in g.nodes() if rng.random() > q]
    h = g.copy()
    h.remove_nodes_from(remove)
    return h


def edge_percolation(g: nx.Graph, q: float, rng: random.Random | None = None) -> nx.Graph:
    """Keep each edge with probability q."""
    if rng is None:
        rng = random.Random()
    remove = [(u, v) for u, v in g.edges() if rng.random() > q]
    h = g.copy()
    h.remove_edges_from(remove)
    return h


def _make_graph(model: str, n: int, param: float, seed: int | None) -> tuple[nx.Graph, GraphData]:
    if model == "binomial":
        return generator.binomial_graph(n, param, seed)
    elif model == "geometric":
        return generator.geometric_graph(n, param, seed)
    elif model == "grid":
        side = max(2, int(round(n ** 0.5)))
        return generator.grid_graph(side)
    raise ValueError(f"Unknown model: {model}")


def sweep(
    model: str,
    n: int,
    param_values: list[float],
    trials: int = 10,
    percolation_type: str | None = None,
    base_param: float | None = None,
    seed: int | None = None,
) -> SweepResult:
    """Run Monte Carlo sweep over a parameter range."""
    rng = random.Random(seed)
    points: list[SweepPoint] = []

    for pval in param_values:
        n_connected = 0
        n_complex = 0
        n_both = 0

        for t in range(trials):
            trial_seed = rng.randint(0, 2**31)

            if percolation_type:
                g, _ = _make_graph(model, n, base_param if base_param is not None else pval, trial_seed)
                perc_rng = random.Random(trial_seed + t)
                if percolation_type == "node":
                    g = node_percolation(g, pval, perc_rng)
                elif percolation_type == "edge":
                    g = edge_percolation(g, pval, perc_rng)
                elif percolation_type == "composed":
                    g = node_percolation(g, pval, perc_rng)
                    g = edge_percolation(g, pval, random.Random(trial_seed + t + 1))
            else:
                g, _ = _make_graph(model, n, pval, trial_seed)

            connected = nx.is_connected(g) if g.number_of_nodes() > 0 else False
            comps = list(nx.connected_components(g))
            cpx = _is_complex(g, comps)

            if connected:
                n_connected += 1
            if cpx:
                n_complex += 1
            if connected and cpx:
                n_both += 1

        points.append(SweepPoint(
            param=pval,
            p_connected=n_connected / trials,
            p_complex=n_complex / trials,
            p_both=n_both / trials,
        ))

    param_name = "q" if percolation_type else ("p" if model == "binomial" else "r" if model == "geometric" else "n")
    return SweepResult(model=model, n=n, param_name=param_name, points=points, trials=trials)
