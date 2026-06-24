"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getResult } from "../../../lib/api";

const stages = ["资料校验", "传统历法计算", "文化出处检索", "候选生成", "质量审查", "结果整理"];

export default function GeneratingPage() {
  const params = useParams<{ requestId: string }>();
  const router = useRouter();
  const [status, setStatus] = useState("RUNNING");
  const [message, setMessage] = useState("正在生成姓名方案");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    async function poll() {
      try {
        const result = await getResult(params.requestId);
        if (!active) return;
        setStatus(result.status);
        setMessage(result.progress?.message || "正在生成姓名方案");
        if (result.status === "COMPLETED") router.replace(`/results/${params.requestId}`);
        if (result.status === "FAILED") setError(result.progress?.message || "生成失败");
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "读取生成状态失败");
      }
    }
    poll();
    const timer = window.setInterval(poll, 1400);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [params.requestId, router]);

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <h1>生成中</h1>
          <span>{status}</span>
        </div>
        <Link className="button secondary" href="/">
          返回修改资料
        </Link>
      </header>
      <section className="panel stack" style={{ maxWidth: 760, margin: "0 auto" }}>
        <h2>{message}</h2>
        <div className="timeline">
          {stages.map((stage, index) => (
            <div key={stage} className={index === 3 ? "active" : ""}>
              {stage}
            </div>
          ))}
        </div>
        {error ? <div className="field-error">{error}</div> : null}
      </section>
    </main>
  );
}
