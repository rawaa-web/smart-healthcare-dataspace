"""S1: PyTorch model and local train/test helpers.

Contracts (docs/interfaces.md):
    Net(input_dim)                            -> model
    train(model, loader, epochs, lr) -> float (average training loss)
    test(model, loader)               -> (loss, accuracy)

Owner: S1.
"""


class Net:
    """Small PyTorch MLP for binary classification on the hospital data."""

    def __init__(self, input_dim):
        """Build the model. `input_dim` is the number of CSV features."""
        raise NotImplementedError("S1: implement ml/model.py::Net")


def train(model, loader, epochs, lr):
    """Train `model` on `loader` for `epochs` epochs at learning rate `lr`.

    Returns the average training loss (float).
    """
    raise NotImplementedError("S1: implement ml/model.py::train")


def test(model, loader):
    """Evaluate `model` on `loader`.

    Returns (loss, accuracy).
    """
    raise NotImplementedError("S1: implement ml/model.py::test")
