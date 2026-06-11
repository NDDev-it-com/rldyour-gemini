import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_hooks_validate():
    gemini_contract.validate_hooks()


def test_subagents_validate():
    gemini_contract.validate_subagents()


def test_projection_parity_validates():
    gemini_contract.validate_projection_parity()
