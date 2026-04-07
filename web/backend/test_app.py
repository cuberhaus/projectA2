"""Tests for the projectA2 FastAPI backend (Phase Transitions Explorer)."""

import pytest
from fastapi.testclient import TestClient

from .app import app

client = TestClient(app)


def test_status():
    r = client.get("/api/status")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_generate_binomial():
    r = client.post("/api/generate", json={
        "model": "binomial", "n": 20, "param": 0.3, "seed": 42,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["n"] == 20
    assert "nodes" in data
    assert "edges" in data
    assert "connected" in data
    assert "n_components" in data


def test_generate_geometric():
    r = client.post("/api/generate", json={
        "model": "geometric", "n": 20, "param": 0.3, "seed": 42,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["n"] == 20


def test_generate_grid():
    r = client.post("/api/generate", json={"model": "grid", "n": 16})
    assert r.status_code == 200
    assert r.json()["n"] > 0


def test_generate_unknown_model():
    r = client.post("/api/generate", json={"model": "quantum"})
    assert r.status_code == 400


def test_generate_deterministic():
    payload = {"model": "binomial", "n": 30, "param": 0.2, "seed": 99}
    r1 = client.post("/api/generate", json=payload)
    r2 = client.post("/api/generate", json=payload)
    assert r1.json()["edges"] == r2.json()["edges"]


def test_generate_node_has_fields():
    r = client.post("/api/generate", json={"n": 10, "param": 0.5, "seed": 1})
    node = r.json()["nodes"][0]
    assert "id" in node
    assert "component" in node


def test_percolate_node():
    r = client.post("/api/percolate", json={
        "model": "binomial", "n": 30, "param": 0.3, "seed": 42,
        "percolation_type": "node", "q": 0.5,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["n"] <= 30


def test_percolate_edge():
    r = client.post("/api/percolate", json={
        "model": "binomial", "n": 30, "param": 0.3, "seed": 42,
        "percolation_type": "edge", "q": 0.5,
    })
    assert r.status_code == 200


def test_percolate_composed():
    r = client.post("/api/percolate", json={
        "model": "binomial", "n": 30, "param": 0.3, "seed": 42,
        "percolation_type": "composed", "q": 0.5,
    })
    assert r.status_code == 200


def test_percolate_unknown_model():
    r = client.post("/api/percolate", json={"model": "nope", "n": 10, "param": 0.1})
    assert r.status_code == 400


def test_sweep():
    r = client.post("/api/sweep", json={
        "model": "binomial", "n": 20,
        "param_min": 0.0, "param_max": 0.5,
        "param_steps": 3, "trials": 2, "seed": 42,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["model"] == "binomial"
    assert data["n"] == 20
    assert len(data["points"]) == 3
    p = data["points"][0]
    assert "param" in p
    assert "p_connected" in p
    assert "p_complex" in p


def test_sweep_with_percolation():
    r = client.post("/api/sweep", json={
        "model": "binomial", "n": 20,
        "param_min": 0.0, "param_max": 1.0,
        "param_steps": 3, "trials": 2,
        "percolation_type": "node", "base_param": 0.3, "seed": 42,
    })
    assert r.status_code == 200
    assert len(r.json()["points"]) == 3
