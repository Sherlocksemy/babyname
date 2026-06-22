from __future__ import annotations

import json
import sys

from app.core.knowledge_audit import KnowledgeAudit


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    audit = KnowledgeAudit()
    report = audit.audit()
    json_path, md_path = audit.write_reports(report)
    summary = {
        "overall_status": report["overall_status"],
        "dataset_count": len(report["datasets"]),
        "report_json": str(json_path),
        "report_md": str(md_path),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["overall_status"] in {"ok", "warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
