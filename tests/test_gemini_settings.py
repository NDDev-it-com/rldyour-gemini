import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_version_surfaces_match():
    gemini_contract.validate_version_surfaces()


def test_runtime_baseline_matches_policy():
    gemini_contract.validate_runtime_baseline(strict=False)

