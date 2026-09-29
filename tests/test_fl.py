"""S2 smoke tests — placeholder until the Flower services are implemented (owner S2)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_module(relative_path: str, module_name: str):
    """Import a service stub without turning services/ into a package."""
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fl_stubs_exposed():
    """The fl-server and fl-client stubs are importable and have a main()."""
    server = _load_module("services/fl-server/server.py", "fl_server_stub")
    client = _load_module("services/fl-client/client.py", "fl_client_stub")
    assert callable(server.main)
    assert callable(client.main)
