from __future__ import annotations

from dataclasses import dataclass


SEMANTIC_ROLE_VERSION = "semantic_roles.v1"

SEMANTIC_CATEGORIES: dict[str, str] = {
    "WISDOM": "认知、思辨、明达",
    "LEARNING": "读书、文教、学养",
    "VIRTUE": "德行、仁义、诚信",
    "CULTIVATION": "修养、涵养、持守",
    "ASPIRATION": "志向、进取、远望",
    "CAPABILITY": "才具、通达、承担",
    "PEACE": "安宁、温和、稳定",
    "AESTHETIC": "清雅、温润、美感",
    "BRIGHTNESS": "光明、晨曜、昭朗",
    "LANDSCAPE": "山川、洲渚、自然",
    "WATER": "水泽、清流、润泽",
    "SPACE": "天地、宇宙、广阔",
    "GROWTH": "生长、初始、新生",
    "ORDER": "礼序、均衡、法度",
    "CULTURE": "文章、书卷、经典",
    "OBJECT": "器物、工具、物件",
    "FUNCTION": "虚词、功能字、连接字",
    "UNKNOWN": "未能从知识库稳定判断",
}

ROLE_BY_CATEGORY: dict[str, str] = {
    "WISDOM": "明辨知思",
    "LEARNING": "书卷学养",
    "VIRTUE": "德行品格",
    "CULTIVATION": "修身涵养",
    "ASPIRATION": "志向开阔",
    "CAPABILITY": "才具通达",
    "PEACE": "安宁温和",
    "AESTHETIC": "清雅温润",
    "BRIGHTNESS": "光明昭朗",
    "LANDSCAPE": "山川自然",
    "WATER": "水泽润清",
    "SPACE": "天地广阔",
    "GROWTH": "新生向上",
    "ORDER": "礼序均衡",
    "CULTURE": "文章文脉",
    "OBJECT": "器物意象",
    "FUNCTION": "功能连接",
    "UNKNOWN": "语义待审",
}

KEYWORDS_BY_CATEGORY: dict[str, tuple[str, ...]] = {
    "WISDOM": ("知", "智", "慧", "思", "睿", "哲", "悟", "辨", "察", "识", "明", "理", "微"),
    "LEARNING": ("学", "问", "闻", "书", "卷", "章", "文", "典", "经", "史", "读"),
    "VIRTUE": ("德", "仁", "义", "礼", "信", "诚", "敬", "正", "贤", "谦", "恭", "善", "蓄"),
    "CULTIVATION": ("修", "养", "涵", "慎", "省", "怀", "守", "持", "蓄", "穆"),
    "ASPIRATION": ("志", "远", "弘", "毅", "达", "成", "承", "望", "鸿", "凌", "卓", "越"),
    "CAPABILITY": ("才", "能", "博", "达", "敏", "捷", "干", "任", "承"),
    "PEACE": ("安", "宁", "和", "温", "静", "平", "怡", "恬", "宜", "晏"),
    "AESTHETIC": ("清", "雅", "润", "微", "美", "芳", "兰", "芷", "瑾", "瑜", "灵", "婉"),
    "BRIGHTNESS": ("明", "昭", "朗", "晖", "晨", "曜", "煦", "光", "华", "星"),
    "LANDSCAPE": ("山", "川", "岳", "峰", "岩", "岚", "洲", "原", "林", "松", "竹"),
    "WATER": ("水", "江", "河", "海", "泽", "泉", "清", "沅", "沐", "涵", "润", "汀", "洲"),
    "SPACE": ("天", "宇", "宙", "庭", "序", "广", "宏", "旷"),
    "GROWTH": ("新", "初", "生", "春", "萌", "茂", "荣", "禾", "苗"),
    "ORDER": ("礼", "序", "衡", "均", "则", "正", "章", "矩", "度"),
    "CULTURE": ("文", "章", "书", "墨", "诗", "辞", "典", "经", "雅"),
    "OBJECT": ("墨", "书", "笔", "印", "刀", "器", "具", "车", "舟", "衣"),
    "FUNCTION": ("之", "其", "而", "于", "以", "与", "若", "兮", "乎", "也", "焉", "矣"),
}

