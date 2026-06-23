from __future__ import annotations

from app.schemas.candidate import NameCandidate


SURNAME_PINYIN = {
    "林": ("lin", 2),
    "陈": ("chen", 2),
    "黄": ("huang", 2),
    "郑": ("zheng", 4),
    "欧阳": ("ou-yang", 1),
}

SURNAME_CHAR_AFFINITY = {
    "林": {"松": 16, "竹": 14, "泉": 12, "清": 8, "乔": 8, "岳": 8, "山": 6, "云": 6},
    "陈": {"承": 16, "维": 12, "新": 12, "文": 10, "章": 8, "仁": 6, "贤": 6},
    "黄": {"昭": 16, "明": 14, "曜": 14, "光": 12, "衡": 10, "晨": 8, "华": 8},
    "郑": {"正": 18, "则": 14, "信": 10, "谦": 10, "敬": 4, "衡": 8},
    "欧阳": {"朗": 18, "曜": 16, "晨": 14, "云": 12, "天": 12, "海": 10, "光": 10, "贤": 12, "庭": 10, "谦": 12, "章": 10},
}


class SurnameFitEvaluator:
    def evaluate(self, surname: str, candidate: NameCandidate) -> dict:
        surname_py, surname_tone = SURNAME_PINYIN.get(surname, (surname, 0))
        tones = [surname_tone] + [int((char.mandarin[0].get("tone") if char and char.mandarin else 0) or 0) for char in [candidate.first_char, candidate.second_char]]
        initials = [surname_py.split("-")[-1][:1]] + [self._initial(char) for char in [candidate.first_char, candidate.second_char]]
        finals = [surname_py.split("-")[-1][-2:]] + [self._final(char) for char in [candidate.first_char, candidate.second_char]]
        initial_conflicts = [idx for idx in range(len(initials) - 1) if initials[idx] and initials[idx] == initials[idx + 1]]
        final_conflicts = [idx for idx in range(len(finals) - 1) if finals[idx] and finals[idx] == finals[idx + 1]]
        rhythm_score = 86 + len(set(tones)) * 3 - len(initial_conflicts) * 8 - len(final_conflicts) * 5
        if len(surname) > 1:
            rhythm_score -= 4
        visual_balance = 88 - (6 if len(surname) > 1 and len(candidate.given_name) == 2 else 0)
        affinity = self._surname_affinity(surname, candidate.given_name)
        score = max(0, min(100, rhythm_score * 0.48 + visual_balance * 0.27 + affinity * 0.25))
        return {
            "surname": surname,
            "given_name": candidate.given_name,
            "tone_pattern": "-".join(str(tone) for tone in tones),
            "initial_conflicts": initial_conflicts,
            "final_conflicts": final_conflicts,
            "rhythm_score": round(rhythm_score, 2),
            "visual_balance_score": round(visual_balance, 2),
            "surname_affinity_score": round(affinity, 2),
            "surname_fit_score": round(score, 2),
        }

    @staticmethod
    def _initial(char) -> str:
        if not char or not char.mandarin:
            return ""
        return str(char.mandarin[0].get("pinyin", ""))[:1]

    @staticmethod
    def _final(char) -> str:
        if not char or not char.mandarin:
            return ""
        pinyin = str(char.mandarin[0].get("pinyin", ""))
        return pinyin[-2:]

    @staticmethod
    def _surname_affinity(surname: str, given_name: str) -> float:
        weights = SURNAME_CHAR_AFFINITY.get(surname, {})
        score = 72.0 + sum(weights.get(char, 0) for char in given_name)
        return max(55.0, min(100.0, score))
