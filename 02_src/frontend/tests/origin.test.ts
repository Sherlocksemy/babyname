import assert from "node:assert/strict";
import { test } from "node:test";

import { originSummaryText, partialResultMessage, shouldPreservePreviousResultOnRegenerateError } from "../lib/origin";

test("direct expression origin displays name-level source", () => {
  const text = originSummaryText({ mode: "DIRECT_EXPRESSION", display_label: "整体出处：诗经 / 巧言" });
  assert.equal(text, "整体出处：诗经 / 巧言");
});

test("composed origin displays component evidences", () => {
  const text = originSummaryText({
    mode: "SEMANTIC_ROLE_COMPOSITION",
    component_evidences: [
      { char: "思", book: "诗经", title: "关雎" },
      { char: "敬", book: "诗经", title: "沔水" }
    ]
  });
  assert.equal(text.includes("生成方式：双字文化组合推导"), true);
  assert.equal(text.includes("思：诗经 / 关雎"), true);
  assert.equal(text.includes("敬：诗经 / 沔水"), true);
});

test("partial result message names the actual qualified count", () => {
  assert.equal(
    partialResultMessage({ result_status: "INSUFFICIENT_QUALIFIED_CANDIDATES", counts: { qualified: 8 } }),
    "本轮仅筛选出8个符合质量标准的名字，系统没有为了凑数降低筛选门槛。"
  );
});

test("regenerate error preserves previous rendered result", () => {
  assert.equal(shouldPreservePreviousResultOnRegenerateError({ top3: [1] }, "换一批失败"), true);
});
