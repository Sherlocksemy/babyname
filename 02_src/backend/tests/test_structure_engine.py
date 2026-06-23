from __future__ import annotations

from app.engines.structure_engine import StructureEngine
from app.schemas.naming_input import NamingInput


def test_structure_engine_uses_only_documented_structures(alpha_input) -> None:
    result = StructureEngine().select(NamingInput.from_dict(alpha_input))
    allowed = {f"S{index:02d}" for index in range(1, 13)}

    assert result["primary_structure"]["id"] in allowed
    assert len(result["top_structures"]) == 3
    assert all(item["id"] in allowed for item in result["top_structures"])


def test_structure_engine_is_deterministic_for_same_seed(alpha_input) -> None:
    naming_input = NamingInput.from_dict(alpha_input)
    engine = StructureEngine()

    assert engine.select(naming_input) == engine.select(naming_input)
