from backend.app.core.knowledge_loader import KnowledgeLoader


def test_knowledge_loader_reads_all_layers():
    loader = KnowledgeLoader()
    data = loader.load()
    assert len(data["compliance"]) == 8105
    assert len(data["char_semantic"]) == 8105
    assert len(data["kangxi"]) == 8105
    assert data["shijing"]
    assert data["zodiac_taboo"]


def test_knowledge_audit_allows_only_warnings():
    report = KnowledgeLoader().audit(write_report=True)
    assert report["status"] in {"ok", "warning"}
    assert not report["missing_files"]
    assert report["duplicate_counts"]["compliance"] == 0

