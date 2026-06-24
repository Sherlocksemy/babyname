from __future__ import annotations


UNSUITABLE_CHARS = set(
    "乂乜儿几卜了么也兮乎哉矣焉其之而于以与或且及并把被将就很吗呢啊吧呗"
    "一二三四五六七八九十百千万亿零不无未非否"
    "旧币王夫女民臣父母鸟虫鱼菜草犬马口手目耳穴"
    "回侧届徒诸近罪"
)

NEGATIVE_HINTS = (
    "贬义",
    "恶",
    "病",
    "死",
    "灾",
    "祸",
    "残",
    "败",
    "毒",
    "怨",
    "哭",
    "哀",
    "凶",
    "杀",
    "亡",
)
NEGATIVE_CHARS = set("恶凶杀亡死灾祸残败毒怨哭哀罪")

TOOL_OBJECT_HINTS = ("器", "具", "刀", "斧", "锤", "盆", "桶", "车", "船", "锅", "碗")
FUNCTION_WORD_HINTS = ("代词", "介词", "助词", "语气词", "连词", "数词")
LOW_NAMEABILITY_DEFINITION_HINTS = ("作恶", "犯法", "旁边", "行不便", "步行", "回旋", "旋转", "秘密", "隐蔽")


class CharacterRiskClassifier:
    def classify(
        self,
        char: str,
        definition: str = "",
        homophone_risks: list[dict] | None = None,
    ) -> tuple[list[str], list[str]]:
        risk_codes: list[str] = []
        rejection_reasons: list[str] = []
        text = definition or ""

        if char in UNSUITABLE_CHARS:
            risk_codes.append("UNSUITABLE_FUNCTION_CHAR")
            rejection_reasons.append("obvious_non_name_character")
        if "贬义" in text or char in NEGATIVE_CHARS:
            risk_codes.append("NEGATIVE_SEMANTIC_HINT")
            rejection_reasons.append("negative_definition_hint")
        if any(hint in text for hint in FUNCTION_WORD_HINTS):
            risk_codes.append("FUNCTION_WORD_SEMANTIC")
            rejection_reasons.append("function_word_semantic")
        if any(hint in text[:80] for hint in LOW_NAMEABILITY_DEFINITION_HINTS):
            risk_codes.append("LOW_NAMEABILITY_DEFINITION")
            rejection_reasons.append("low_nameability_definition")
        if any(hint in text for hint in TOOL_OBJECT_HINTS):
            risk_codes.append("OBJECT_OR_TOOL_SEMANTIC")
        if homophone_risks:
            risk_codes.append("HOMOPHONE_RISK")
            rejection_reasons.append("homophone_blacklist")

        return list(dict.fromkeys(risk_codes)), list(dict.fromkeys(rejection_reasons))
