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

## Tech Stack

- **Python** with NetworkX, NumPy, matplotlib, tqdm
- **C++** for graph generation and component algorithms
- **Sphinx** for documentation

## Building the Docs

```bash
make html
```
