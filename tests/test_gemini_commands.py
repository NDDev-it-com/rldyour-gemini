import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import gemini_contract


def test_commands_validate():
    gemini_contract.validate_commands()


def test_skills_validate():
    gemini_contract.validate_skills()

