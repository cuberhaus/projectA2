from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NodeData:
    id: int
    x: float
    y: float
    component: int = -1


@dataclass(slots=True)
class GraphData:
    nodes: list[NodeData]
    edges: list[tuple[int, int]]
    n: int = 0
    connected: bool = False
    is_complex: bool = False
    n_components: int = 0

    def __post_init__(self):
        if not self.n:
            self.n = len(self.nodes)


@dataclass(slots=True)
class SweepPoint:
    param: float
    p_connected: float
    p_complex: float
    p_both: float


@dataclass(slots=True)
class SweepResult:
    model: str
    n: int
    param_name: str
    points: list[SweepPoint]
    trials: int
