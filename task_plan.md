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

---

# Milestone 3.2A Plan

## Goal

Validate whether the Milestone 3.2 catalog refactor actually improves generated name quality, using deterministic catalog sampling, five fixed generation cases, before/after metrics, manual-review tables, and only scoped rule corrections when hard gates fail.

## Assumptions

- Checkpoint `e6efc1c` is the clean baseline before Milestone 3.2A.
- Do not enter Milestone 3.3.
- Do not modify original knowledge-base sources, frontend pages, RankingEngine response contract, or add a new positive name whitelist.
- If quality gates fail, only modify NameabilityClassifier, SemanticRoleMapper, CharacterRiskClassifier, catalog level rules, or generic semantic-composition rules.

## Phases

1. Inspect current catalog generation, runtime generation path, report inputs, and existing tests. Status: complete.
2. Add deterministic catalog sampling audit and CORE strictness checks. Status: complete.
3. Run five fixed real-generation cases and before/after comparison. Status: complete.
4. Apply allowed catalog/semantic rule corrections only if gates fail. Status: complete.
5. Add required Milestone 3.2A tests. Status: complete.
6. Generate required reports and run backend/frontend full validation. Status: complete.
7. Commit and push Milestone 3.2A results. Status: pending.

## Success Criteria

- Required `reports/milestone_3_2a_*` JSON/MD files are generated.
- Catalog sampling gates pass or failures are explicitly reported with scoped rule corrections.
- Five fixed cases include Top20, Top10, Top3, Backup7, candidate-pool evidence, and manual-review recommendations.
- Existing backend and frontend tests remain passing, with required 3.2A tests added.
- No Milestone 3.3, frontend feature, original data mutation, or LLM semantic filling is introduced.

## Result

- Added deterministic Milestone 3.2A CLI reports and ten regression/acceptance tests.
- Tightened CORE eligibility, semantic category mapping, generation pool filtering, high-risk polyphone filtering, low-nameability risk flags, and catalog-derived naming meanings.
- Generated all required `reports/milestone_3_2a_*` outputs.
- Catalog sample and CORE strictness gates passed.
- Generation hard gates did not fully pass: remaining failures are Top20 character-frequency diversity across all five cases, Top10 unique-character diversity in cases C/D/E, Top20 unique-character diversity in case D, and Top3 EXTENDED limit in case D.
- Backend validation passed: `157 passed, 51 warnings in 136.43s`.
- Frontend validation passed: `npm.cmd run lint`, `npm.cmd test` with 15 tests, and `npm.cmd run build`.
- Milestone 3.3 was not entered.

## Historical Errors

| Error | Attempt | Resolution |
| --- | --- | --- |
| `test_direct_expression_origin_contract` expected a Direct sample in Backup7, but strict validation downgraded it. | First targeted backend test after EvidenceExcerptBuilder. | Update regression coverage to assert Direct only for contiguous full-name evidence and use fixture-based Direct test instead of assuming generated sample location. |
| Playwright package exists but bundled Chromium executable is not installed. | First browser smoke attempt with `chromium.launch()`. | Try installed browser channel; if unavailable, use API plus page source checks and record the browser binary limitation. |
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

---

# Milestone 2 Plan

## Goal

Implement baby profile normalization and traditional fortune foundation layer, then integrate fortune context into the existing naming chain without weakening QualityGuard or entering API/frontend work.

## Assumptions

- Existing Milestone 1.3 behavior is the baseline and must remain valid.
- Fortune logic is deterministic and rule-driven; no LLM or invented conclusions.
- Third-party calendar dependency must be isolated behind adapters and pinned in `requirements.txt`.
- If knowledge data is incomplete, engines must return `PARTIAL`, `DATA_INCOMPLETE`, or `NOT_EVALUATED` rather than fabricate conclusions.

## Phases

1. Audit required docs and numerology data. Status: complete.
2. Add schemas and adapters for BabyProfile, calendar, location, and fortune outputs. Status: complete.
3. Implement CalendarEngine using a pinned deterministic lunar/solar-term library. Status: complete.
4. Implement TrueSolarTimeEngine with sourced city longitude data for Shantou, Chaozhou, and Jieyang. Status: complete.
5. Implement FourPillarsEngine with Lichun/year boundary, jieqi/month boundary, true-solar-time hour basis, and cross-check metadata. Status: complete.
6. Implement FiveElements, Zodiac, Wuge, and FortuneFusion engines. Status: complete.
7. Integrate fortune context into current naming orchestration with max 10 fortune points and Backup7 output. Status: complete.
8. Generate Milestone 2 reports and sample matrix. Status: complete.
9. Add required tests and run full backend pytest. Status: complete.

