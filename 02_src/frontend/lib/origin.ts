export function originSummaryText(origin: any): string {
  if (!origin) return "出处：未标注";
  if (origin.mode === "DIRECT_EXPRESSION") return origin.display_label || "整体出处";
  const components = (origin.component_evidences || []).map((item: any) => `${item.char}：${[item.book, item.title].filter(Boolean).join(" / ") || "有单字依据"}${item.display_excerpt ? ` “${item.display_excerpt}”` : ""}`);
  return `生成方式：双字文化组合推导 ${components.join("；")}`.trim();
}

export function partialResultMessage(result: any): string | null {
  if (result?.result_status !== "INSUFFICIENT_QUALIFIED_CANDIDATES") return null;
  const count = result?.counts?.qualified ?? (result?.top3?.length || 0) + (result?.backup7?.length || 0);
  return `本轮仅筛选出${count}个符合质量标准的名字，系统没有为了凑数降低筛选门槛。`;
}

export function shouldPreservePreviousResultOnRegenerateError(currentResult: any, error: string): boolean {
  return Boolean(currentResult && error);
}