RADICAL_CATEGORY_HINTS: dict[str, str] = {
    "氵": "WATER",
    "水": "WATER",
    "山": "LANDSCAPE",
    "木": "GROWTH",
    "艹": "GROWTH",
    "日": "BRIGHTNESS",
    "火": "BRIGHTNESS",
    "灬": "BRIGHTNESS",
    "宀": "PEACE",
    "玉": "AESTHETIC",
    "王": "AESTHETIC",
    "言": "CULTURE",
    "讠": "CULTURE",
}

CATEGORY_PRIORITY: dict[str, int] = {
    "WISDOM": 1,
    "VIRTUE": 2,
    "CULTIVATION": 3,
    "ASPIRATION": 4,
    "LEARNING": 5,
    "AESTHETIC": 6,
    "PEACE": 7,
    "BRIGHTNESS": 8,
    "CAPABILITY": 9,
    "CULTURE": 10,
    "ORDER": 11,
    "WATER": 12,
    "LANDSCAPE": 13,
    "SPACE": 14,
    "GROWTH": 15,
    "OBJECT": 90,
    "FUNCTION": 91,
    "UNKNOWN": 99,
}

EXPLICIT_PRIMARY_CATEGORY: dict[str, str] = {
    "修": "CULTIVATION",
    "远": "ASPIRATION",
    "泽": "WATER",
    "星": "BRIGHTNESS",
    "宇": "SPACE",
    "安": "PEACE",
    "序": "ORDER",
    "川": "LANDSCAPE",
    "洲": "WATER",
    "峰": "LANDSCAPE",
    "山": "LANDSCAPE",
}

EXPLICIT_CATEGORY_OVERRIDES: dict[str, list[str]] = {
    "宫": ["OBJECT", "SPACE"],
    "室": ["OBJECT", "SPACE"],
    "殿": ["OBJECT", "SPACE"],
    "宝": ["OBJECT", "AESTHETIC"],
    "玉": ["OBJECT", "AESTHETIC"],
    "珠": ["OBJECT", "AESTHETIC"],
    "山": ["LANDSCAPE"],
    "林": ["LANDSCAPE", "GROWTH"],
    "江": ["WATER", "LANDSCAPE"],
    "河": ["WATER", "LANDSCAPE"],
    "湖": ["WATER", "LANDSCAPE"],
    "海": ["WATER", "LANDSCAPE", "SPACE"],
    "泉": ["WATER", "AESTHETIC"],
    "泽": ["WATER", "AESTHETIC"],
    "清": ["WATER", "AESTHETIC"],
    "涛": ["WATER", "LANDSCAPE"],
    "洪": ["WATER", "SPACE"],
    "峰": ["LANDSCAPE", "ASPIRATION"],
    "岳": ["LANDSCAPE", "ASPIRATION"],
    "岭": ["LANDSCAPE"],
    "风": ["LANDSCAPE", "AESTHETIC"],
    "云": ["SPACE", "AESTHETIC"],
    "雪": ["AESTHETIC", "WATER"],
    "阳": ["BRIGHTNESS", "LANDSCAPE"],
    "晖": ["BRIGHTNESS", "AESTHETIC"],
    "明": ["BRIGHTNESS", "WISDOM"],
    "世": ["ORDER", "CULTURE"],
    "国": ["ORDER", "CULTURE"],
    "东": ["SPACE", "BRIGHTNESS"],
    "西": ["SPACE"],
    "南": ["SPACE"],
    "北": ["SPACE"],
    "富": ["CAPABILITY"],
    "贵": ["CAPABILITY"],
    "发": ["ASPIRATION", "CAPABILITY"],
    "兴": ["ASPIRATION", "BRIGHTNESS"],
    "飞": ["ASPIRATION", "SPACE"],
    "学": ["LEARNING", "ASPIRATION"],
    "文": ["CULTURE", "LEARNING"],
    "劳": ["FUNCTION"],
    "见": ["FUNCTION"],
    "生": ["GROWTH"],
    "周": ["ORDER"],
    "勤": ["CULTIVATION", "ASPIRATION"],
    "诗": ["CULTURE", "AESTHETIC"],
    "书": ["CULTURE", "LEARNING"],
    "谊": ["VIRTUE", "PEACE"],
    "惠": ["VIRTUE", "PEACE"],
    "仁": ["VIRTUE"],
    "德": ["VIRTUE", "CULTIVATION"],
    "信": ["VIRTUE"],
    "敬": ["VIRTUE", "CULTIVATION"],
    "正": ["VIRTUE", "ORDER"],
    "谦": ["VIRTUE", "CULTIVATION"],
    "贤": ["VIRTUE", "WISDOM"],
    "承": ["CAPABILITY", "CULTURE"],
    "思": ["WISDOM", "CULTURE"],
    "知": ["WISDOM", "LEARNING"],
    "安": ["PEACE"],
    "宁": ["PEACE"],
    "楚": ["AESTHETIC", "LANDSCAPE"],
    "莹": ["AESTHETIC", "BRIGHTNESS"],
    "芳": ["AESTHETIC", "GROWTH"],
    "芬": ["AESTHETIC", "GROWTH"],
    "兰": ["AESTHETIC", "CULTURE"],
    "芊": ["AESTHETIC", "GROWTH"],
    "深": ["WATER", "WISDOM"],
    "远": ["ASPIRATION", "SPACE"],
}


