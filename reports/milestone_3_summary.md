# Milestone 3 Summary

## Status

Milestone 3 API, SQLite, and frontend MVP integration is implemented and validated.

## Added Dependencies

- fastapi==0.137.2: HTTP API and Swagger.
- uvicorn==0.49.0: local ASGI server.
- pydantic==2.13.4: request validation.
- SQLAlchemy==2.0.51: SQLite ORM persistence.
- httpx==0.28.1: API tests and smoke checks.
- pytest==9.1.0: backend tests.
- pandas==3.0.3: retained verified data tooling dependency.
- Next.js 16.2.9 / React 19.2.7 / TypeScript 6.0.3 / tsx 4.22.4: frontend MVP.

## SQLite Tables

- naming_sessions
- naming_runs
- candidates
- favorites

## API Endpoints

- GET /health
- GET /ready
- POST /api/v1/names/generate
- GET /api/v1/names/{request_id}
- GET /api/v1/names/{request_id}/candidates/{candidate_id}
- POST /api/v1/names/{request_id}/regenerate
- POST /api/v1/favorites
- GET /api/v1/favorites?request_id=
- DELETE /api/v1/favorites/{favorite_id}

## Frontend Pages

- /
- /generating/[requestId]
- /results/[requestId]
- /results/[requestId]/[candidateId]

## E2E Result

- Request ID: req_671837b9d72f42f9ae2693222fad9a98
- Top3: 林思敬 / 林思弘 / 林敬谦
- Backup7: 林承仁 / 林承贤 / 林仁庭 / 林谦正 / 林安德 / 林德嘉 / 林明信
- Regenerated Top3: 林贤庭 / 林仁承 / 林贤承
- Regenerated Backup7: 林嘉信 / 林德修 / 林德朗 / 林谦章 / 林云章 / 林波文
- Regeneration overlap: []
- Favorite ID: fav_f7beb88c80c34df8a9f4d6735473e80e

## Test Results

- Backend: 105 passed, 33 warnings in 210.37s.
- Frontend lint: passed.
- Frontend test: 4 passed.
- Frontend build: passed.
- HTTP E2E smoke: passed.

## Performance

- Startup elapsed: 5711.78 ms.
- Knowledge load elapsed: 442.76 ms.
- Generate API elapsed: 1875.71 ms.
- Engine generation elapsed: 1725.02 ms.
- Result read elapsed: 9.4 ms.
- Candidate detail elapsed: 8.34 ms.
- Regenerate API elapsed: 1788.32 ms.

## Known Limits

- Generation is synchronous inside the 202 API contract for MVP.
- Only 汕头市、潮州市、揭阳市 are supported for true solar time.
- Wuge interpretation remains DATA_INCOMPLETE and only numeric values are shown.
- No auth, payment, PDF, sharing, admin, Redis, PostgreSQL, LangGraph, or Agent work was added.
- npm audit reports 2 moderate vulnerabilities in the current dependency tree; no forced upgrade was applied.

## Acceptance

Milestone 3 acceptance standard: passed for local MVP integration. Do not enter payment, membership, PDF, or production deployment without confirmation.
