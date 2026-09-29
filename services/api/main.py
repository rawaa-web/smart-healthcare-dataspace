"""S4: FastAPI gateway — the single entry point for the dashboard and the FL server.

While MOCK_MODE=true (the default) every endpoint returns canned JSON from
mock_data.py, so the dashboard and tests work before the EDC connectors
(S3) exist. The "no contract, no training" gate lives in
POST /training/start. Contracts and sample JSON: docs/interfaces.md.

Owner: S4.
"""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from mock_data import MOCK_CONNECTORS, MOCK_CONTRACTS, MOCK_LOGS, MOCK_TRAINING_APPROVED
from pydantic import BaseModel

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

app = FastAPI(title="Smart Healthcare Data Space API", version="0.1.0")

_metrics: list[dict] = []
_trainings: list[dict] = []


class MetricPayload(BaseModel):
    """Body of POST /metrics — one aggregated round, sent by the FL server."""

    round: int
    accuracy: float
    loss: float
    time: float


@app.get("/health")
def health() -> dict:
    """Liveness probe used by the dashboard, the FL server and CI."""
    return {"status": "ok", "mock_mode": MOCK_MODE}


@app.get("/connectors/status")
def connectors_status() -> list[dict]:
    """Status of the EDC connectors (edc-a, edc-b, edc-c)."""
    return MOCK_CONNECTORS


@app.get("/contracts")
def contracts() -> list[dict]:
    """Data contracts negotiated with the hospitals."""
    return MOCK_CONTRACTS


@app.post("/metrics")
def post_metric(payload: MetricPayload) -> dict:
    """Store one aggregated training round (sent by the FL server)."""
    metric = payload.model_dump()
    _metrics.append(metric)
    return {"stored": len(_metrics), "metric": metric}


@app.get("/metrics")
def get_metrics() -> list[dict]:
    """All training rounds recorded so far."""
    return _metrics


@app.get("/logs")
def logs() -> list[dict]:
    """Audit trail of connector activity (publish / negotiate / transfer)."""
    return MOCK_LOGS


@app.post("/training/start")
def training_start() -> dict:
    """The "no contract, no training" gate.

    Training may only start when an approved data contract covers the
    hospitals. In MOCK_MODE the gate always passes.
    """
    if not MOCK_MODE:
        raise HTTPException(
            status_code=501,
            detail="Real EDC contract negotiation is not implemented yet (S3/S4).",
        )
    training = {"training_id": len(_trainings) + 1, "status": "approved"}
    _trainings.append(training)
    return training


@app.get("/training/approved")
def training_approved() -> dict:
    """Contracts currently approved for training."""
    return MOCK_TRAINING_APPROVED
