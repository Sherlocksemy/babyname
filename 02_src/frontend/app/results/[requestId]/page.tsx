"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { createFavorite, getResult, listFavorites, regenerate } from "../../../lib/api";
import { archetypeLabel, cleanList, displayScore, enumLabel, formatScore, formatTrueSolarTime, fourPillarRows, originModeLabel, riskLabel, structureLabel, teochewSummary } from "../../../lib/display";
import { originSummaryText, partialResultMessage } from "../../../lib/origin";

export default function ResultsPage() {
  const params = useParams<{ requestId: string }>();
  const router = useRouter();
  const [result, setResult] = useState<any>(null);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);

  async function load() {
    const data = await getResult(params.requestId);
    setResult(data);
    const favoriteData = await listFavorites(params.requestId);
    setFavorites(new Set((favoriteData.favorites || []).map((item: any) => item.candidate_id)));
  }

  useEffect(() => {
    load()
      .catch((err) => setError(err instanceof Error ? err.message : "结果读取失败"))
      .finally(() => setLoading(false));
  }, [params.requestId]);

  async function favorite(candidateId: string) {
    await createFavorite(params.requestId, candidateId);
    setFavorites((current) => new Set([...current, candidateId]));
  }

  async function doRegenerate() {
    setRegenerating(true);
    setError("");
    try {
      await regenerate(params.requestId);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "换一批失败");
    } finally {
      setRegenerating(false);
    }
  }

  if (loading) return <main className="shell"><section className="panel">读取结果中</section></main>;
  if (error && !result) return <main className="shell"><section className="panel field-error">{error}</section></main>;
  if (!result) return null;

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <h1>命名结果</h1>
          <span>精品方案与备选方案</span>
        </div>
        <div className="actions">
          <button className="button secondary" type="button" disabled={regenerating} onClick={doRegenerate}>
            {regenerating ? "换名中" : "换一批"}
          </button>
          <Link className="button subtle" href="/">
            返回修改资料
          </Link>
        </div>
      </header>

      <div className="stack" style={{ maxWidth: 1180, margin: "0 auto" }}>
        <section className="panel">
          <h2>宝宝画像摘要</h2>
          <div className="summary-grid">
            <Summary label="姓氏" value={result.profile_summary?.surname} />
            <Summary label="性别" value={enumLabel(result.profile_summary?.gender)} />
            <Summary label="出生城市" value={result.profile_summary?.birth_city} />
            <Summary label="历法" value={enumLabel(result.profile_summary?.calendar_type)} />
            <Summary label="出生时间" value={result.profile_summary?.birth_time} />
            <Summary label="风格偏好" value={(result.profile_summary?.style_preferences || []).join("、")} />
          </div>
        </section>

        <section className="panel">
          <h2>命理摘要</h2>
          <div className="summary-grid">
            {fourPillarRows(result.fortune_summary?.four_pillars).map(([label, value]) => (
              <Summary key={label} label={label} value={value} />
            ))}
            <Summary label="生肖" value={result.fortune_summary?.zodiac || "未评估"} />
            <Summary label="真太阳时" value={formatTrueSolarTime(result.fortune_summary?.true_solar_time?.true_solar_time)} />
            <Summary label="计算状态" value={enumLabel(result.fortune_summary?.calculation_status)} />
          </div>
          <Limitations items={result.limitations} />
        </section>
        {partialResultMessage(result) ? (
          <section className="notice">
            {partialResultMessage(result)}
          </section>
        ) : null}
        {error ? <section className="notice">{error}</section> : null}

        <section className="panel stack">
          <h2>Top3精品方案</h2>
          <div className="summary-grid">
            {result.top3.map((item: any) => (
              <CandidateCard key={item.candidate_id} item={item} requestId={params.requestId} favorited={favorites.has(item.candidate_id)} onFavorite={() => favorite(item.candidate_id)} />
            ))}
          </div>
        </section>

        <section className="panel stack">
          <h2>Top3对比</h2>
          <div className="compare-grid">
            {result.top3.map((item: any) => (
              <div className="card" key={item.candidate_id}>
                <h3>{item.full_name}</h3>
                <p className="small">综合推荐：{displayScore(item).grade}</p>
                <p className="small">姓名结构：{structureLabel(item)}</p>
                <p className="small">人格方向：{archetypeLabel(item)}</p>
                <p className="small">文化生成方式：{originModeLabel(item.origin)}</p>
                <p className="small">音律：{item.pinyin || "未标注"}</p>
                <p className="small">基础传统文化适配：{formatScore(item.nes_breakdown?.fortune)}</p>
                <p className="small">热门与模板风险：{riskLabel(item.popularity_template_risk)}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="panel stack">
          <h2>Backup7</h2>
          <div className="backup-grid">
            {result.backup7.map((item: any) => (
              <Link className="backup-item" key={item.candidate_id} href={`/results/${params.requestId}/${item.candidate_id}`}>
                <strong>{item.full_name}</strong>
                <div className="small">推荐等级：{displayScore(item).grade}</div>
                <div className="small">人格方向：{archetypeLabel(item)}</div>
                <div className="small">{(item.display_score?.diversity_reasons || [])[0] || "作为备选方案保留。"}</div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

function Summary({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="card">
      <div className="meta">{label}</div>
      <strong>{value || "未评估"}</strong>
    </div>
  );
}

function CandidateCard({ item, requestId, favorited, onFavorite }: { item: any; requestId: string; favorited: boolean; onFavorite: () => void }) {
  const score = displayScore(item);
  return (
    <article className="card stack">
      <p className="name">{item.full_name}</p>
      <div className="score">综合推荐：{score.grade}</div>
      <div className="small">推荐指数：{score.ranking}</div>
      <div className="small">姓名结构：{structureLabel(item)}</div>
      <div className="small">人格方向：{archetypeLabel(item)}</div>
      <OriginSummary origin={item.origin} />
      <div className="small">组合义：{item.one_sentence_meaning}</div>
      <div className="small">普通话：{item.pinyin || "未标注"}</div>
      <div className="small">{teochewSummary(item.teochew_pronunciation)}</div>
      <div className="small">热门与模板风险：{riskLabel(item.popularity_template_risk)}</div>
      <div className="candidate-actions">
        <button className="button secondary" type="button" disabled={favorited} onClick={onFavorite}>
          {favorited ? "已收藏" : "收藏"}
        </button>
        <Link className="button subtle" href={`/results/${requestId}/${item.candidate_id}`}>
          查看详情
        </Link>
      </div>
    </article>
  );
}

function OriginSummary({ origin }: { origin: any }) {
  if (!origin) return <div className="small">出处：未标注</div>;
  if (origin.mode === "DIRECT_EXPRESSION") {
    const evidence = origin.name_level_evidence || {};
    return <div className="small">{origin.display_label} “{evidence.display_excerpt || evidence.matched_text || ""}”</div>;
  }
  return (
    <div className="small">
      {originSummaryText(origin)}
    </div>
  );
}

function Limitations({ items }: { items: unknown }) {
  const values = cleanList(items);
  if (!values.length) return null;
  return (
    <ul className="small">
      {values.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}