@dataclass(frozen=True)
class SemanticMapping:
    categories: list[str]
    roles: list[str]
    keywords: list[str]
    basis: list[str]


class SemanticRoleMapper:
    def map_character(self, profile: dict, culture_links: list[dict] | None = None) -> SemanticMapping:
        char = str(profile.get("char") or "")
        base = profile.get("base") or {}
        semantic = profile.get("semantic") or {}
        kangxi = profile.get("kangxi") or {}
        radical = str(base.get("radical") or kangxi.get("kangxi_radical") or "")
        components = kangxi.get("components") or []
        definition_head = self._definition_head(str(semantic.get("definition") or ""))
        ancient_head = self._definition_head(str(semantic.get("ancient_meaning") or ""))
        text = "".join(
            [
                char,
                definition_head,
                ancient_head,
                radical,
                "".join(str(item) for item in components),
            ]
        )
        categories: list[str] = []
        keywords: list[str] = []
        basis: list[str] = []

        if radical in RADICAL_CATEGORY_HINTS:
            categories.append(RADICAL_CATEGORY_HINTS[radical])
            basis.append(f"radical:{radical}")

        for category, tokens in KEYWORDS_BY_CATEGORY.items():
            hits = [token for token in tokens if token and token in text]
            if hits:
                categories.append(category)
                keywords.extend(hits[:3])
                basis.append(f"keyword:{category}")

        for link in culture_links or []:
            for keyword in link.get("keywords") or []:
                if keyword in ("君子", "品格", "仁德"):
                    categories.append("VIRTUE")
                elif keyword in ("清雅", "温润"):
                    categories.append("AESTHETIC")
                elif keyword in ("志向", "高远"):
                    categories.append("ASPIRATION")
                elif keyword in ("书卷", "文脉"):
                    categories.append("CULTURE")

        if char in EXPLICIT_CATEGORY_OVERRIDES:
            categories = list(EXPLICIT_CATEGORY_OVERRIDES[char])
            basis.append(f"explicit_category:{char}")
        else:
            categories = list(dict.fromkeys(categories))
            categories.sort(key=lambda item: CATEGORY_PRIORITY.get(item, 80))
        explicit = EXPLICIT_PRIMARY_CATEGORY.get(char)
        if explicit:
            if explicit in categories:
                categories.remove(explicit)
            categories.insert(0, explicit)
        if not categories:
            categories = ["UNKNOWN"]
            basis.append("fallback:unknown")

        primary_categories = [item for item in categories if item not in {"OBJECT", "FUNCTION", "UNKNOWN"}] or categories
        roles = [ROLE_BY_CATEGORY[item] for item in primary_categories[:3]]
        return SemanticMapping(
            categories=categories[:5],
            roles=list(dict.fromkeys(roles)),
            keywords=list(dict.fromkeys(keywords))[:10],
            basis=list(dict.fromkeys(basis)),
        )

    @staticmethod
    def _definition_head(text: str) -> str:
        if not text:
            return ""
        for marker in ("--", "。", "；", ";", "\n"):
            if marker in text:
                text = text.split(marker, 1)[0]
        return text[:90]
