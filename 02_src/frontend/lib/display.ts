export const ENUM_LABELS: Record<string, string> = {
  male: "男",
  female: "女",
  neutral: "中性",
  unknown: "未说明",
  solar: "公历",
  lunar: "农历",
  COMPLETE: "计算完成",
  COMPLETED: "计算完成",
  PARTIAL: "部分完成",
  FAILED: "未完成",
  NOT_EVALUATED: "暂未评估",
  DATA_INCOMPLETE: "数据尚不完整",
  LOW: "低",
  MEDIUM: "中",
  HIGH: "高",
  UNKNOWN: "暂无法评估",
  SAFE: "未见明显风险",
  NOTICE: "需留意"
};

export function enumLabel(value: unknown): string {
  const key = String(value || "");
  return ENUM_LABELS[key] || key || "未评估";
}

export function formatScore(value: unknown): string {
  const number = Number(value);
  if (!Number.isFinite(number)) return "未评估";
  return number.toFixed(1);
}

export function displayScore(item: any): { grade: string; ranking: string; nes: string } {
  const score = item?.display_score || item?.recommendation?.display_score || {};
  const nes = score.nes_score ?? item?.nes_score ?? item?.score ?? item?.recommendation?.score;
  return {
    grade: score.grade || (Number(nes) >= 90 ? "卓越" : Number(nes) >= 85 ? "优秀" : "良好"),
    ranking: formatScore(score.ranking_score ?? item?.ranking_score ?? nes),
    nes: formatScore(nes)
  };
}

export function structureLabel(item: any): string {
  return item?.structure_label || item?.structure?.label || "未归类";
}

export function archetypeLabel(item: any): string {
  return item?.archetype_label || item?.archetype?.label || "未归类";
}

export function originModeLabel(origin: any): string {
  if (!origin) return "文化依据待补充";
  if (origin.mode === "DIRECT_EXPRESSION") return "整体出处";
  if (origin.mode === "SEMANTIC_ROLE_COMPOSITION") return "双字文化组合推导";
  if (origin.mode === "IMAGERY_TRANSFORMATION") return "意象转化推导";
  return origin.display_label || "文化推导";
}

export function formatTrueSolarTime(value: unknown): string {
  const text = String(value || "");
  const match = text.match(/^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})(?::\d{2})?/);
  return match ? `${match[1]} ${match[2]}` : text || "未计算";
}

export function fourPillarRows(four: any): Array<[string, string]> {
  if (!four) return [];
  return [
    ["年柱", four.year_pillar?.text],
    ["月柱", four.month_pillar?.text],
    ["日柱", four.day_pillar?.text],
    ["时柱", four.hour_pillar?.text],
    ["日主", four.day_master]
  ].filter(([, value]) => Boolean(value)) as Array<[string, string]>;
}

export function cleanList(items: unknown): string[] {
  if (!Array.isArray(items)) return [];
  return items.map((item) => String(item || "").trim()).filter(Boolean);
}

export function riskLabel(risk: any): string {
  return risk?.label || enumLabel(risk?.level);
}

export function teochewSummary(teochew: any): string {
  const limitations = cleanList(teochew?.limitations);
  return limitations.length ? limitations.join("；") : "潮汕单字读音：暂未查询；姓名连读及变调风险：暂未完整评估";
}