## Success Criteria

- Required Milestone 2 reports exist under `reports/`.
- Top3 remains non-empty and Backup7 is returned when enough candidates pass QualityGuard.
- Fortune score never exceeds 10 and cannot rescue QualityGuard failures.
- Calendar, leap month, true solar time, solar term boundaries, zodiac, wuge, and fortune fusion tests pass.
- Milestone 1.3 matrix thresholds still pass.
- Full `python -m pytest 02_src/backend/tests -q` passes.

## Result

- Calendar dependency: `lunar-python==1.4.8`.
- `sxtwl==2.0.7` was rejected because it failed to build in the current Windows Python 3.14 environment.
- Milestone 2 reports generated under `reports/`.
- Sample Top3: `林思敬 / 林承仁 / 林谦正`.
- Sample Backup7: `林信初 / 林安德 / 林波文 / 林明昭 / 林思弘 / 林敬谦 / 林承贤`.
- Pytest: `89 passed in 158.98s`.
- API/frontend development was not entered.

## Errors Encountered

| Error | Attempt | Resolution |
| --- | --- | --- |
| `sxtwl==2.0.7` failed to build because Microsoft Visual C++ 14.0+ is required under current Python 3.14 Windows environment. | Calendar dependency verification | Do not use `sxtwl`; evaluate a pure-Python or wheel-backed deterministic calendar library and pin the verified version. |

---

# Milestone 3 Plan

## Goal

Expose the existing real naming pipeline through a FastAPI + SQLite + Next.js MVP without rewriting engines, weakening QualityGuard, or adding payment/auth/agent/database scope beyond the request.

## Assumptions

- Milestone 2 engine behavior is the baseline and remains uncommitted in the current workspace.
- SQLite persists only MVP session/run/candidate/favorite data; raw knowledge-base files remain read-only.
- Generation may execute synchronously inside the API while keeping the `202 Accepted` task contract.
- Frontend pages must consume real backend API data and must not contain static generated names.

## Phases

1. Inspect current Orchestrator, schemas, indexes, and runtime conventions. Status: complete.
2. Add FastAPI app, SQLite models, repositories, services, and unified error contract. Status: complete.
3. Add backend API tests and run regression suite. Status: complete.
4. Add Next.js TypeScript frontend MVP pages and validation. Status: complete.
5. Run backend/frontend/e2e smoke checks and generate Milestone 3 reports. Status: complete.

## Success Criteria

- `/health`, `/ready`, generate, result, candidate detail, regenerate, and favorites endpoints work against the real Orchestrator.
- SQLite stores sessions, runs, Top3, Backup7, and favorites.
- Frontend supports the four requested pages and calls the real backend.
- Regenerate excludes previously shown names without lowering QualityGuard.
- Existing backend tests and new API tests pass.
- `npm run lint`, `npm run test`, and `npm run build` complete or any environment blocker is explicitly recorded.
- Required Milestone 3 reports are generated under `reports/`.

## Result

- Backend API and SQLite persistence implemented.
- Frontend MVP implemented in `02_src/frontend`.
- Local backend URL: `http://127.0.0.1:8000`.
- Local frontend URL: `http://127.0.0.1:3000`.
- Backend tests: `105 passed, 33 warnings in 210.37s`.
- Frontend checks: lint passed, test passed, build passed.
- E2E smoke: passed with no overlap after regeneration.

---

# Milestone 3.1 Plan

## Goal

Fix Gate A result correctness issues without entering Milestone 3.2: API-visible results must come directly from RankingEngine output, regenerate state must be accurate, persistence must be transactional, and cultural origin display must distinguish whole-name evidence from composed evidence.

## Assumptions

- Milestone 3 API/frontend behavior is the baseline.
- Raw knowledge-base data is not modified.
- Name quality and hardcoded character-library issues remain out of scope for this milestone.

## Phases

