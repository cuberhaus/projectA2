from __future__ import annotations

# ── Phase 14 (Option A) — Sentry SDK + JSON-line stdout (no-op if missing) ─
try:
    from ._sentry_obs import (  # type: ignore[import-not-found]
        init_observability,
        breadcrumb as _crumb,
        span as _span,
        tag as _tag,
        SessionIdMiddleware as _SessionIdMiddleware,
    )

    init_observability(service="phase-transitions")
except ImportError:
    from contextlib import contextmanager

    def _tag(*_a, **_kw):
        return None

    def _crumb(*_a, **_kw):
        return None

    @contextmanager
    def _span(*_a, **_kw):
        yield None

    class _SessionIdMiddleware:  # type: ignore[no-redef]
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            await self.app(scope, receive, send)

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import generator, analysis

app = FastAPI(title="Phase Transitions Explorer")
app.add_middleware(_SessionIdMiddleware)
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
    _tag("model", req.model)
    _tag("n", req.n)
    _tag("param", req.param)
    _crumb(
        "graph", "generate",
        model=req.model, n=req.n, param=req.param, seed=req.seed,
    )
    with _span(
        "graph.generate",
        description=f"{req.model} n={req.n} param={req.param}",
        model=req.model, n=req.n, param=req.param,
    ):
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

    _tag("model", req.model)
    _tag("n", req.n)
    _tag("param", req.param)
    _tag("percolation_type", req.percolation_type)
    _tag("q", req.q)
    _crumb(
        "percolation", "percolate request",
        model=req.model, n=req.n, percolation_type=req.percolation_type, q=req.q,
    )
    with _span(
        "percolation.run",
        description=f"{req.percolation_type} q={req.q} on {req.model} n={req.n}",
        model=req.model, percolation_type=req.percolation_type, q=req.q,
    ):
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

    _tag("model", req.model)
    _tag("n", req.n)
    _tag("trials", req.trials)
    if req.percolation_type:
        _tag("percolation_type", req.percolation_type)
    _crumb(
        "sweep", "sweep range",
        model=req.model, n=req.n,
        param_min=req.param_min, param_max=req.param_max,
        steps=req.param_steps, trials=req.trials,
        percolation_type=req.percolation_type,
    )

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
    with _span(
        "sweep.run",
        description=f"{req.model} n={req.n} steps={req.param_steps} trials={req.trials}",
        trials=req.trials, steps=req.param_steps,
    ):
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
