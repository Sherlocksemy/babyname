from __future__ import annotations

from backend.app.core.knowledge_audit import KnowledgeAudit


def test_audit_reports_core_status_and_checks(tmp_path) -> None:
    audit = KnowledgeAudit()
    report = audit.audit()
    json_path, md_path = audit.write_reports(report, tmp_path)

    assert report["overall_status"] in {"ok", "warning"}
    assert report["datasets"]["compliance_hanzi"]["row_count"] == 8105
    assert report["datasets"]["char_semantic"]["row_count"] == 8105
    assert json_path.exists()
    assert md_path.exists()

    check_names = {check["name"] for check in report["checks"]}
    assert "character_joinability" in check_names
    assert "culture_schema_and_name_candidates" in check_names
    assert "bazi_rules_operability" in check_names
