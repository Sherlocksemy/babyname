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
