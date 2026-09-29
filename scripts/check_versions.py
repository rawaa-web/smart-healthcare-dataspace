"""Fail if the same package is pinned to different versions in different requirements files.

Scans ./requirements.txt and services/*/requirements.txt, normalizes package
names (case, '_' vs '-') and reports any package that appears with more than
one pinned version. Exit code 0 when consistent, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "requirements.txt", *sorted((ROOT / "services").glob("*/requirements.txt"))]

# name[extras]==version   (environment markers after ';' are ignored)
LINE_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?==([^\s;#]+)")


def normalize(name: str) -> str:
    return name.lower().replace("_", "-")


def main() -> int:
    pins: dict[str, list[tuple[str, Path]]] = {}
    missing: list[Path] = []
    unpinned: list[tuple[Path, str]] = []

    for path in FILES:
        if not path.is_file():
            missing.append(path)
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith(("#", "-")):
                continue  # comments and options such as --extra-index-url
            match = LINE_RE.match(line)
            if match is None:
                unpinned.append((path, line))
                continue
            name, version = normalize(match.group(1)), match.group(2)
            pins.setdefault(name, []).append((version, path))

    status = 0
    for path in missing:
        print(f"ERROR: missing requirements file: {path.relative_to(ROOT)}")
        status = 1
    for path, line in unpinned:
        print(f"WARNING: unpinned requirement in {path.relative_to(ROOT)}: {line}")

    print("\nPinned versions (package -> version @ files):")
    conflicts: list[str] = []
    for name in sorted(pins):
        versions = {version for version, _ in pins[name]}
        files = ", ".join(str(path.relative_to(ROOT)) for _, path in pins[name])
        print(f"  {name:<16} {', '.join(sorted(versions)):<12} ({files})")
        if len(versions) > 1:
            conflicts.append(name)

    if conflicts:
        print(f"\nERROR: version conflicts for: {', '.join(conflicts)}")
        return 1
    print("\nAll requirements files are consistent.")
    return status


if __name__ == "__main__":
    sys.exit(main())
