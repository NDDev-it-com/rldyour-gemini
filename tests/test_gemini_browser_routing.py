import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_browser_routing_validates():
    gemini_contract.validate_browser_routing()


def test_native_boundaries_validate():
    gemini_contract.validate_native_boundaries()

