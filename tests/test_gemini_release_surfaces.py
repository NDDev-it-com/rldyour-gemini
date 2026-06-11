import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_antigravity_policy_validates():
    gemini_contract.validate_antigravity_policy()


def test_serena_memories_validate():
    gemini_contract.validate_serena_memories()


def test_all_validates():
    gemini_contract.validate_all(strict=False)
