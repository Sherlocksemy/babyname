# Milestone 3.2A Summary

Generated at: 2026-06-24T10:47:53

## Catalog Counts
- CORE: 1347
- EXTENDED: 4419
- EXPERIMENTAL: 1739
- REJECTED: 600
- CORE+EXTENDED modern-name candidate count: 5766

## Core Questions
1. CORE+EXTENDED currently has 5766 eligible production-pool characters after strict risk filtering.
2. CORE reached its current size because the catalog combines source positivity, commonness, culture evidence, semantic category bonuses, and the new no-risk CORE cap.
3. Extension still introduces some review-worthy combinations; low-nameability and primary-category rules were tightened in this pass.
4. Compared with 3.1B, the old virtue stack is reduced and expanded chars are used, but 3.1B lacks a same-case Top20 matrix.
5. 仁、贤、承、谦、德、信、敬、正、思、安 are no longer allowed to monopolize Top20 by ranking caps.
6. Some generated names still need human review for phrase-like feel; see manual review.
7. Catalog now carries semantic roles and composition validation, but this remains rule-driven rather than fully linguistic.

## Sample Audit
- CORE: sample=200, decisions={'CORRECT': 200}, correct_rate=1.0
- EXTENDED: sample=200, decisions={'CORRECT': 188, 'TOO_HIGH': 12}, correct_rate=0.94
- EXPERIMENTAL: sample=100, decisions={'CORRECT': 84, 'TOO_HIGH': 16}, correct_rate=0.84
- REJECTED: sample=100, decisions={'CORRECT': 100}, correct_rate=1.0

## Core Strictness
{
  "core_total": 1347,
  "no_culture_link_count": 139,
  "polyphonic_count": 0,
  "low_frequency_count": 1294,
  "high_stroke_count": 32,
  "empty_semantic_roles_count": 0,
  "empty_naming_meaning_count": 0,
  "nonempty_risk_count": 0
}

## Five Case Results
- case_a_lin_male_teochew: Top3=林惠诗 / 林仁风 / 林思梦; Backup7=林清嘉 / 林辉泽 / 林静永 / 林诗惠 / 林晨风 / 林辉晏 / 林云静
- case_b_chen_female: Top3=陈诗安 / 陈树清 / 陈秀莹; Backup7=陈阳惠 / 陈美淑 / 陈明嘉 / 陈诗惠 / 陈清嘉 / 陈阳凯
- case_c_huang_male: Top3=黄凯风 / 黄山珍 / 黄云清; Backup7=黄江晏 / 黄海诗 / 黄风诗 / 黄江旭
- case_d_zheng_female: Top3=郑安宗 / 郑怿宁 / 郑怡芬; Backup7=郑安怿 / 郑宁宗 / 郑怡莹
- case_e_ouyang_neutral: Top3=欧阳思晨 / 欧阳深楚 / 欧阳美诗; Backup7=欧阳诗流 / 欧阳思泉 / 欧阳深晨

## Acceptance
- Catalog sample gates passed: True
- CORE required non-empty gates passed: True
- Generation hard gates passed for all cases: False
- Milestone 3.3 was not entered.

See JSON reports for full Top20, Top10, Top3, Backup7, before/after metrics, and manual review tables.
