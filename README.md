# Project A2

Algorithmics course project on phase transitions in graph properties. Analyzes connectivity and complexity across different random graph families (binomial, geometric, grid) using both Python and C++.

## Overview

The project studies how structural properties of random graphs change as parameters vary, focusing on phenomena like the emergence of giant connected components. It includes graph generation, property computation, and visualization.

## Structure

```
├── graph.py              # Main script: graph generation, connectivity analysis, plotting
├── cpp_codes/
│   ├── Connex_i_Complex.cc
│   ├── graphGenerator.cc
│   ├── connectedComponent.cc
│   ├── Generador.cc
│   └── ConnexComplex.cc
├── proves/               # Test scripts
│   ├── main.py
│   ├── cool_function.py
│   ├── nsquare.py
│   └── graph_old.py
├── source/               # Sphinx documentation sources
│   ├── conf.py
│   ├── index.rst
│   └── graph.rst
├── build/                # Generated HTML documentation
├── misc/                 # Notes and instructions
├── Makefile              # Sphinx docs + tar packaging
└── requirements.txt      # Python dependencies
```

## Web App

An interactive web frontend for exploring connectivity and complexity phase transitions on random graphs with real-time percolation animation and Monte Carlo sweep charts.

**Stack:** Lit (Web Components, Vite) + HTML5 Canvas + D3.js charts + FastAPI backend (NetworkX)

### Quick Start

```bash
# Docker (recommended)
docker compose up -d        # http://localhost:8085

# Dev mode
make web-dev                # Backend :8085, Vite dev server
```

### Features

- Three random graph models: Binomial (Erdos-Renyi), Geometric, Grid
- Animated percolation scrubber — watch edges appear as p increases
- Canvas rendering with per-model layouts (force, geometric, grid)
- D3.js line charts for Monte Carlo phase transition curves
- Configurable N, p range, trials for sweep experiments

### Web Structure

```
web/
├── frontend/          # Lit + Vite + Canvas + D3.js
│   └── src/
│       ├── components/        # Lit Web Components
│       └── styles/            # Dark theme CSS
├── backend/           # FastAPI + NetworkX
│   └── app.py
└── requirements.txt
```

## Tech Stack

- **Python** with NetworkX, NumPy, matplotlib, tqdm
- **C++** for graph generation and component algorithms
- **Lit** (Web Components) + **Canvas** + **D3.js** for the interactive web frontend
- **FastAPI** + **NetworkX** for the web backend
- **Sphinx** for documentation

## Building the Docs

```bash
make html
```
