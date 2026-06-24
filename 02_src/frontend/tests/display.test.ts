import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import { enumLabel, formatScore, formatTrueSolarTime, fourPillarRows, originModeLabel, teochewSummary } from "../lib/display";

test("gender calendar and status enums display in Chinese", () => {
  assert.equal(enumLabel("male"), "男");
  assert.equal(enumLabel("solar"), "公历");
  assert.equal(enumLabel("COMPLETE"), "计算完成");
  assert.equal(enumLabel("DATA_INCOMPLETE"), "数据尚不完整");
});

test("four pillars and true solar time are structured without microseconds", () => {
  const rows = fourPillarRows({
    year_pillar: { text: "乙巳" },
    month_pillar: { text: "戊寅" },
    day_pillar: { text: "己巳" },
    hour_pillar: { text: "戊辰" },
    day_master: "己"
  });
  assert.deepEqual(rows[0], ["年柱", "乙巳"]);
  assert.equal(formatTrueSolarTime("2025-03-01 08:03:41.084871"), "2025-03-01 08:03");
});

test("score format keeps one decimal", () => {
  assert.equal(formatScore(94.04), "94.0");
  assert.equal(formatScore(92.37), "92.4");
});

test("teochew incomplete evaluation does not display NOTICE", () => {
  const text = teochewSummary({ risk_level: "UNKNOWN", limitations: ["潮汕单字读音：已查询", "姓名连读及变调风险：暂未完整评估"] });
  assert.equal(text.includes("NOTICE"), false);
  assert.equal(text.includes("暂未完整评估"), true);
});

test("origin mode is mapped to trusted Chinese display label", () => {
  assert.equal(originModeLabel({ mode: "SEMANTIC_ROLE_COMPOSITION" }), "双字文化组合推导");
});

test("result page source hides old internal user-facing labels", () => {
  const source = readFileSync("app/results/[requestId]/page.tsx", "utf8");
  assert.equal(source.includes("Structure："), false);
  assert.equal(source.includes("Archetype："), false);
  assert.equal(source.includes("重名风险"), false);
  assert.equal(source.includes("JSON.stringify"), false);
});

test("detail page source does not render raw json blocks", () => {
  const source = readFileSync("app/results/[requestId]/[candidateId]/page.tsx", "utf8");
  assert.equal(source.includes("<pre>"), false);
  assert.equal(source.includes("JSON.stringify"), false);
  assert.equal(source.includes("Structure："), false);
  assert.equal(source.includes("Archetype："), false);
});