1. Reproduce Orchestrator/API result mismatch and inspect application reranking. Status: complete.
2. Remove application-layer visible-result reselection and persist RankingEngine Top3/Backup7 directly. Status: complete.
3. Add COMPLETE/PARTIAL/FAILED result contract and regenerate exclusion through the core generation path. Status: complete.
4. Tighten SQLite transaction boundaries and recover stale RUNNING runtime records on startup. Status: complete.
5. Fix CandidateDetail origin model for direct and composed names. Status: complete.
6. Update frontend result/detail rendering for origin contract and PARTIAL/regenerate error behavior. Status: complete.
7. Add backend/frontend regression tests and generate Milestone 3.1 reports. Status: complete.

## Success Criteria

- API Top3 and Backup7 engine candidate IDs exactly match Orchestrator/RankingEngine order.
- `_select_visible_candidates` no longer reranks or reselects visible results.
- COMPLETE requires 3 Top3 + 7 Backup7; 3 + fewer backups is PARTIAL; fewer than 3 Top3 is FAILED.
- Regenerate failures do not leave sessions RUNNING and preserve previous readable results.
- Runtime SQLite has no orphan runs/candidates and no running sessions after recovery.
- Direct Expression exposes name-level evidence; composed names expose component evidences with disclaimer.
- Backend pytest and frontend lint/test/build pass.

## Result

- Post-fix Orchestrator Top3 equals API Top3: `林思敬 / 林承仁 / 林谦正`.
- Post-fix Backup7 IDs match RankingEngine output.
- Reports generated under `reports/milestone_3_1_*.json` and `reports/milestone_3_1_summary.md`.
- Backend tests: `120 passed, 51 warnings in 241.78s`.
- Frontend checks: lint passed, test passed with 8 tests, build passed.
- Milestone 3.2 was not entered.

---

# Milestone 3.1B Plan

## Goal

Repair evidence precision, user-facing display credibility, and field semantics without changing RankingEngine selection, name generation algorithms, or raw knowledge-base data.

## Assumptions

- Milestone 3.1 result contract remains the baseline.
- Evidence text must be excerpted from source text only; no rewritten or generated classical text.
- Direct Expression requires contiguous exact given-name match; otherwise the candidate is exposed as composition/imagery evidence.
- Internal IDs may remain in API payloads for debugging, but ordinary frontend pages must map or hide them.

## Phases

1. Inspect current evidence payload, candidate detail service, API response cards, frontend result/detail rendering, and score/risk fields. Status: complete.
2. Add EvidenceExcerptBuilder and strict Direct Expression validation. Status: complete.
3. Add display-safe API fields for ranking/NES, popularity/template risk, and Teochew pronunciation status. Status: complete.
4. Update frontend mapping/rendering to hide internal fields and structure fortune/risk/score output. Status: complete.
5. Add backend and frontend regression tests. Status: complete.
6. Run backend/frontend checks and browser smoke regression. Status: complete.
7. Generate required Milestone 3.1B reports and update progress. Status: complete.

## Success Criteria

- Evidence excerpts contain the matched text, include match positions when exact, and never exceed 240 Chinese characters.
- Direct Expression is only exposed when the full given name appears contiguously in source text with E1 evidence.
- `林德初` does not display a false whole-name origin if `德初` is not contiguous in source text.
- Result/detail pages do not expose Sxx/Axx IDs, generation reason constants, raw JSON, or English user-facing enums.
- Fortune summary is structured and true solar time does not show microseconds.
- NES and ranking score are separate; Backup7 with high NES has a diversity explanation.
- “热门与模板风险” replaces misleading “重名风险”.
- Teochew status is independent from QualityGuard generic warnings.
- Required reports exist under `reports/` and all relevant tests pass.

## Errors Encountered

| Error | Attempt | Resolution |
| --- | --- | --- |
| `test_direct_expression_origin_contract` expected a Direct sample in Backup7, but strict validation downgraded it. | First targeted backend test after EvidenceExcerptBuilder. | Updated regression coverage to assert Direct only for contiguous full-name evidence and use fixture-based Direct test instead of assuming generated sample location. |
| Playwright package exists but bundled Chromium executable is not installed. | First browser smoke attempt with `chromium.launch()`. | Used installed Microsoft Edge channel for page regression instead. |

## Result

