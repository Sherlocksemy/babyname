# Milestone 3.1 Summary

Generated at: 2026-06-23T17:00:51

## Scope
Gate A only: result correctness, regenerate state contract, transaction integrity, and trustworthy cultural origin display. Milestone 3.2 was not entered.

## Key Validation
- Post-fix Orchestrator Top3: 林思敬, 林承仁, 林谦正
- Post-fix API Top3: 林思敬, 林承仁, 林谦正
- Top3 engine IDs match: True
- Backup7 engine IDs match: True
- API status/result_status: COMPLETED / COMPLETE
- Counts: {'top3': 3, 'backup': 7, 'qualified': 10, 'required': 10}
- _select_visible_candidates is disabled and raises if called.

## Regenerate and State
- Three regenerate attempts recorded in reports/milestone_3_1_regenerate_validation.json.
- Partial shortage simulation: HTTP 202, status=PARTIAL, result_status=INSUFFICIENT_QUALIFIED_CANDIDATES, counts={'top3': 3, 'backup': 5, 'qualified': 8, 'required': 10}
- Failed regenerate simulation: HTTP 500, previous_result_preserved=True, session_status=COMPLETED

## Cultural Origin
- Direct Expression sample validated: True
- Composed sample validated: True
- Frontend result/detail pages render origin.mode and do not promote the first component evidence to whole-name source.

## Database Integrity
- Stale RUNNING recovery is implemented in 02_src/backend/app/db/init_db.py.
- SQLite foreign keys enabled: True
- Integrity report: {'orphan_runs': 0, 'orphan_candidates': 0, 'empty_completed_runs': 0, 'running_sessions': 0}

## Added Files
- 02_src/backend/tests/test_api_top3_matches_ranking.py
- 02_src/backend/tests/test_api_backup7_matches_ranking.py
- 02_src/backend/tests/test_no_application_layer_reranking.py
- 02_src/backend/tests/test_complete_result_requires_3_plus_7.py
- 02_src/backend/tests/test_partial_result_contract.py
- 02_src/backend/tests/test_regenerate_failed_run_state.py
- 02_src/backend/tests/test_regenerate_session_not_stuck_running.py
- 02_src/backend/tests/test_regenerate_preserves_previous_success.py
- 02_src/backend/tests/test_generation_transaction_rollback.py
- 02_src/backend/tests/test_no_orphan_candidates.py
- 02_src/backend/tests/test_direct_expression_origin_contract.py
- 02_src/backend/tests/test_composed_origin_contract.py
- 02_src/backend/tests/test_composed_name_returns_two_evidences.py
- 02_src/backend/tests/test_candidate_detail_does_not_use_first_evidence_as_name_origin.py
- 02_src/frontend/lib/origin.ts
- 02_src/frontend/tests/origin.test.ts
- reports/milestone_3_1_result_contract.json
- reports/milestone_3_1_origin_contract.json
- reports/milestone_3_1_regenerate_validation.json
- reports/milestone_3_1_database_integrity.json
- reports/milestone_3_1_summary.md

## Modified Files
- 02_src/backend/app/services/naming_application_service.py
- 02_src/backend/app/services/candidate_detail_service.py
- 02_src/backend/app/repositories/naming_repository.py
- 02_src/backend/app/db/init_db.py
- 02_src/backend/app/db/models.py
- 02_src/backend/app/db/session.py
- 02_src/backend/app/schemas/naming_input.py
- 02_src/backend/app/schemas/baby_profile.py
- 02_src/backend/app/engines/name_composer.py
- 02_src/backend/tests/test_result_api.py
- 02_src/backend/tests/test_candidate_detail_api.py
- 02_src/backend/tests/test_sqlite_persistence.py
- 02_src/frontend/app/results/[requestId]/page.tsx
- 02_src/frontend/app/results/[requestId]/[candidateId]/page.tsx

## Deleted Files
- None

## Tests
- Backend: 120 passed, 51 warnings in 241.78s
- Frontend lint: passed
- Frontend test: 8 passed
- Frontend build: passed

## Acceptance
Milestone 3.1 Gate A acceptance criteria are met. Do not proceed to Milestone 3.2 without explicit confirmation.
