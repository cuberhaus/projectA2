from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import generator, analysis

app = FastAPI(title="Phase Transitions Explorer")
_pool = ThreadPoolExecutor(max_workers=2)

DIST_DIR = Path(__file__).parent.parent / "frontend" / "dist"


class GenerateRequest(BaseModel):
    model: str = "binomial"
    n: int = 50
    param: float = 0.1
    seed: Optional[int] = None


class PercolateRequest(BaseModel):
    model: str = "binomial"
    n: int = 50
    param: float = 0.1
    seed: Optional[int] = None
    percolation_type: str = "node"
    q: float = 0.5


class SweepRequest(BaseModel):
    model: str = "binomial"
    n: int = 50
    param_min: float = 0.0
    param_max: float = 1.0
    param_steps: int = 20
    trials: int = 10
    percolation_type: Optional[str] = None
    base_param: Optional[float] = None
    seed: Optional[int] = None


def _graph_to_dict(data):
    return {
        "nodes": [{"id": nd.id, "x": nd.x, "y": nd.y, "component": nd.component} for nd in data.nodes],
        "edges": data.edges,
        "n": data.n,
        "connected": data.connected,
        "is_complex": data.is_complex,
        "n_components": data.n_components,
    }


@app.get("/api/status")
async def status():
    return {"status": "ok"}


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    try:
        if req.model == "grid":
            side = max(2, int(round(req.n ** 0.5)))
            g, data = generator.grid_graph(side)
        elif req.model == "geometric":
            g, data = generator.geometric_graph(req.n, req.param, req.seed)
        elif req.model == "binomial":
            g, data = generator.binomial_graph(req.n, req.param, req.seed)
        else:
            raise HTTPException(400, f"Unknown model: {req.model}")
    except Exception as e:
        raise HTTPException(400, str(e))

    data = analysis.annotate(g, data)
    return _graph_to_dict(data)


@app.post("/api/percolate")
async def percolate(req: PercolateRequest):
    import random as _random

    try:
        if req.model == "grid":
            side = max(2, int(round(req.n ** 0.5)))
            g, data = generator.grid_graph(side)
        elif req.model == "geometric":
            g, data = generator.geometric_graph(req.n, req.param, req.seed)
        elif req.model == "binomial":
            g, data = generator.binomial_graph(req.n, req.param, req.seed)
        else:
            raise HTTPException(400, f"Unknown model: {req.model}")
    except Exception as e:
        raise HTTPException(400, str(e))

    rng = _random.Random(req.seed)
    if req.percolation_type == "node":
        g = analysis.node_percolation(g, req.q, rng)
    elif req.percolation_type == "edge":
        g = analysis.edge_percolation(g, req.q, rng)
    elif req.percolation_type == "composed":
        g = analysis.node_percolation(g, req.q, rng)
        g = analysis.edge_percolation(g, req.q, _random.Random((req.seed or 0) + 1))

    surviving = set(g.nodes())
    for nd in data.nodes:
        if nd.id not in surviving:
            nd.component = -1
    data.edges = [(u, v) for u, v in g.edges()]
    data = analysis.annotate(g, data)
    nodes_out = [nd for nd in data.nodes if nd.id in surviving]
    data.nodes = nodes_out

    return _graph_to_dict(data)


@app.post("/api/sweep")
async def sweep(req: SweepRequest):
    import asyncio

    param_values = [
        req.param_min + i * (req.param_max - req.param_min) / max(req.param_steps - 1, 1)
        for i in range(req.param_steps)
    ]

    def run():
        return analysis.sweep(
            model=req.model,
            n=req.n,
            param_values=param_values,
            trials=req.trials,
            percolation_type=req.percolation_type,
            base_param=req.base_param,
            seed=req.seed,
        )

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(_pool, run)

    return {
        "model": result.model,
        "n": result.n,
        "param_name": result.param_name,
        "trials": result.trials,
        "points": [
            {"param": p.param, "p_connected": p.p_connected, "p_complex": p.p_complex, "p_both": p.p_both}
            for p in result.points
        ],
    }


if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="static")
