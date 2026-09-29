# Interfaces — read this first

Every contract between services lives here. **If a PR changes a contract, it
must update this file** (see `.github/pull_request_template.md`).

## 1. Service names, ports and hosts

| Service            | Folder                | Host name (compose & k8s) | Port  | Notes                          |
| ------------------ | --------------------- | ------------------------- | ----- | ------------------------------ |
| FL server          | `services/fl-server`  | `flower-server`           | 8080  | Flower gRPC (FedAvg)           |
| FL client A/B/C    | `services/fl-client`  | `fl-client-a|b|c`         | —     | same image, 3 hospitals        |
| API gateway        | `services/api`        | `api`                     | 8000  | FastAPI                        |
| Dashboard          | `services/dashboard`  | `dashboard`               | 8501  | Streamlit                      |
| EDC connectors     | `services/edc` (S3)   | `edc-a`, `edc-b`, `edc-c` | 19193 | management API, **planned**    |

The EDC connectors are Java services owned by S3 and are not wired into
docker-compose / kustomization yet.

## 2. Environment variables

| Variable         | Used by          | Default (compose)      | Meaning                             |
| ---------------- | ---------------- | ---------------------- | ----------------------------------- |
| `MOCK_MODE`      | api              | `true`                 | canned JSON without real connectors |
| `API_URL`        | dashboard, fl-server | `http://api:8000`  | base URL of the gateway             |
| `SERVER_ADDRESS` | fl-server, fl-client | `0.0.0.0:8080` / `flower-server:8080` | Flower gRPC endpoint |
| `NUM_ROUNDS`     | fl-server        | `5`                    | number of FedAvg rounds             |
| `HOSPITAL_ID`    | fl-client        | `a`                    | `a`, `b` or `c`                     |
| `DATA_PATH`      | fl-client        | `/data/data.csv`       | local CSV, mounted **read-only**    |

## 3. ml/ contracts (owner S1)

```python
from ml.data import load_data          # (csv_path) -> (train_loader, test_loader, input_dim)
from ml.model import Net, train, test  # Net(input_dim)
                                       # train(model, loader, epochs, lr) -> float
                                       # test(model, loader)              -> (loss, accuracy)
```

CSV contract (data/hospitals/a.csv, b.csv, c.csv): one row per patient, a
header line, numeric feature columns plus one binary target column
`heart_disease`. Small, public, reproducible, committed.

## 4. API endpoints (owner S4)

All bodies are JSON. While `MOCK_MODE=true` every response is canned
(`services/api/mock_data.py`).

### GET /health

```json
{ "status": "ok", "mock_mode": true }
```

### POST /metrics

Sent by the FL server after every aggregated round.

Request body:

```json
{ "round": 1, "accuracy": 0.74, "loss": 0.51, "time": 12.3 }
```

Response:

```json
{ "stored": 1, "metric": { "round": 1, "accuracy": 0.74, "loss": 0.51, "time": 12.3 } }
```

### GET /metrics

```json
[ { "round": 1, "accuracy": 0.74, "loss": 0.51, "time": 12.3 } ]
```

### GET /connectors/status

```json
[ { "connector": "edc-a", "hospital": "a", "status": "up",
    "management_url": "http://edc-a:19193/management" } ]
```

### GET /contracts

```json
[ { "contract_id": "contract-a", "hospital": "a", "status": "active" } ]
```

### POST /training/start

The **"no contract, no training" gate**: without an approved data contract
training is refused. Response while mock mode:

```json
{ "training_id": 1, "status": "approved" }
```

### GET /training/approved

```json
{ "approved": true, "contracts": ["contract-a", "contract-b", "contract-c"] }
```

### GET /logs

```json
[ { "time": "2026-01-01T10:00:00Z", "connector": "edc-a",
    "action": "publish", "asset": "hospital-a-data" } ]
```

## 5. EDC connector management APIs (owner S3, planned)

Base URL per connector: `http://edc-a|b|c:19193/management`. S4 calls them
exclusively through `services/api/edc_client.py`:

```python
publish_asset(connector, payload)   # publish a hospital dataset as an asset
request_catalog(connector)          # discover the other hospitals' assets
negotiate_contract(connector, asset_id)
fetch_logs(connector)               # audit trail
```
