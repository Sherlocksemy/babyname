# Milestone 3.1B Summary

Generated at: 2026-06-23T17:57:39

## Scope
Gate B for evidence precision and trusted user display only. RankingEngine, name generation, and raw knowledge base were not modified. Milestone 3.2 was not entered.

## Evidence Precision
- Sample: 林思敬
- 林思敬 component excerpts: 求之不得，寤寐思服。 / 我友敬矣，谗言其兴。
- Excerpt hard limit: <= 240 Chinese characters.
- Direct Expression now requires exact contiguous full given-name match with E1 evidence.

## Direct Origin Validation
- 林德初 contiguous match in 《诗经·宾之初筵》: False
- 林德初 final origin_mode: SEMANTIC_ROLE_COMPOSITION
- Downgraded false Direct Expression count in sample run: 3

## Display Contract
- Internal IDs and reason constants are hidden from ordinary pages.
- Gender/calendar/status enums are mapped to Chinese.
- Fortune summary is structured; true solar time is displayed to minute precision.
- Detail page no longer renders raw JSON blocks.

## Score and Risk Display
- NES and ranking score are returned separately.
- Backup7 cards include diversity explanation when applicable.
- “热门与模板风险” replaces misleading duplicate-name wording.
- Teochew pronunciation uses independent status/limitations and no longer derives NOTICE from generic QualityGuard warnings.

## Page Regression
- Browser: msedge via Playwright channel.
- Result/detail checks: {'browser': 'msedge via Playwright channel', 'request_id': 'req_b87102ecf3a2427091f566ad5ee9b4bc', 'resultNoRawJson': True, 'resultNoInternalIds': True, 'resultNoEnglishEnums': True, 'resultHasChineseRisk': True, 'resultHasStructuredFourPillars': True, 'resultNoMicroseconds': True, 'detailNoRawJson': True, 'detailNoInternalIds': True, 'detailHasTwoExcerpts': True, 'detailTeochewHonest': True, 'detailPopularity': True}

## Tests
- Backend: 129 passed, 51 warnings in 228.41s.
- Frontend lint: passed.
- Frontend test: 15 passed.
- Frontend build: passed.

## Acceptance
Milestone 3.1B acceptance criteria are met. Do not proceed to Milestone 3.2 without explicit confirmation.
