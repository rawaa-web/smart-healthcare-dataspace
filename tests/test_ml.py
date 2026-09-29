"""S1 smoke tests — placeholder until ml/ is implemented (owner S1)."""

import ml.data
import ml.model


def test_ml_contracts_exposed():
    """The documented ml/ contracts exist and are importable."""
    assert callable(ml.data.load_data)
    assert callable(ml.model.train)
    assert callable(ml.model.test)
    assert callable(ml.model.Net)
