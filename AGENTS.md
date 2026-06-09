# projectA2

Frozen FIB-UPC algorithmics coursework studying phase transitions in random graphs — connectivity and giant-component emergence across binomial (Erdos-Renyi), geometric, and grid (`graella`) families. Mixes a Python/NetworkX analysis driver with C++ graph generators and an optional Lit + FastAPI web demo.

## Architecture

- [graph.py](graph.py) — main driver: generation, connectivity/complexity computation, matplotlib plots; uses `networkx`, `numpy`, `tqdm`.
- [cpp_codes/](cpp_codes/) — standalone C++ programs (`graphGenerator.cc`, `Generador.cc`, `connectedComponent.cc`, `Connex_i_Complex.cc`, `ConnexComplex.cc`) producing graph text files consumed by `graph.py`.
- [source/](source/) + `build/` — Sphinx documentation (`make docs` → `build/html`).
- [web/](web/) — Lit + Vite frontend and FastAPI + NetworkX backend for interactive percolation/Monte Carlo demos.
- [proves/](proves/) — scratch/experimental scripts.

## Build and Test

- Python deps: `pip install -r requirements.txt` (NetworkX, NumPy, matplotlib, tqdm, Sphinx).
- Run experiments: `python graph.py` (reads pre-generated graph files from disk).
- Docs: `make docs`. Submission tarball: `make tar`.
- Web: `make dev` (backend on `:8085` + Vite) or `docker compose up -d`.

## Pitfalls

- Frozen coursework — do not refactor `graph.py` or `cpp_codes/` semantics; preserve filenames referenced by `make tar`.
- Catalan naming is intentional (`graella` = grid, `proves` = tests).
- Monte Carlo sweeps over `N`, `p`, trials can take a long time; reduce parameters when smoke-testing.
- `graph.py` reads files via `os.getcwd()` + relative directory strings — run from the repo root.

See [README.md](README.md).
