from __future__ import annotations

import random

from app.catalogs.mapping_catalog import ensure_all_catalogs
from app.catalogs.structure_catalog import get_structure_catalog
from app.schemas.naming_input import NamingInput


class StructureEngine:
    def __init__(self) -> None:
        ensure_all_catalogs()
        self.catalog = get_structure_catalog()
        self.by_id = {item["id"]: item for item in self.catalog}

    def select(self, naming_input: NamingInput) -> dict:
        preference_text = " ".join(naming_input.style_preferences + naming_input.liked_chars)
        rng = random.Random(naming_input.generation_seed)
        results = []
        for item in self.catalog:
            score = 30.0
            details = []
            for keyword in item["keywords"]:
                if keyword and keyword in preference_text:
                    score += 14.0
                    details.append({"reason": "STYLE_KEYWORD_MATCH", "keyword": keyword, "score": 14.0})
            for role in item["semantic_roles"]:
                if role and role in preference_text:
                    score += 10.0
                    details.append({"reason": "SEMANTIC_ROLE_MATCH", "keyword": role, "score": 10.0})
            if naming_input.region == "teochew" and item["id"] in {"S05", "S08", "S09"}:
                score += 2.0
                details.append({"reason": "REGION_TONE_PREFERENCE", "score": 2.0})
            if naming_input.gender == "male" and item["id"] in {"S02", "S03", "S10"}:
                score += 1.5
                details.append({"reason": "GENDER_STYLE_PRIOR", "score": 1.5})
            if naming_input.gender == "female" and item["id"] in {"S08", "S09", "S11"}:
                score += 1.5
                details.append({"reason": "GENDER_STYLE_PRIOR", "score": 1.5})
            score += rng.random() * 0.0001
            if not details:
                details.append({"reason": "BASELINE_CATALOG_PRIOR", "score": 30.0})
            results.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "score": round(score, 4),
                    "reason_codes": [detail["reason"] for detail in details],
                    "score_details": details,
                    "semantic_roles": item["semantic_roles"],
                    "keywords": item["keywords"],
                    "preferred_culture_sources": item["preferred_culture_sources"],
                }
            )
        results.sort(key=lambda row: (-row["score"], row["id"]))
        top3 = results[:3]
        return {"primary_structure": top3[0], "secondary_structures": top3[1:], "top_structures": top3, "candidate_structures": results[:6]}
