"use client";

import { useRouter } from "next/navigation";
import type { ReactNode } from "react";
import { useState } from "react";
import { generateNames } from "../lib/api";
import { ProfileForm, SUPPORTED_CITIES, splitChars, validateProfile } from "../lib/validation";

const styles = ["书卷清雅", "君子品格", "山水自然", "温润知性", "现代高级"];

const initialProfile: ProfileForm = {
  surname: "林",
  gender: "male",
  calendar_type: "solar",
  birth_year: 2025,
  birth_month: 3,
  birth_day: 1,
  birth_hour: 8,
  birth_minute: 30,
  is_leap_month: false,
  birth_province: "广东省",
  birth_city: "汕头市",
  timezone: "Asia/Shanghai",
  region: "teochew",
  style_preferences: ["书卷清雅", "君子品格"],
  liked_chars: [],
  blocked_chars: [],
  generation_seed: null
};

export default function HomePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<ProfileForm>(initialProfile);
  const [likedText, setLikedText] = useState("");
  const [blockedText, setBlockedText] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [serverError, setServerError] = useState("");

  function update<K extends keyof ProfileForm>(key: K, value: ProfileForm[K]) {
    setProfile((current) => ({ ...current, [key]: value }));
  }

  function toggleStyle(style: string) {
    setProfile((current) => {
      const exists = current.style_preferences.includes(style);
      const next = exists ? current.style_preferences.filter((item) => item !== style) : [...current.style_preferences, style];
      return { ...current, style_preferences: next };
    });
  }

  async function submit() {
    const nextProfile = { ...profile, liked_chars: splitChars(likedText), blocked_chars: splitChars(blockedText) };
    const nextErrors = validateProfile(nextProfile);
    setErrors(nextErrors);
    setServerError("");
    if (Object.keys(nextErrors).length) return;
    setSubmitting(true);
    try {
      localStorage.setItem("yiyuan:lastProfile", JSON.stringify(nextProfile));
      const accepted = await generateNames(nextProfile);
      router.push(`/generating/${accepted.request_id}`);
    } catch (error) {
      setServerError(error instanceof Error ? error.message : "生成请求失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <h1>易元命名 Pro MVP</h1>
          <span>宝宝信息填写</span>
        </div>
        <span className="badge">NES_MVP_2.0</span>
      </header>

      <div className="layout">
        <section className="panel stack">
          <h2>宝宝档案</h2>
          <div className="notice">当前MVP仅支持汕头、潮州、揭阳的真太阳时计算。</div>

          <div className="form-grid">
            <Field label="姓氏" error={errors.surname}>
              <input value={profile.surname} onChange={(event) => update("surname", event.target.value)} />
            </Field>

            <Field label="性别">
              <select value={profile.gender} onChange={(event) => update("gender", event.target.value)}>
                <option value="male">男孩</option>
                <option value="female">女孩</option>
                <option value="neutral">中性</option>
              </select>
            </Field>

            <Field label="历法">
              <div className="segmented">
                <button className={`segment ${profile.calendar_type === "solar" ? "active" : ""}`} type="button" onClick={() => update("calendar_type", "solar")}>
                  公历
                </button>
                <button className={`segment ${profile.calendar_type === "lunar" ? "active" : ""}`} type="button" onClick={() => update("calendar_type", "lunar")}>
                  农历
                </button>
              </div>
            </Field>

            {profile.calendar_type === "lunar" ? (
              <Field label="闰月">
                <select value={profile.is_leap_month ? "yes" : "no"} onChange={(event) => update("is_leap_month", event.target.value === "yes")}>
                  <option value="no">不是闰月</option>
                  <option value="yes">闰月</option>
                </select>
              </Field>
            ) : (
              <Field label="时区">
                <input value={profile.timezone} readOnly />
              </Field>
            )}

            <Field label="出生年" error={errors.birth_year}>
              <input type="number" value={profile.birth_year} onChange={(event) => update("birth_year", Number(event.target.value))} />
            </Field>
            <Field label="出生月" error={errors.birth_month}>
              <input type="number" value={profile.birth_month} onChange={(event) => update("birth_month", Number(event.target.value))} />
            </Field>
            <Field label="出生日" error={errors.birth_day}>
              <input type="number" value={profile.birth_day} onChange={(event) => update("birth_day", Number(event.target.value))} />
            </Field>
            <Field label="出生小时" error={errors.birth_hour}>
              <input type="number" value={profile.birth_hour} onChange={(event) => update("birth_hour", Number(event.target.value))} />
            </Field>
            <Field label="出生分钟" error={errors.birth_minute}>
              <input type="number" value={profile.birth_minute} onChange={(event) => update("birth_minute", Number(event.target.value))} />
            </Field>
            <Field label="省份">
              <input value={profile.birth_province} onChange={(event) => update("birth_province", event.target.value)} />
            </Field>
            <Field label="城市" error={errors.birth_city}>
              <select value={profile.birth_city} onChange={(event) => update("birth_city", event.target.value)}>
                {SUPPORTED_CITIES.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="地域">
              <select value={profile.region} onChange={(event) => update("region", event.target.value)}>
                <option value="teochew">潮汕</option>
                <option value="mandarin">普通话</option>
              </select>
            </Field>
            <Field label="喜欢字">
              <input value={likedText} onChange={(event) => setLikedText(event.target.value)} placeholder="例如：知 清 予" />
            </Field>
            <Field label="禁用字" error={errors.blocked_chars}>
              <input value={blockedText} onChange={(event) => setBlockedText(event.target.value)} placeholder="例如：梓 轩 诺" />
            </Field>
          </div>

          <div className="field">
            <label>风格偏好</label>
            <div className="chips">
              {styles.map((style) => (
                <button key={style} type="button" className={`chip ${profile.style_preferences.includes(style) ? "active" : ""}`} onClick={() => toggleStyle(style)}>
                  {style}
                </button>
              ))}
            </div>
          </div>

          {serverError ? <div className="field-error">{serverError}</div> : null}

          <div className="actions">
            <button className="button" type="button" disabled={submitting} onClick={submit}>
              {submitting ? "生成中" : "生成姓名方案"}
            </button>
          </div>
        </section>

        <aside className="panel stack">
          <h3>当前配置</h3>
          <div className="small">姓氏：{profile.surname || "未填写"}</div>
          <div className="small">性别：{profile.gender === "male" ? "男孩" : profile.gender === "female" ? "女孩" : "中性"}</div>
          <div className="small">城市：{profile.birth_city}</div>
          <div className="small">风格：{profile.style_preferences.join("、") || "未选择"}</div>
          <div className="small">历法：{profile.calendar_type === "solar" ? "公历" : "农历"}</div>
        </aside>
      </div>
    </main>
  );
}

function Field({ label, error, children }: { label: string; error?: string; children: ReactNode }) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
      {error ? <span className="field-error">{error}</span> : null}
    </div>
  );
}
