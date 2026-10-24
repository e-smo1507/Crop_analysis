from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
pytestmark = pytest.mark.skipif(not (ROOT / "models" / "model_full.pkl").exists(),
                                reason="train the model first")


def test_estimate_both_modes():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception
    at.button[0].click().run()
    assert not at.exception and at.metric[0].value.endswith("tonnes per hectare")
    at.radio[0].set_value(at.radio[0].options[1]).run()
    at.button[0].click().run()
    assert not at.exception and at.metric[0].value
