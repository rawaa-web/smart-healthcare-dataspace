"""S2: Flower FedAvg server stub.

Reads its configuration from environment variables and prints them, so the
docker-compose / Kubernetes wiring can be smoke-tested before the real FedAvg
strategy is implemented. Contracts: docs/interfaces.md.

Owner: S2.
"""

from __future__ import annotations

import os

SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")
NUM_ROUNDS = os.getenv("NUM_ROUNDS", "5")
API_URL = os.getenv("API_URL", "http://api:8000")


def main() -> None:
    """Print the server configuration, then exit.

    TODO S2: run Flower's FedAvg strategy, aggregate client metrics and POST
    each round to {API_URL}/metrics (body in docs/interfaces.md).
    """
    print("[fl-server] SERVER_ADDRESS =", SERVER_ADDRESS)
    print("[fl-server] NUM_ROUNDS     =", NUM_ROUNDS)
    print("[fl-server] API_URL        =", API_URL)
    print("[fl-server] stub: FedAvg aggregation not implemented yet (S2)")


if __name__ == "__main__":
    main()
