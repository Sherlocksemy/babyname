from __future__ import annotations


CHAR_INFO: dict[str, dict] = {
    "知": {"role": "认知", "category": "wisdom", "quality": 95},
    "思": {"role": "思辨", "category": "wisdom", "quality": 92},
    "微": {"role": "细察", "category": "wisdom_detail", "quality": 88},
    "慎": {"role": "审慎", "category": "cultivation", "quality": 90},
    "辨": {"role": "辨析", "category": "wisdom_detail", "quality": 88},
    "闻": {"role": "闻学", "category": "learning", "quality": 84},
    "道": {"role": "道理", "category": "principle", "quality": 86},
    "文": {"role": "文气", "category": "culture", "quality": 82},
    "书": {"role": "书卷", "category": "object", "quality": 68},
    "墨": {"role": "文墨", "category": "object", "quality": 64},
    "言": {"role": "言辞", "category": "language", "quality": 72},
    "章": {"role": "文采", "category": "culture", "quality": 82},
    "德": {"role": "德行", "category": "virtue_core", "quality": 92},
    "仁": {"role": "仁德", "category": "virtue_label", "quality": 86},
    "贤": {"role": "贤德", "category": "virtue_label", "quality": 84},
    "义": {"role": "义理", "category": "virtue_core", "quality": 82},
    "礼": {"role": "礼序", "category": "virtue_order", "quality": 78},
    "信": {"role": "诚信", "category": "virtue_core", "quality": 80},
    "诚": {"role": "诚意", "category": "virtue_core", "quality": 86},
    "敬": {"role": "敬慎", "category": "cultivation", "quality": 86},
    "正": {"role": "正直", "category": "virtue_action", "quality": 88},
    "则": {"role": "准则", "category": "principle", "quality": 78},
    "行": {"role": "践行", "category": "virtue_action", "quality": 84},
    "景": {"role": "德望", "category": "virtue_image", "quality": 84},
    "怀": {"role": "怀抱", "category": "virtue_action", "quality": 84},
    "瑾": {"role": "美质", "category": "virtue_image", "quality": 88},
    "弘": {"role": "弘阔", "category": "aspiration", "quality": 88},
    "毅": {"role": "坚毅", "category": "resolve", "quality": 90},
    "修": {"role": "修养", "category": "cultivation", "quality": 88},
    "远": {"role": "远志", "category": "aspiration", "quality": 86},
    "能": {"role": "才能", "category": "capability", "quality": 82},
    "承": {"role": "传承", "category": "inheritance", "quality": 82},
    "维": {"role": "维系", "category": "inheritance", "quality": 76},
    "新": {"role": "新生", "category": "growth", "quality": 80},
    "灵": {"role": "灵秀", "category": "aesthetic", "quality": 82},
    "均": {"role": "均正", "category": "virtue_order", "quality": 78},
    "清": {"role": "清正", "category": "aesthetic", "quality": 88},
    "晏": {"role": "安宁", "category": "peace", "quality": 86},
    "和": {"role": "温和", "category": "peace", "quality": 84},
    "安": {"role": "安定", "category": "peace", "quality": 82},
    "宁": {"role": "宁静", "category": "peace", "quality": 84},
    "有": {"role": "持有", "category": "function", "quality": 62},
    "容": {"role": "包容", "category": "virtue_capacity", "quality": 86},
    "若": {"role": "如若", "category": "function", "quality": 58},
    "谷": {"role": "虚怀", "category": "landscape_symbol", "quality": 82},
    "牧": {"role": "涵养", "category": "cultivation", "quality": 78},
    "之": {"role": "连属", "category": "function", "quality": 55},
    "明": {"role": "光明", "category": "brightness", "quality": 88},
    "昭": {"role": "昭朗", "category": "brightness", "quality": 84},
    "嘉": {"role": "嘉善", "category": "virtue_praise", "quality": 84},
    "宜": {"role": "适宜", "category": "fit", "quality": 68},
    "宇": {"role": "空间", "category": "space", "quality": 72},
    "山": {"role": "山岳", "category": "landscape", "quality": 70},
    "川": {"role": "河川", "category": "landscape", "quality": 70},
    "洲": {"role": "水洲", "category": "landscape", "quality": 66},
    "泽": {"role": "水泽", "category": "landscape", "quality": 74},
    "星": {"role": "星象", "category": "image", "quality": 72},
    "云": {"role": "云气", "category": "image", "quality": 74},
    "序": {"role": "秩序", "category": "abstract", "quality": 66},
    "博": {"role": "博雅", "category": "capacity", "quality": 82},
    "达": {"role": "通达", "category": "aspiration", "quality": 80},
    "鸿": {"role": "鸿志", "category": "aspiration", "quality": 80},
    "凌": {"role": "凌云", "category": "aspiration", "quality": 76},
    "志": {"role": "志向", "category": "aspiration", "quality": 82},
    "望": {"role": "远望", "category": "aspiration", "quality": 78},
    "庭": {"role": "庭序", "category": "inheritance", "quality": 74},
    "彦": {"role": "贤彦", "category": "virtue_label", "quality": 78},
    "朗": {"role": "朗明", "category": "brightness", "quality": 82},
    "睿": {"role": "睿智", "category": "wisdom", "quality": 82},
    "谦": {"role": "谦逊", "category": "virtue_core", "quality": 84},
    "然": {"role": "自然", "category": "aesthetic", "quality": 72},
    "南": {"role": "南方", "category": "image", "quality": 70},
    "乔": {"role": "高乔", "category": "image", "quality": 76},
    "松": {"role": "松节", "category": "virtue_image", "quality": 80},
    "竹": {"role": "竹节", "category": "virtue_image", "quality": 80},
    "兰": {"role": "兰质", "category": "aesthetic", "quality": 78},
    "芷": {"role": "芳芷", "category": "aesthetic", "quality": 78},
    "华": {"role": "光华", "category": "brightness", "quality": 76},
    "光": {"role": "光明", "category": "brightness", "quality": 78},
    "辰": {"role": "星辰", "category": "image", "quality": 76},
    "晨": {"role": "晨光", "category": "brightness", "quality": 78},
    "曜": {"role": "曜明", "category": "brightness", "quality": 76},
    "煦": {"role": "温煦", "category": "peace", "quality": 78},
    "衡": {"role": "平衡", "category": "virtue_order", "quality": 78},
    "宥": {"role": "宽宥", "category": "virtue_capacity", "quality": 78},
    "初": {"role": "初心", "category": "growth", "quality": 74},
    "天": {"role": "天宇", "category": "space", "quality": 74},
    "地": {"role": "厚土", "category": "landscape", "quality": 66},
    "海": {"role": "海量", "category": "landscape_symbol", "quality": 78},
    "波": {"role": "波澜", "category": "image", "quality": 70},
    "岳": {"role": "山岳", "category": "landscape_symbol", "quality": 80},
    "岩": {"role": "岩峻", "category": "landscape_symbol", "quality": 76},
    "泉": {"role": "清泉", "category": "aesthetic", "quality": 76},
    "风": {"role": "风度", "category": "aesthetic", "quality": 74},
    "雨": {"role": "润泽", "category": "peace", "quality": 72},
    "渊": {"role": "深远", "category": "wisdom_detail", "quality": 78},
}

