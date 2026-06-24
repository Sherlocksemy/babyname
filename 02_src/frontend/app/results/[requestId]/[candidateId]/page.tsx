"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { createFavorite, getCandidateDetail } from "../../../../lib/api";
import { archetypeLabel, cleanList, displayScore, enumLabel, formatScore, originModeLabel, riskLabel, structureLabel, teochewSummary } from "../../../../lib/display";

export default function CandidateDetailPage() {
  const params = useParams<{ requestId: string; candidateId: string }>();
  const [detail, setDetail] = useState<any>(null);
  const [error, setError] = useState("");
  const [favorited, setFavorited] = useState(false);

  useEffect(() => {
    getCandidateDetail(params.requestId, params.candidateId)
      .then(setDetail)
      .catch((err) => setError(err instanceof Error ? err.message : "详情读取失败"));
  }, [params.requestId, params.candidateId]);

  async function favorite() {
    await createFavorite(params.requestId, params.candidateId);
    setFavorited(true);
  }

  if (error) return <main className="shell"><section className="panel field-error">{error}</section></main>;
  if (!detail) return <main className="shell"><section className="panel">读取详情中</section></main>;

  const score = displayScore(detail);

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <h1>{detail.name.full_name}</h1>
          <span>{detail.name.pinyin || "读音待补充"}</span>
        </div>
        <div className="actions">
          <button className="button secondary" type="button" disabled={favorited} onClick={favorite}>
            {favorited ? "已收藏" : "收藏"}
          </button>
          <Link className="button subtle" href={`/results/${params.requestId}`}>
            返回结果
          </Link>
        </div>
      </header>

      <div className="stack" style={{ maxWidth: 980, margin: "0 auto" }}>
        <Section title="推荐结论">
          <p className="name">{detail.name.full_name}</p>
          <p className="score">综合推荐：{score.grade}</p>
          <p>推荐指数：{score.ranking}；基础质量：{score.nes}</p>
          <p>{detail.recommendation.summary}</p>
        </Section>

        <Section title="姓名整体气质">
          <p>{detail.recommendation.summary}</p>
        </Section>

        <Section title="姓名结构">
          <p>姓名结构：{structureLabel(detail)}</p>
          <p>语义结构：{detail.structure.semantic_pattern || "未标注"}</p>
          <p>适配程度：{enumLabel(detail.structure.compatibility_level)}</p>
        </Section>

        <Section title="人格方向">
          <p>{archetypeLabel(detail)}</p>
          <List items={detail.archetype.profile_fit_reasons} fallback="暂无额外说明" />
        </Section>

        <Section title="生成方式">
          <p>{originModeLabel(detail.origin)}</p>
          <p>{detail.origin?.composition_reason || "基于文化证据、字义和姓名结构综合推导。"}</p>
        </Section>

        <Section title="字义与组合义">
          <p>{detail.meaning.combined_meaning || detail.recommendation.summary}</p>
          <div className="summary-grid">
            {(detail.meaning.chars || []).map((item: any) => (
              <CharMeaning key={item.char} item={item} />
            ))}
          </div>
        </Section>

        <Section title="文化出处">
          <OriginDetail origin={detail.origin} />
        </Section>

        <Section title="普通话读音">
          <ReadingList groups={detail.pronunciation.mandarin} empty="普通话读音待补充" />
        </Section>

        <Section title="潮汕话读音和能力限制">
          <p>{teochewSummary(detail.pronunciation.teochew_pronunciation)}</p>
          <ReadingList groups={detail.pronunciation.teochew} empty="潮汕单字读音待补充" />
        </Section>

        <Section title="命理基础参考">
          <p>五行适配状态：{enumLabel(detail.fortune.five_elements.status)}</p>
          <p>建议元素：{(detail.fortune.five_elements.recommended_elements || []).join("、") || "未评估"}</p>
          <p>候选字五行：{(detail.fortune.five_elements.char_elements || []).join("、") || "未标注"}</p>
          <p>生肖：{detail.fortune.zodiac?.zodiac || detail.fortune.zodiac?.folk_zodiac || "未评估"}</p>
        </Section>

        <Section title="五格计算值">
          <WugeSummary wuge={detail.fortune.wuge} />
        </Section>

        <Section title="评分分项">
          <p>基础质量：{formatScore(detail.scores.nes_total)}</p>
          <p>综合排序：{formatScore(detail.scores.ranking_score)}</p>
          <List items={detail.scores.selection_reasons} fallback="排序说明待补充" />
          <List items={detail.scores.diversity_reasons} fallback="" />
          <ScoreBreakdown breakdown={detail.scores.breakdown} />
        </Section>

        <Section title="热门与模板风险">
          <p>{riskLabel(detail.scores.popularity_template_risk)}</p>
          <List items={detail.scores.popularity_template_risk?.reasons} fallback="暂无法评估真实全国重名情况。" />
        </Section>

        <Section title="限制和免责声明">
          <List items={detail.limitations} fallback="暂无额外限制说明" />
          <p>{detail.disclaimer}</p>
        </Section>
      </div>
    </main>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function CharMeaning({ item }: { item: any }) {
  const semantic = item.semantic || {};
  const kangxi = item.kangxi || {};
  const base = item.base || {};
  return (
    <div className="card">
      <h3>{item.char}</h3>
      <p>现代常用义：{semantic.definition || "未标注"}</p>
      <p>古典含义：{semantic.ancient_meaning || "未标注"}</p>
      <p>命名语义：{semantic.definition || "需结合语境判断"}</p>
      <p>五行：{kangxi.element || "未标注"}</p>
      <p>康熙笔画：{kangxi.kangxi_strokes || "未标注"}</p>
      <p>普通话拼音：{base.pinyin_main || "未标注"}</p>
    </div>
  );
}

function OriginDetail({ origin }: { origin: any }) {
  if (!origin) return <p>未标注</p>;
  if (origin.mode === "DIRECT_EXPRESSION") {
    const evidence = origin.name_level_evidence || {};
    return (
      <div className="stack">
        <p>{origin.display_label}</p>
        <p>“{evidence.display_excerpt || evidence.matched_text || "摘录待补充"}”</p>
        <p className="small">命中：{evidence.matched_text || "未标注"}；来源：{evidence.book || "未标注"} / {evidence.title || "无篇名"} / {evidence.author || "无作者"}</p>
      </div>
    );
  }
  return (
    <div className="stack">
      <p>{origin.display_label}</p>
      {(origin.component_evidences || []).map((item: any) => (
        <div className="card" key={`${item.position}-${item.char}`}>
          <h3>{item.char}字出处</h3>
          <p>“{item.display_excerpt || item.matched_text || "摘录待补充"}”</p>
          <p className="small">命中：{item.matched_text || item.char}；来源：{item.book || "未标注"} / {item.title || "无篇名"} / {item.author || "无作者"}</p>
        </div>
      ))}
      <p>{origin.composition_reason}</p>
      <p className="small">{origin.disclaimer}</p>
    </div>
  );
}

function ReadingList({ groups, empty }: { groups: any[]; empty: string }) {
  const rows = (groups || []).flat();
  if (!rows.length) return <p>{empty}</p>;
  return (
    <ul>
      {rows.slice(0, 8).map((item: any, index: number) => (
        <li key={`${item.pinyin || item.pinyin_teochew || index}-${index}`}>
          {item.pinyin || item.pinyin_teochew || item.reading || "读音待标注"}
        </li>
      ))}
    </ul>
  );
}

function WugeSummary({ wuge }: { wuge: any }) {
  if (!wuge) return <p>五格计算值暂未评估</p>;
  const rows = [
    ["天格", wuge.tiange],
    ["人格", wuge.renge],
    ["地格", wuge.dige],
    ["外格", wuge.waige],
    ["总格", wuge.zongge],
    ["解释状态", enumLabel(wuge.interpretation_status)]
  ].filter(([, value]) => value !== undefined && value !== null && value !== "");
  return (
    <ul>
      {rows.map(([label, value]) => (
        <li key={label}>{label}：{String(value)}</li>
      ))}
    </ul>
  );
}

function ScoreBreakdown({ breakdown }: { breakdown: any }) {
  const labels: Record<string, string> = {
    phonetic: "读音",
    phonology: "音律",
    meaning: "字义",
    culture: "文化",
    structure: "结构",
    archetype: "人格",
    uniqueness: "热门与模板避让",
    aesthetic: "字形审美",
    fortune: "传统文化适配",
    naturalness: "自然度",
    penalties: "扣分项"
  };
  const rows = Object.entries(breakdown || {}).filter(([key]) => labels[key]);
  if (!rows.length) return null;
  return (
    <ul>
      {rows.map(([key, value]) => (
        <li key={key}>{labels[key]}：{formatScore(value)}</li>
      ))}
    </ul>
  );
}

function List({ items, fallback }: { items: unknown; fallback: string }) {
  const values = cleanList(items);
  if (!values.length) return fallback ? <p>{fallback}</p> : null;
  return (
    <ul>
      {values.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}