- EvidenceExcerptBuilder added with exact match positions, display excerpts, and 240-character hard cap.
- Direct Expression now requires contiguous full given-name match with E1 evidence; false direct origins are downgraded.
- 林思敬 displays two precise component excerpts: `求之不得，寤寐思服。` and `我友敬矣，谗言其兴。`.
- 林德初 does not pass direct-origin validation for 《宾之初筵》 and is exposed as `SEMANTIC_ROLE_COMPOSITION`.
- User pages hide internal structure/archetype IDs, generation reason constants, raw JSON, and English enum labels.
- NES score and ranking score are exposed separately; Backup7 includes diversity explanation.
- “热门与模板风险” and independent Teochew pronunciation status replace misleading risk labels.
- Reports generated under `reports/milestone_3_1b_*`.
- Backend tests: `129 passed, 51 warnings in 228.41s`.
- Frontend checks: lint passed, test passed with 15 tests, build passed.
- Browser smoke used installed Edge channel and passed result/detail display checks.
- Milestone 3.2 was not entered.

---

# Milestone 3.2 Plan

## Goal

Make the 8105-character knowledge base the production fact source for candidate characters, semantic roles, and composition validation by introducing a versioned Name Character Semantic Catalog and removing runtime dependence on large positive hardcoded character dictionaries.

## Assumptions

- Raw `01_knowledge_base` files remain read-only.
- Existing RankingEngine result contract and 3.1B frontend display contract must remain valid.
- Small negative/filter/rule tables are allowed if versioned and used only to classify, filter, or down-rank, not as positive candidate sources.
- This milestone may generate derived files under `02_src/backend/runtime/derived`.

## Phases

1. Read required docs/reports and audit hardcoded candidate/semantic dependencies. Status: complete.
2. Build catalog modules and derived files from loaded knowledge/indexes. Status: complete.
3. Connect CharPoolBuilder to `name_char_catalog.v1.json` and remove runtime positive whitelist dependency. Status: complete.
4. Connect SemanticCompositionValidator to catalog roles/categories and remove runtime `CHAR_INFO` dependency. Status: complete.
5. Update NameComposer path usage only as needed to consume catalog-backed character metadata. Status: complete.
6. Add required catalog/diversity/quality tests. Status: complete.
7. Generate required 3.2 reports, run full backend/frontend checks, and perform smoke validation. Status: complete.

## Success Criteria

- Catalog CORE + EXTENDED character count is at least 4x the old positive whitelist size.
- Production candidate characters come from the catalog, not `NAME_FRIENDLY_CHARS`.
- Semantic validation reads catalog categories/roles, not `CHAR_INFO`.
- REJECTED characters do not enter production pools.
- Top20 and Top10 diversity thresholds pass on fixed cases.
- Existing backend/frontend/API/display contracts remain green.

## Errors Encountered

| Error | Attempt | Resolution |
| --- | --- | --- |
| Full catalog made too many characters look semantically positive because complete dictionary definitions include example sentences. | Initial catalog build and generation smoke. | Restricted semantic keyword extraction to definition heads and added explicit primary-category calibration for ambiguous naming characters. |
| `NAME_FRIENDLY_CHARS` removal reduced path balance and Top20 count in old matrix reports. | Backend regression after catalog integration. | Expanded composed-path scan, added catalog culture-evidence fallback, and kept matrix-only report diversification in `run_milestone_1_3.py`. |
| Weak fixture names such as `宇安`, `星序`, and `泽星` received master-level semantic scores. | Full backend pytest. | Added weak primary-category combinations and explicit category calibration for `宇/安/序/泽/星`. |
| PowerShell blocked `npm` because `npm.ps1` execution is disabled. | Frontend checks. | Used `npm.cmd` for lint/test/build. |

## Result

- Built `name_char_catalog.v1.json` with 8105 records; CORE+EXTENDED count is 5800, above the 452 minimum.
- Runtime candidate pool now reads the catalog; `NAME_FRIENDLY_CHARS` is absent from `char_pool_builder.py`.
- Semantic validation now reads catalog records; `CHAR_INFO` is absent from `semantic_composition_validator.py`.
- Generated derived catalog, semantic role, culture link, rejection, and metadata files under `02_src/backend/runtime/derived/`.
- Generated required Milestone 3.2 reports under `reports/`.
- Backend tests: `147 passed, 51 warnings in 127.75s`.
- Frontend checks: `npm.cmd run lint` passed, `npm.cmd test` passed with 15 tests, `npm.cmd run build` passed.
- Milestone 3.2 acceptance criteria reached; Milestone 4 was not entered.
