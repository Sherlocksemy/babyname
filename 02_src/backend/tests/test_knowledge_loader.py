from __future__ import annotations

import json

import pytest

from backend.app.core.knowledge_loader import KnowledgeLoadError, KnowledgeLoader
from backend.app.schemas.knowledge import DatasetSpec


def test_loads_required_knowledge_sets() -> None:
    loaded = KnowledgeLoader().load_all()

    assert loaded["compliance_hanzi"].row_count == 8105
    assert loaded["char_base_info"].row_count == 8105
    assert loaded["char_semantic"].row_count == 8105
    assert loaded["kangxi_strokes"].row_count == 8105
    assert "知" in loaded["char_semantic"].data


def test_missing_required_file_raises(tmp_path) -> None:
    spec = DatasetSpec(name="missing", relative_path="missing.csv", kind="csv", required=True)
    loader = KnowledgeLoader(tmp_path, dataset_specs=(spec,))

    with pytest.raises(KnowledgeLoadError):
        loader.load_all()


def test_utf8_sig_csv_and_json_are_supported(tmp_path) -> None:
    csv_path = tmp_path / "sample.csv"
    json_path = tmp_path / "sample.json"
    csv_path.write_text("char,value\n知,ok\n", encoding="utf-8-sig")
    json_path.write_text(json.dumps({"知": {"value": "ok"}}, ensure_ascii=False), encoding="utf-8-sig")

    csv_rows, csv_encoding = KnowledgeLoader.read_csv(csv_path)
    json_data, json_encoding = KnowledgeLoader.read_json(json_path)

    assert csv_rows == [{"char": "知", "value": "ok"}]
    assert json_data["知"]["value"] == "ok"
    assert csv_encoding == "utf-8-sig"
    assert json_encoding == "utf-8-sig"
