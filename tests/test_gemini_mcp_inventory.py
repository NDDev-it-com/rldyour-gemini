import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_mcp_inventory_validates():
    gemini_contract.validate_mcp_inventory()


def test_retired_residue_validates():
    gemini_contract.validate_retired_residue()

