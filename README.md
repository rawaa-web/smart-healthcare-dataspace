# Smart Healthcare Data Space

Three hospitals train **one PyTorch model together with Federated Learning**
(Flower, FedAvg) **without sharing raw data**. Eclipse Dataspace Connectors
(EDC, Java) handle publish / discover / contract negotiation, a FastAPI
gateway exposes the state, and a Streamlit dashboard visualises it. Local
runs use Docker Compose; the target deployment is Kubernetes (Minikube).

Team of 5 students (S1–S5), mixed Windows (Git Bash) / Linux / macOS.

```
hospital A ─┐                                    ┌─ edc-a (S3, Java)
hospital B ─┼─ Flower clients ─> flower-server:8080│─ edc-b       contracts (publish /
hospital C ─┘   (local CSVs only)   FedAvg rounds └─ edc-c        discover / negotiate)
                                          │
                                          v  POST /metrics
                                     api:8000 (S4, FastAPI — "no contract, no training")
                                          ^
                                          |  GET /health, /metrics, ...
                                   dashboard:8501 (S1, Streamlit)
```

## Prerequisites

| Tool            | Version            | Needed by            |
| --------------- | ------------------ | -------------------- |
| Python          | **3.11**           | everyone             |
| Git             | recent             | everyone             |
| Docker Desktop  | with Compose v2+   | S1, S2, S4, S5       |
| kubectl         | 1.28+              | S5                   |
| Minikube        | latest             | S5                   |
| JDK             | 17                 | S3 only (EDC)        |

On Windows Git Bash you also need GNU make: `choco install make` or
`scoop install make`.

## Quick start

```bash
git clone https://github.com/rawaa-web/smart-healthcare-dataspace.git
cd smart-healthcare-dataspace
bash scripts/setup.sh   # creates .venv (Python 3.11), installs pinned deps, creates .env
make check              # environment + version-consistency checks
make test               # smoke tests
make lint               # ruff
```

`scripts/setup.sh` detects Windows (`.venv/Scripts`) and Linux/macOS
(`.venv/bin`) automatically.

## Daily commands

| Command        | Effect                                                  |
| -------------- | ------------------------------------------------------- |
| `make data`    | build the 3 hospital CSVs (TODO S1)                     |
| `make build`   | build all Docker images (fl-client from the repo root)  |
| `make up`      | start the local stack (`docker compose up -d`)          |
| `make down`    | stop it                                                 |
| `make deploy`  | apply `k8s/` to Minikube (namespace first)              |
| `make clean`   | remove caches                                           |

## Team and ownership (one folder = one image = one owner)

| Role | Owner of                                                            |
| ---- | ------------------------------------------------------------------- |
| S1   | `ml/`, `data/`, `services/dashboard/`                               |
| S2   | `services/fl-server/`, `services/fl-client/`                        |
| S3   | `services/edc/` (Java, excluded from compose/kustomize for now)     |
| S4   | `services/api/`                                                     |
| S5   | `k8s/`, `Makefile`, `docker-compose.yml`, CI                        |

Everyone reads [`docs/interfaces.md`](docs/interfaces.md) first: all
contracts (function signatures, API bodies, ports, env vars) live there.

## Git rules

- Branch per role (`s1-ml`, `s2-fl`, `s3-edc`, `s4-api`, `s5-k8s`), PRs into
  `main` using the PR template; one reviewer (the service owner).
- Never force-push. Never commit secrets or `.env` (only `.env.example`).
- Small, logical commits (`chore:`, `feat:`, `docs:`, `ci:`, `test:`).
- If a contract changed, update `docs/interfaces.md` in the same PR.

## Demo steps (end of sprint)

1. `make data` — build the hospital CSVs.
2. `make build && make up` — local stack: gateway on
   <http://localhost:8000/docs>, dashboard on <http://localhost:8501>.
3. Federated training: `docker compose run fl-client-a` etc. (TODO S2).
4. `make deploy` — same topology on Minikube, then
   `kubectl -n smart-healthcare port-forward svc/dashboard 8501:8501`.
