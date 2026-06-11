import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_manifest_validates():
    gemini_contract.validate_manifest()


def test_settings_validates():
    gemini_contract.validate_settings()

