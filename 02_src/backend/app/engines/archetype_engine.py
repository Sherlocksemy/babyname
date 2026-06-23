from __future__ import annotations

from collections import defaultdict

from app.catalogs.archetype_catalog import get_archetype_catalog
from app.catalogs.mapping_catalog import ARCHETYPE_CONFLICTS, STRUCTURE_ARCHETYPE_MATRIX, ensure_all_catalogs
from app.schemas.naming_input import NamingInput


class ArchetypeEngine:
    def __init__(self) -> None:
        ensure_all_catalogs()
        self.catalog = get_archetype_catalog()
        self.by_id = {item["id"]: item for item in self.catalog}

    def select(self, structures: list[dict], naming_input: NamingInput) -> dict:
        preference_text = " ".join(naming_input.style_preferences)
        scores: dict[str, float] = defaultdict(float)
        details: dict[str, list[dict]] = defaultdict(list)

        for index, structure in enumerate(structures):
            rank_weight = max(1.0, 3.0 - index)
            for mapping in STRUCTURE_ARCHETYPE_MATRIX.get(structure["id"], []):
                value = mapping["weight"] * rank_weight * 5
                archetype_id = mapping["archetype_id"]
                scores[archetype_id] += value
                details[archetype_id].append(
                    {
                        "source": "STRUCTURE_ARCHETYPE_MATRIX",
                        "structure_id": structure["id"],
                        "score": value,
                    }
                )

        for item in self.catalog:
            for keyword in item["keywords"]:
                if keyword in preference_text:
                    scores[item["id"]] += 8
                    details[item["id"]].append({"source": "STYLE_KEYWORD_MATCH", "keyword": keyword, "score": 8})

        for archetype_id, conflicts in ARCHETYPE_CONFLICTS.items():
            if archetype_id not in scores:
                continue
            for conflict in conflicts:
                if conflict in scores and scores[conflict] > 0:
                    scores[archetype_id] -= 3
                    details[archetype_id].append({"source": "ARCHETYPE_CONFLICT_PENALTY", "conflict": conflict, "score": -3})

        ranked = []
        for archetype_id, score in scores.items():
            item = self.by_id[archetype_id]
            ranked.append(
                {
                    "id": archetype_id,
                    "name": item["name"],
                    "score": round(score, 4),
                    "score_details": details[archetype_id],
                    "keywords": item["keywords"],
                    "semantic_roles": item["semantic_roles"],
                    "preferred_culture_sources": item["preferred_culture_sources"],
                }
            )
        ranked.sort(key=lambda row: (-row["score"], row["id"]))
        top3 = ranked[:3]
        return {"primary_archetype": top3[0], "secondary_archetypes": top3[1:], "top_archetypes": top3, "candidate_archetypes": ranked[:4]}
