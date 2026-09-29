"""S3 smoke tests — the EDC connectors are Java services owned by S3.

Until S3 delivers them, only the placeholder structure is checked here.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_edc_placeholder_structure():
    """services/edc contains its README and the config/ folder."""
    assert (ROOT / "services" / "edc" / "README.md").is_file()
    assert (ROOT / "services" / "edc" / "config").is_dir()
