from __future__ import annotations

from itertools import combinations, product

from backend.app.schemas.baby_profile import BabyProfile


class NameComposer:
    def compose(self, profile: BabyProfile, pool: list[dict], excluded_names: set[str] | None = None, locked_chars: list[str] | None = None, limit: int = 420) -> list[tuple[str, list[dict]]]:
        excluded_names = excluded_names or set()
        locked_chars = locked_chars or []
        by_char = {item["char"]: item for item in pool}
        usable = [item for item in pool if item["char"] not in profile.banned_chars]
        results: list[tuple[str, list[dict]]] = []
        if profile.name_length == 1:
            for item in usable:
                given = item["char"]
                if profile.surname + given not in excluded_names:
                    results.append((given, [item]))
                if len(results) >= limit:
                    break
            return results
        fixed = profile.generation_char or (locked_chars[0] if locked_chars else None)
        pairs = []
        if fixed and fixed in by_char:
            pairs = [(by_char[fixed], item) for item in usable if item["char"] != fixed]
            if profile.generation_char:
                pairs = pairs
        else:
            pairs = list(combinations(usable[:90], 2)) + [(b, a) for a, b in combinations(usable[:45], 2)]
        for first, second in pairs:
            if first["char"] == second["char"]:
                continue
            given = first["char"] + second["char"]
            if profile.surname + given in excluded_names:
                continue
            results.append((given, [first, second]))
            if len(results) >= limit:
                break
        return results

