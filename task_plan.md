# Data Quality Audit Plan

## Goal

Audit and repair generated knowledge-base outputs under `01_knowledge_base` and extractor scripts under `03_tools`, with special focus on missing fields such as `radical` in `tongyong_guifan_hanzi.csv`.

## Phases

1. Inventory generated outputs and quantify missing rates. Status: complete.
2. Trace high-impact missing fields back to raw sources and extractor logic. Status: complete.
3. Patch extractor scripts and validation checks. Status: complete.
4. Rebuild all outputs and verify improved quality. Status: complete.
5. Summarize remaining source-data limitations. Status: complete.

## Success Criteria

- Compliance CSV has 8105 unique whitelist characters.
- Key fields have explicit missing-count reports.
- `radical` and modern stroke coverage are improved using available raw sources.
- `validate_outputs.py` catches unacceptable emptiness and high-impact missing data.
- README files remain honest about inferred or unavailable fields.

## Errors Encountered

| Error | Attempt | Resolution |
| --- | --- | --- |
| `python .\03_tools\build_all.py` timed out after 304 seconds | First rebuild after adding Unihan | Optimize Unihan radical simplification to avoid repeated OpenCC initialization, then rerun in steps. |
| `PermissionError` writing `teochew_pronunciation.csv` | Full rebuild after core fix | Retry pronunciation script; likely file lock by another Windows process if repeated. |

---

# Milestone 1.3 Plan

## Goal

Implement Milestone 1.3 personalization and cross-case de-homogenization without entering Milestone 2. Keep changes scoped to deterministic name generation/ranking quality, reports, and tests.

## Assumptions

- Existing Milestone 1.2 code and reports are the baseline.
- No original knowledge-base files are modified.
- No LLM, API, frontend, database, fortune engines, or agent framework is added.

## Phases

1. Inspect current generation, quality guard, scoring, ranking, and reconstruction behavior. Status: complete.
2. Add deterministic profile specificity and surname fit into candidate evaluation. Status: complete.
3. Extend candidate generation with direct, semantic-role composition, and imagery transformation paths. Status: complete.
4. Update ranking to enforce profile thresholds and generation-path diversity. Status: complete.
5. Generate Milestone 1.3 matrices and overlap reports. Status: complete.
6. Add requested regression tests. Status: complete.
7. Run CLI matrix/report generation and full pytest. Status: complete.

## Success Criteria

- Matrix A: 15 Top3 slots contain at least 12 unique given names, unique rate >= 80%, each given name appears <= 2, pairwise Top3 overlap <= 1, pairwise Top20 given-name Jaccard <= 0.25.
- Matrix B: no pair has identical Top3, at least 60% Top1 names differ, same given name has surname-fit variation across surnames.
- Each Top20 has Direct Expression <= 50%, Semantic Role Composition >= 30%, Imagery Transformation >= 15%, unless explicitly reported as insufficient.
- Reports required by the task are generated under `reports/`.
- Existing and newly added backend tests pass.

## Result

- Matrix A threshold: passed.
- Matrix B threshold: passed.
- Pytest: `65 passed in 136.48s`.
- Milestone 2 was not entered.
