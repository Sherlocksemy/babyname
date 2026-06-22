from __future__ import annotations

from app.schemas.knowledge import DatasetSpec


DATASET_SPECS: tuple[DatasetSpec, ...] = (
    DatasetSpec(
        name="compliance_hanzi",
        relative_path="01_compliance_layer/tongyong_guifan_hanzi.csv",
        kind="csv",
        primary_key="char",
        required_fields=("char", "level", "strokes_modern", "radical", "unicode"),
        category="compliance",
    ),
    DatasetSpec(
        name="char_base_info",
        relative_path="02_char_attribute_layer/char_base_info.csv",
        kind="csv",
        primary_key="char",
        required_fields=("char", "pinyin_main", "strokes_modern", "radical", "structure", "wubi"),
        category="character",
    ),
    DatasetSpec(
        name="char_semantic",
        relative_path="02_char_attribute_layer/char_semantic.json",
        kind="json",
        primary_key="char",
        required_fields=("definition", "positive_level", "common_level", "ancient_meaning"),
        category="character",
    ),
    DatasetSpec(
        name="kangxi_strokes",
        relative_path="02_char_attribute_layer/kangxi_strokes.json",
        kind="json",
        primary_key="char",
        required_fields=("kangxi_strokes", "kangxi_radical", "element", "components"),
        category="character",
    ),
    DatasetSpec(
        name="mandarin_pinyin",
        relative_path="03_pronunciation_layer/mandarin_pinyin.json",
        kind="json",
        primary_key="char",
        required_fields=("pinyin", "tone", "is_common", "rhyme"),
        category="pronunciation",
    ),
    DatasetSpec(
        name="teochew_pronunciation",
        relative_path="03_pronunciation_layer/teochew_pronunciation.csv",
        kind="csv",
        required_fields=("char", "pinyin_teochew", "tone", "accent", "is_colloquial", "is_literary"),
        category="pronunciation",
    ),
    DatasetSpec(
        name="homophone_blacklist",
        relative_path="03_pronunciation_layer/homophone_blacklist.csv",
        kind="csv",
        required_fields=("char", "homophone_char", "bad_meaning", "language_type"),
        category="pronunciation",
    ),
    DatasetSpec(
        name="shijing",
        relative_path="04_culture_origin_layer/shijing/shijing_full.json",
        kind="json",
        primary_key="id",
        required_fields=("id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates"),
        category="culture",
    ),
    DatasetSpec(
        name="chuci",
        relative_path="04_culture_origin_layer/chuci/chuci_full.json",
        kind="json",
        primary_key="id",
        required_fields=("id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates"),
        category="culture",
    ),
    DatasetSpec(
        name="tang_poetry",
        relative_path="04_culture_origin_layer/tang_poetry/tang_poetry.json",
        kind="json",
        primary_key="id",
        required_fields=("id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates"),
        category="culture",
    ),
    DatasetSpec(
        name="song_ci",
        relative_path="04_culture_origin_layer/song_ci/song_ci.json",
        kind="json",
        primary_key="id",
        required_fields=("id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates"),
        category="culture",
    ),
    DatasetSpec(
        name="sishuwujing",
        relative_path="04_culture_origin_layer/sishuwujing/sishuwujing.json",
        kind="json",
        primary_key="id",
        required_fields=("id", "title", "author", "dynasty", "chapter", "content", "translation", "keywords", "name_candidates"),
        category="culture",
    ),
    DatasetSpec(
        name="char_frequency",
        relative_path="05_name_popularity_layer/char_frequency.csv",
        kind="csv",
        primary_key="char",
        required_fields=("char", "gender_tendency", "frequency_rank", "heat_level", "era_tag"),
        category="popularity",
    ),
    DatasetSpec(
        name="top_names_blacklist",
        relative_path="05_name_popularity_layer/top_names_blacklist.csv",
        kind="csv",
        primary_key="name",
        required_fields=("name", "gender", "estimated_count", "heat_level"),
        category="popularity",
    ),
    DatasetSpec(
        name="bazi_rules",
        relative_path="06_numerology_layer/bazi_rules.json",
        kind="json",
        required_fields=("ten_gods", "patterns", "element_rules", "ushen_rules"),
        category="rules",
    ),
    DatasetSpec(
        name="wuge_rules",
        relative_path="06_numerology_layer/wuge_rules.json",
        kind="json",
        required_fields=("stroke_math", "sancai_config", "calculate_rules"),
        category="rules",
    ),
    DatasetSpec(
        name="zodiac_taboo",
        relative_path="06_numerology_layer/zodiac_taboo.csv",
        kind="csv",
        primary_key="zodiac",
        required_fields=("zodiac", "good_radicals", "bad_radicals", "good_meaning", "bad_meaning", "lucky_elements"),
        category="rules",
    ),
)


CULTURE_DATASETS = tuple(spec.name for spec in DATASET_SPECS if spec.category == "culture")

PLANNED_LAYER_DIRS: tuple[str, ...] = (
    "07_surname_layer",
    "08_archetype_layer",
    "09_imagery_layer",
    "10_quality_rules_layer",
)


def get_dataset_spec(name: str) -> DatasetSpec:
    for spec in DATASET_SPECS:
        if spec.name == name:
            return spec
    raise KeyError(f"Unknown dataset: {name}")
