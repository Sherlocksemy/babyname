from __future__ import annotations

from backend.app.core.knowledge_loader import KnowledgeLoader


class WugeEngine:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.data = (loader or KnowledgeLoader()).load()
        self.kangxi = self.data["kangxi"]
        self.rules = self.data["wuge_rules"]

    def analyze(self, surname: str, given_name: str) -> dict:
        strokes = {ch: int(self.kangxi.get(ch, {}).get("kangxi_strokes") or 1) for ch in surname + given_name}
        s = [strokes[ch] for ch in surname]
        g = [strokes[ch] for ch in given_name]
        if len(surname) == 1 and len(given_name) == 1:
            grids = {"天格": s[0] + 1, "人格": s[0] + g[0], "地格": g[0] + 1, "外格": 2, "总格": s[0] + g[0]}
        elif len(surname) == 1:
            grids = {"天格": s[0] + 1, "人格": s[0] + g[0], "地格": sum(g), "外格": g[-1] + 1, "总格": s[0] + sum(g)}
        elif len(given_name) == 1:
            grids = {"天格": sum(s), "人格": s[-1] + g[0], "地格": g[0] + 1, "外格": s[0] + 1, "总格": sum(s) + g[0]}
        else:
            grids = {"天格": sum(s), "人格": s[-1] + g[0], "地格": sum(g), "外格": s[0] + g[-1], "总格": sum(s) + sum(g)}
        detail = {k: self.rules.get("stroke_math", {}).get(str(v), {"luck": "平", "meaning": "无对应数理说明"}) for k, v in grids.items()}
        lucky = sum(1 for item in detail.values() if item.get("luck") == "吉")
        return {"strokes": strokes, "grids": grids, "detail": detail, "score": min(10, 4 + lucky), "notes": "五格数理仅作传统文化参考，不作为决定性依据。"}

