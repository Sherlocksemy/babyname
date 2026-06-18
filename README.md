# 易元命名 MVP

知识库驱动的新生儿智能取名系统。后端直接只读引用 `01_knowledge_base/`，不修改原始知识库；名字由本地知识库和规则引擎筛选生成，不使用 AI 直接生成最终名字。

## 后端运行

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

## 前端运行

```bash
cd frontend
npm install
npm run dev
```

Windows 推荐使用脚本启动，避免重复传入 Next.js `--hostname/--port` 导致页面事件未绑定：

```powershell
.\scripts\run_backend.ps1
.\scripts\run_frontend.ps1
```

或同时打开两个服务窗口：

```powershell
.\scripts\run_dev.ps1
```

默认前端访问 `http://127.0.0.1:3000`，后端 API 为 `http://127.0.0.1:8000`。

## 测试

```bash
python -m pytest
```

## 审计报告

知识库审计报告输出到 `backend/reports/knowledge_audit_report.json`。
