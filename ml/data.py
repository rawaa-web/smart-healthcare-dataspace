"""S1: load one hospital CSV into PyTorch train/test loaders.

Contract (docs/interfaces.md):
    load_data(csv_path) -> (train_loader, test_loader, input_dim)

Owner: S1.
"""


def load_data(csv_path):
    """Load one hospital CSV.

    Args:
        csv_path: path to a hospital CSV (data/hospitals/a.csv, b.csv, c.csv).

    Returns:
        (train_loader, test_loader, input_dim).
    """
    raise NotImplementedError("S1: implement ml/data.py::load_data")