COMPLEMENTARY_CATEGORY_PAIRS: set[tuple[str, str]] = {
    ("wisdom", "wisdom_detail"),
    ("wisdom", "aspiration"),
    ("learning", "principle"),
    ("cultivation", "wisdom"),
    ("cultivation", "aspiration"),
    ("cultivation", "capability"),
    ("cultivation", "virtue_core"),
    ("virtue_action", "virtue_core"),
    ("virtue_action", "principle"),
    ("virtue_action", "virtue_image"),
    ("virtue_core", "brightness"),
    ("virtue_praise", "virtue_core"),
    ("aspiration", "resolve"),
    ("inheritance", "virtue_core"),
    ("inheritance", "growth"),
    ("aesthetic", "peace"),
    ("aesthetic", "aesthetic"),
    ("aesthetic", "virtue_order"),
    ("brightness", "brightness"),
    ("brightness", "aspiration"),
    ("space", "peace"),
    ("function", "virtue_capacity"),
    ("function", "landscape_symbol"),
    ("fit", "language"),
    ("virtue_image", "brightness"),
    ("culture", "virtue_core"),
    ("image", "culture"),
    ("wisdom", "capacity"),
    ("capacity", "virtue_core"),
    ("capacity", "aspiration"),
    ("brightness", "virtue_image"),
    ("brightness", "peace"),
    ("image", "brightness"),
    ("image", "aspiration"),
    ("image", "landscape_symbol"),
    ("landscape_symbol", "image"),
    ("landscape_symbol", "wisdom_detail"),
    ("space", "landscape_symbol"),
    ("peace", "virtue_core"),
    ("peace", "cultivation"),
    ("peace", "aesthetic"),
    ("aesthetic", "peace"),
    ("aesthetic", "virtue_image"),
    ("virtue_image", "aesthetic"),
    ("inheritance", "virtue_label"),
    ("growth", "virtue_core"),
}

