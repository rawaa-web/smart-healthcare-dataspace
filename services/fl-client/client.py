"""S2: Flower client stub — the same image runs as hospitals A, B and C.

Reads its configuration from environment variables and prints them, so the
per-hospital wiring (one CSV mounted read-only at /data/data.csv) can be
smoke-tested before the real Flower NumPyClient is implemented.

Owner: S2.
"""

from __future__ import annotations

import os

HOSPITAL_ID = os.getenv("HOSPITAL_ID", "a")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "flower-server:8080")
DATA_PATH = os.getenv("DATA_PATH", "/data/data.csv")


def main() -> None:
    """Print the client configuration, then exit.

    TODO S2: load {DATA_PATH} with ml.data.load_data and connect a
    Flower NumPyClient to {SERVER_ADDRESS}.
    """
    print("[fl-client] HOSPITAL_ID    =", HOSPITAL_ID)
    print("[fl-client] SERVER_ADDRESS =", SERVER_ADDRESS)
    print("[fl-client] DATA_PATH      =", DATA_PATH)
    print(f"[fl-client] stub: hospital {HOSPITAL_ID} training not implemented yet (S2)")


if __name__ == "__main__":
    main()
