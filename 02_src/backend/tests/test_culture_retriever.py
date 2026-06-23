from __future__ import annotations

from app.engines.archetype_engine import ArchetypeEngine
from app.engines.culture_retriever import CultureRetriever
from app.engines.structure_engine import StructureEngine
from app.indexes.culture_index import CultureIndex
from app.schemas.naming_input import NamingInput


def test_culture_retriever_returns_real_knowledge_base_text(alpha_input) -> None:
    naming_input = NamingInput.from_dict(alpha_input)
    structure_result = StructureEngine().select(naming_input)
    archetype_result = ArchetypeEngine().select(structure_result["top_structures"], naming_input)
    retriever = CultureRetriever()
    evidences = retriever.retrieve(
        structure_result["candidate_structures"],
        archetype_result["candidate_archetypes"],
        naming_input.style_preferences,
    )
    all_contents = {record.get("content") for record in CultureIndex().records}

    assert evidences
    assert evidences[0].original_text in all_contents
    assert {item.source_type for item in evidences}.issuperset({"shijing", "chuci", "tang_poetry", "song_ci", "sishuwujing"})
