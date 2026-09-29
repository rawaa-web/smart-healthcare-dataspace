# Smart Healthcare Data Space — developer commands (owner S5).
# Requires GNU make. On Windows Git Bash: choco install make  |  scoop install make

# Use the venv python when it exists (Windows and Linux/macOS layouts).
VENV_PY := $(wildcard .venv/Scripts/python.exe)
ifeq ($(VENV_PY),)
VENV_PY := $(wildcard .venv/bin/python)
endif
ifeq ($(VENV_PY),)
VENV_PY := python
endif

.PHONY: setup check test lint data build up down deploy clean

setup:              ## python 3.11 venv + pinned deps + .env + check_env
	bash scripts/setup.sh

check:              ## environment + version-consistency checks
	$(VENV_PY) scripts/check_env.py
	$(VENV_PY) scripts/check_versions.py

test:               ## pytest (smoke tests until services are implemented)
	$(VENV_PY) -m pytest

lint:               ## ruff
	$(VENV_PY) -m ruff check .

data:               ## build the 3 hospital CSVs (S1)
	@echo "TODO: implement ml/prepare_data.py (owner S1)"

build:              ## build all Docker images (fl-client from the repo root)
	docker build -t fl-server:dev services/fl-server
	docker build -f services/fl-client/Dockerfile -t fl-client:dev .
	docker build -t api:dev services/api
	docker build -t dashboard:dev services/dashboard

up:                 ## start the local stack (EDC excluded, see services/edc/)
	docker compose up -d

down:               ## stop the local stack
	docker compose down

deploy:             ## Kubernetes (Minikube): namespace first, then the kustomization
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -k k8s/

clean:              ## remove caches only (never touches .venv or data)
	rm -rf .pytest_cache .ruff_cache
	find . \( -name ".git" -o -name ".venv" -o -name "venv" \) -prune \
	  -o -type d -name "__pycache__" -exec rm -rf {} +
