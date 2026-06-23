from __future__ import annotations


COMPATIBILITY: dict[str, dict[str, str]] = {
    "S01": {"A01": "HIGH", "A02": "HIGH", "A08": "MEDIUM"},
    "S02": {"A03": "HIGH", "A04": "HIGH", "A07": "HIGH", "A12": "MEDIUM"},
    "S03": {"A05": "HIGH", "A10": "HIGH", "A04": "MEDIUM"},
    "S04": {"A08": "HIGH", "A10": "HIGH", "A01": "MEDIUM"},
    "S05": {"A02": "HIGH", "A06": "HIGH", "A07": "HIGH", "A09": "HIGH"},
    "S06": {"A01": "HIGH", "A02": "HIGH", "A08": "MEDIUM"},
    "S07": {"A03": "HIGH", "A07": "HIGH", "A11": "MEDIUM"},
    "S08": {"A08": "HIGH", "A03": "MEDIUM", "A09": "MEDIUM"},
    "S09": {"A09": "HIGH", "A01": "MEDIUM"},
    "S10": {"A04": "HIGH", "A05": "HIGH", "A06": "HIGH", "A02": "MEDIUM"},
    "S11": {"A10": "HIGH", "A11": "HIGH", "A08": "MEDIUM"},
    "S12": {"A12": "HIGH", "A03": "MEDIUM"},
}

LEVEL_SCORE = {"HIGH": 100.0, "MEDIUM": 72.0, "LOW": 45.0, "CONFLICT": 0.0}


def evaluate_compatibility(structure_id: str, archetype_id: str) -> dict:
    level = COMPATIBILITY.get(structure_id, {}).get(archetype_id, "LOW")
    if structure_id == "S09" and archetype_id == "A03":
        level = "CONFLICT"
    reason = f"COMPATIBILITY_{level}"
    return {
        "structure_archetype_compatibility": LEVEL_SCORE[level],
        "compatibility_level": level,
        "compatibility_reason_codes": [reason],
        "passed": level not in {"CONFLICT"},
        "top3_allowed": level == "HIGH",
    }
