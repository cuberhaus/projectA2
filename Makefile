# Sphinx documentation + Web app targets
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help install dev web-build docker-build docker-up docker-down docker-logs tar clean

default: help

install: ## Install web frontend dependencies
	cd web/frontend && npm install

dev: ## Start backend + frontend dev servers
	cd web && uvicorn backend.app:app --host 127.0.0.1 --port 8085 --reload &
	cd web/frontend && npm run dev

web-build: ## Build frontend for production
	cd web/frontend && npm run build

docker-build: ## Build Docker image
	docker compose build

docker-up: ## Start Docker container
	docker compose up -d

docker-down: ## Stop Docker container
	docker compose down

docker-logs: ## Tail container logs
	docker compose logs -f

tar: ## Package sources for submission
	tar -cvf PROJ-1.tar graph.py source/ requirements.txt build/ README.md

docs: ## Build Sphinx documentation
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean: ## Clean build artifacts
	rm -rf web/frontend/dist web/frontend/node_modules PROJ-1.tar

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
