"""Verify the development environment.

Fails (exit code 1) if:
- Python is not 3.11.x
- any dependency from requirements.txt cannot be imported
- torch is NOT the CPU-only build

Prints the version of every package on success.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import shutil
import sys
from pathlib import Path

# dist name on PyPI -> module name to import
PACKAGES = {
    "torch": "torch",
    "flwr": "flwr",
    "numpy": "numpy",
    "pandas": "pandas",
    "scikit-learn": "sklearn",
    "fastapi": "fastapi",
    "uvicorn[standard]": "uvicorn",
    "pydantic": "pydantic",
    "requests": "requests",
    "python-dotenv": "dotenv",
    "streamlit": "streamlit",
    "pytest": "pytest",
    "ruff": None,  # ruff ships a binary, there is nothing to import
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def main() -> None:
    if sys.version_info[:2] != (3, 11):
        fail(f"Python 3.11.x is required, found {sys.version.split()[0]}")
    print(f"python {sys.version.split()[0]}  OK")

    for dist_name, module_name in PACKAGES.items():
        try:
            version = importlib.metadata.version(dist_name.split("[")[0])
        except importlib.metadata.PackageNotFoundError:
            fail(f"package '{dist_name}' is not installed")
        if module_name is not None:
            try:
                importlib.import_module(module_name)
            except ImportError as exc:
                fail(f"package '{dist_name}' is installed but cannot be imported: {exc}")
        print(f"{dist_name:<20} {version}")

    import torch

    if torch.version.cuda is not None:
        fail(f"torch must be the CPU-only build, got CUDA build {torch.__version__} "
             "(keep '--extra-index-url https://download.pytorch.org/whl/cpu' first in "
             "requirements.txt)")
    print(f"torch {torch.__version__}  CPU-only build  OK")

    ruff_binary = Path(sys.prefix) / (
        "Scripts/ruff.exe" if sys.platform == "win32" else "bin/ruff"
    )
    if shutil.which("ruff") is None and not ruff_binary.is_file():
        fail("ruff binary not found (neither on PATH nor in the venv)")
    print("ruff binary available  OK")

    print("\nEnvironment check passed.")


if __name__ == "__main__":
    main()