WEAK_CATEGORY_COMBINATIONS: dict[tuple[str, str], str] = {
    ("virtue_label", "virtue_label"): "SEMANTIC_REDUNDANCY",
    ("object", "object"): "OBJECT_OBJECT_PAIR",
    ("object", "culture"): "OBJECT_OBJECT_PAIR",
    ("landscape", "landscape"): "LANDSCAPE_DUPLICATION",
    ("image", "abstract"): "SEMANTIC_DISCONNECT",
    ("landscape", "image"): "SEMANTIC_DISCONNECT",
    ("fit", "language"): "INCOMPLETE_PHRASE",
    ("space", "peace"): "FORCED_INTERPRETATION",
}


class SemanticCompositionValidator:
    def validate(self, given_name: str, structure_id: str = "", archetype_id: str = "") -> dict:
        if len(given_name) != 2:
            return self._result(given_name, "", "", "", 0, ["INCOMPLETE_PHRASE", "LOW_NAMEABILITY"], False)

        first, second = given_name[0], given_name[1]
        first_info = CHAR_INFO.get(first)
        second_info = CHAR_INFO.get(second)
        issues: list[str] = []
        if not first_info or not second_info:
            issues.append("SEMANTIC_DISCONNECT")
            return self._result(given_name, "", "", "", 42, issues, False)

        first_cat = first_info["category"]
        second_cat = second_info["category"]
        pair = (first_cat, second_cat)
        if pair in WEAK_CATEGORY_COMBINATIONS:
            issues.append(WEAK_CATEGORY_COMBINATIONS[pair])
        if first_cat == second_cat and first_cat in {"landscape", "object", "abstract"}:
            issues.append("LANDSCAPE_DUPLICATION" if first_cat == "landscape" else "ABSTRACT_LABEL_PAIR")
        if first_cat == second_cat and first_cat == "virtue_label":
            issues.append("SEMANTIC_REDUNDANCY")

        complementary = pair in COMPLEMENTARY_CATEGORY_PAIRS
        reverse_complementary = (second_cat, first_cat) in COMPLEMENTARY_CATEGORY_PAIRS
        base_quality = (first_info["quality"] + second_info["quality"]) / 2
        completeness = base_quality
        if complementary:
            completeness += 6
        elif reverse_complementary:
            completeness += 3
        else:
            completeness -= 12
            if "SEMANTIC_DISCONNECT" not in issues:
                issues.append("SEMANTIC_DISCONNECT")

        if issues:
            completeness -= min(30, len(set(issues)) * 8)
        if first_cat in {"object", "function"} and second_cat in {"object", "function"}:
            issues.append("LOW_NAMEABILITY")
            completeness -= 10

        completeness = max(0, min(96, completeness))
        passed = completeness >= 72 and not set(issues) & {"LOW_NAMEABILITY", "FORCED_INTERPRETATION", "INCOMPLETE_PHRASE"}
        meaning = self._derive_meaning(first, second, first_info["role"], second_info["role"]) if passed else ""
        return self._result(first + second, first_info["role"], second_info["role"], meaning, round(completeness, 2), sorted(set(issues)), passed)

    @staticmethod
    def _derive_meaning(first: str, second: str, first_role: str, second_role: str) -> str:
        return f"{first}取{first_role}之意，{second}取{second_role}之意，组合为{first_role}与{second_role}相成。"

    @staticmethod
    def _result(given_name: str, role_first: str, role_second: str, meaning: str, completeness: float, issues: list[str], passed: bool) -> dict:
        return {
            "given_name": given_name,
            "semantic_role_first": role_first,
            "semantic_role_second": role_second,
            "combined_meaning": meaning,
            "meaning_completeness": completeness,
            "issues": issues,
            "passed": passed,
        }
