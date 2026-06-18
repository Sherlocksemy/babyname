"use client";

import { BookOpen, Heart, RefreshCcw, Search, Star } from "lucide-react";
import { useMemo, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

type Candidate = {
  name: string;
  given_name: string;
  group: string;
  score: number;
  pinyin: string;
  summary: string;
  culture_origin: { core?: any };
  pronunciation: any;
  teochew: any;
  bazi: any;
  zodiac: any;
  wuge: any;
  popularity: any;
  score_breakdown: any;
  warnings: string[];
  recommendation_reason: string;
};

export default function Home() {
  const [form, setForm] = useState({
    surname: "陈",
    gender: "female",
    birth_datetime: "2026-06-18 09:30",
    birth_place: "广东省汕头市",
    name_length: 2,
    style_preferences: "温润,诗意",
    banned_chars: "梓,轩",
    liked_chars: "清",
    avoid_hot_names: true,
    need_teochew_check: true,
    need_culture_origin: true
  });
  const [requestId, setRequestId] = useState("");
  const [results, setResults] = useState<Candidate[]>([]);
  const [selected, setSelected] = useState<Candidate | null>(null);
  const [favorites, setFavorites] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const grouped = useMemo(() => {
    return {
      featured: results.filter((item) => item.group === "精选推荐"),
      style: results.filter((item) => item.group === "风格备选"),
      creative: results.filter((item) => item.group === "创意探索")
    };
  }, [results]);

  async function generate() {
    setLoading(true);
    setError("");
    try {
      const payload = {
        ...form,
        style_preferences: split(form.style_preferences),
        banned_chars: split(form.banned_chars),
        liked_chars: split(form.liked_chars),
        name_length: Number(form.name_length)
      };
      const res = await fetch(`${API_BASE}/api/names/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setRequestId(data.request_id);
      setResults(data.results || []);
      setSelected(data.results?.[0] || null);
    } catch (err: any) {
      setError(err.message || "生成失败");
    } finally {
      setLoading(false);
    }
  }

  async function regenerate() {
    if (!requestId) return generate();
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/names/regenerate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request_id: requestId, excluded_names: results.map((item) => item.name) })
      });
      const data = await res.json();
      setRequestId(data.request_id);
      setResults(data.results || []);
      setSelected(data.results?.[0] || null);
    } finally {
      setLoading(false);
    }
  }

  function favorite(item: Candidate) {
    setFavorites((prev) => (prev.some((fav) => fav.name === item.name) ? prev : [...prev, item]));
  }

  return (
    <main>
      <section className="shell">
        <aside className="panel form">
          <h1>易元命名</h1>
          <div className="grid">
            <Field label="姓氏" value={form.surname} onChange={(v) => setForm({ ...form, surname: v })} />
            <label>
              性别
              <select value={form.gender} onChange={(e) => setForm({ ...form, gender: e.target.value })}>
                <option value="female">女</option>
                <option value="male">男</option>
                <option value="neutral">中性</option>
              </select>
            </label>
            <Field label="出生时间" value={form.birth_datetime} onChange={(v) => setForm({ ...form, birth_datetime: v })} />
            <Field label="出生地" value={form.birth_place} onChange={(v) => setForm({ ...form, birth_place: v })} />
            <label>
              名字字数
              <select value={form.name_length} onChange={(e) => setForm({ ...form, name_length: Number(e.target.value) })}>
                <option value={1}>单字名</option>
                <option value={2}>双字名</option>
              </select>
            </label>
            <Field label="风格偏好" value={form.style_preferences} onChange={(v) => setForm({ ...form, style_preferences: v })} />
            <Field label="禁用字" value={form.banned_chars} onChange={(v) => setForm({ ...form, banned_chars: v })} />
            <Field label="喜欢字" value={form.liked_chars} onChange={(v) => setForm({ ...form, liked_chars: v })} />
          </div>
          <div className="checks">
            <label><input type="checkbox" checked={form.avoid_hot_names} onChange={(e) => setForm({ ...form, avoid_hot_names: e.target.checked })} />避开爆款</label>
            <label><input type="checkbox" checked={form.need_teochew_check} onChange={(e) => setForm({ ...form, need_teochew_check: e.target.checked })} />潮汕话检查</label>
            <label><input type="checkbox" checked={form.need_culture_origin} onChange={(e) => setForm({ ...form, need_culture_origin: e.target.checked })} />需要出处</label>
          </div>
          <div className="actions">
            <button onClick={generate} disabled={loading}><Search size={18} />{loading ? "生成中" : "生成名字"}</button>
            <button className="ghost" onClick={regenerate} disabled={loading || !results.length}><RefreshCcw size={18} />换一批</button>
          </div>
          {error && <p className="error">{error}</p>}
        </aside>

        <section className="content">
          <NameGroup title="精选推荐" items={grouped.featured} onSelect={setSelected} onFavorite={favorite} />
          <NameGroup title="风格备选" items={grouped.style} onSelect={setSelected} onFavorite={favorite} />
          <NameGroup title="创意探索" items={grouped.creative} onSelect={setSelected} onFavorite={favorite} />
        </section>

        <aside className="panel detail">
          {selected ? <Detail item={selected} /> : <div className="empty">生成后查看名字详情</div>}
          <div className="compare">
            <h2>收藏对比</h2>
            {favorites.map((item) => (
              <div className="fav" key={item.name}>
                <strong>{item.name}</strong><span>{item.score}</span><small>{item.popularity?.heat_level}</small>
              </div>
            ))}
          </div>
        </aside>
      </section>
    </main>
  );
}

function Field({ label, value, onChange }: { label: string; value: any; onChange: (value: string) => void }) {
  return <label>{label}<input value={value} onChange={(e) => onChange(e.target.value)} /></label>;
}

function NameGroup({ title, items, onSelect, onFavorite }: any) {
  if (!items.length) return null;
  return <section><h2>{title}</h2><div className="cards">{items.map((item: Candidate) => <article className="card" key={item.name} onClick={() => onSelect(item)}><div><strong>{item.name}</strong><span>{item.pinyin}</span></div><b>{item.score}</b><p>{item.summary}</p><footer><button onClick={(e) => { e.stopPropagation(); onFavorite(item); }}><Heart size={16} />收藏</button><span>{item.popularity?.heat_level}</span></footer></article>)}</div></section>;
}

function Detail({ item }: { item: Candidate }) {
  const core = item.culture_origin?.core || {};
  return <div><h2>{item.name}<span>{item.score}</span></h2><p className="reason">{item.recommendation_reason}</p><Info icon={<BookOpen size={16} />} title="文化出处" value={core.title ? `${core.source}《${core.title}》：${core.original_text}` : "无高置信度核心出处"} /><Info icon={<Star size={16} />} title="读音" value={`${item.pinyin}；普通话分 ${item.score_breakdown?.mandarin}/15`} /><Info title="八字参考" value={item.bazi?.explanation || ""} /><Info title="生肖参考" value={item.zodiac?.notes || ""} /><Info title="五格简析" value={item.wuge?.notes || ""} />{item.warnings?.length > 0 && <div className="warn">{item.warnings.join(" / ")}</div>}</div>;
}

function Info({ title, value, icon }: { title: string; value: string; icon?: any }) {
  return <div className="info"><h3>{icon}{title}</h3><p>{value}</p></div>;
}

function split(value: string) {
  return value.split(/[,，、\s]+/).map((item) => item.trim()).filter(Boolean);
}
