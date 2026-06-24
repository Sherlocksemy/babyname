from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from app.adapters.location_adapter import CITY_COORDINATES
from app.repositories.naming_repository import NamingRepository, dumps, loads
from app.schemas.api_error import ApiError
from app.schemas.api_request import NamingGenerateRequest, RegenerateRequest
from app.services.candidate_detail_service import CandidateDetailService


class NamingApplicationService:
    def __init__(self, db, orchestrator, indexes: dict[str, Any] | None = None) -> None:
        self.db = db
        self.orchestrator = orchestrator
        self.indexes = indexes or {}
        self.repo = NamingRepository(db)
        self.detail_service = CandidateDetailService(indexes)

    def generate(self, request: NamingGenerateRequest) -> dict:
        payload = request.model_dump()
        payload["generation_seed"] = payload.get("generation_seed") or 20260623
        self._validate_supported_city(payload["birth_city"])
        session = self.repo.create_session(payload)
        run_number = 1
        seed = int(payload["generation_seed"])
        try:
            return self._execute_run(session.session_id, payload, run_number=run_number, seed=seed, exclude_names=set())
        except ApiError as exc:
            self.db.rollback()
            self.repo.record_failed_run(session.session_id, run_number, seed, exc.code, exc.message, session_status="FAILED")
            raise
        except Exception as exc:
            self.db.rollback()
            mapped = self._map_generation_error(exc)
            self.repo.record_failed_run(session.session_id, run_number, seed, mapped.code, mapped.message, session_status="FAILED")
            raise mapped from exc

    def regenerate(self, request_id: str, request: RegenerateRequest) -> dict:
        session = self.repo.get_session(request_id)
        if session is None:
            raise ApiError("SESSION_NOT_FOUND", "Naming session not found.", status_code=404)
        original_payload = loads(session.request_payload_json)
        if not isinstance(original_payload, dict):
            raise ApiError("GENERATION_FAILED", "Stored request payload is not readable.", status_code=500)
        payload = dict(original_payload)
        if request.liked_chars:
            payload["liked_chars"] = list(dict.fromkeys(payload.get("liked_chars", []) + request.liked_chars))
        if request.blocked_chars:
            payload["blocked_chars"] = list(dict.fromkeys(payload.get("blocked_chars", []) + request.blocked_chars))
        run_number = len(self.repo.list_runs(request_id)) + 1
        seed = int(request.generation_seed or (int(payload.get("generation_seed") or 20260623) + run_number * 9973))
        payload["generation_seed"] = seed
        previous = self._shown_names(request_id)
        previous_status = session.status if session.status in {"COMPLETED", "PARTIAL"} else "COMPLETED"
        try:
            return self._execute_run(request_id, payload, run_number=run_number, seed=seed, exclude_names=previous)
        except ApiError as exc:
            self.db.rollback()
            self.repo.record_failed_run(request_id, run_number, seed, exc.code, exc.message, session_status=previous_status)
            raise
        except Exception as exc:
            self.db.rollback()
            mapped = self._map_generation_error(exc)
            self.repo.record_failed_run(request_id, run_number, seed, mapped.code, mapped.message, session_status=previous_status)
            raise mapped from exc

    def get_result(self, request_id: str) -> dict:
        session = self.repo.get_session(request_id)
        if session is None:
            raise ApiError("SESSION_NOT_FOUND", "Naming session not found.", status_code=404)
        if session.status in {"PENDING", "RUNNING"}:
            return {
                "request_id": request_id,
                "status": session.status,
                "progress": {"stage": "GENERATING", "message": "正在生成姓名方案"},
            }
        if session.status == "FAILED":
            return {
                "request_id": request_id,
                "status": "FAILED",
                "result_status": "GENERATION_FAILED",
                "counts": {"top3": 0, "backup": 0, "qualified": 0, "required": 10},
                "progress": {"stage": "FAILED", "message": session.error_message or "生成失败"},
                "warnings": [session.error_code] if session.error_code else [],
            }
        run = self.repo.latest_readable_run(request_id)
        if run is None:
            raise ApiError("GENERATION_FAILED", "No naming run exists for this session.", status_code=500)
        candidates = self.repo.list_candidates_for_run(run.run_id)
        top3 = [self.detail_service.to_card(row) for row in candidates if row.rank_type == "TOP3"]
        backup7 = [self.detail_service.to_card(row) for row in candidates if row.rank_type == "BACKUP7"]
        summary = loads(run.result_summary_json) or {}
        return {
            "request_id": request_id,
            "run_id": run.run_id,
            "status": session.status,
            "profile_summary": self._profile_summary(loads(session.request_payload_json) or {}, summary),
            "fortune_summary": self._fortune_summary(summary),
            "top3": top3,
            "backup7": backup7,
            "result_status": summary.get("result_status"),
            "counts": summary.get("counts", {"top3": len(top3), "backup": len(backup7), "qualified": len(top3) + len(backup7), "required": 10}),
            "limitations": summary.get("limitations", []),
            "warnings": summary.get("warnings", []),
        }

    def get_candidate_detail(self, request_id: str, candidate_id: str) -> dict:
        session = self.repo.get_session(request_id)
        if session is None:
            raise ApiError("SESSION_NOT_FOUND", "Naming session not found.", status_code=404)
        row = self.repo.get_candidate_in_session(request_id, candidate_id)
        if row is None:
            raise ApiError("CANDIDATE_NOT_FOUND", "Candidate not found in this naming session.", status_code=404)
        return self.detail_service.to_detail(row, request_id)

    def _execute_run(self, session_id: str, payload: dict, run_number: int, seed: int, exclude_names: set[str]) -> dict:
        started = time.perf_counter()
        result = self._run_with_exclusion(payload, exclude_names)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        top3 = result.get("top3") or []
        backup7 = result.get("backup7") or []
        contract = self._result_contract(result, top3, backup7)
        if contract["status"] == "FAILED":
            raise ApiError(
                contract["result_status"],
                "Naming engine did not return at least 3 qualified Top3 candidates.",
                status_code=409,
                details=contract["counts"],
            )
        run = self.repo.create_run(session_id, run_number, seed, status=contract["status"], commit=False)
        saved = self.repo.save_candidates(run.run_id, top3, backup7, commit=False)
        result_summary = {
            "run_id": run.run_id,
            "ranking_version": "RankingEngine.MVP",
            "result_status": contract["result_status"],
            "counts": contract["counts"],
            "warnings": self._warnings(result),
            "limitations": self._limitations(result),
            "profile": result.get("profile"),
            "baby_profile": result.get("baby_profile"),
            "fortune": result.get("fortune"),
            "top3_names": [item.get("full_name") for item in top3],
            "backup7_names": [item.get("full_name") for item in backup7],
            "candidate_count": len(saved),
            "generation_elapsed_ms": elapsed_ms,
        }
        self.repo.complete_run(run.run_id, result_summary, status=contract["status"], commit=False)
        self.repo.update_session_status(session_id, contract["status"], commit=False)
        self.db.commit()
        return {
            "request_id": session_id,
            "run_id": run.run_id,
            "status": contract["status"],
            "result_status": contract["result_status"],
            "top3": [self.detail_service.to_card(row) for row in saved if row.rank_type == "TOP3"],
            "backup7": [self.detail_service.to_card(row) for row in saved if row.rank_type == "BACKUP7"],
            "counts": contract["counts"],
            "warnings": result_summary["warnings"],
            "limitations": result_summary["limitations"],
            "created_at": run.created_at.isoformat(),
        }

    def _run_with_exclusion(self, payload: dict, exclude_names: set[str]) -> dict:
        best_partial: dict | None = None
        for attempt in range(5):
            attempt_payload = dict(payload)
            attempt_payload["generation_seed"] = int(payload["generation_seed"]) + attempt * 7919
            attempt_payload["exclude_given_names"] = sorted(exclude_names)
            result = self.orchestrator.run(attempt_payload)
            if not result.get("ok"):
                raise ApiError("INVALID_INPUT", "; ".join(result.get("errors") or ["Invalid naming input."]), status_code=422)
            status = self._result_contract(result, result.get("top3") or [], result.get("backup7") or [])
            if status["status"] == "COMPLETED":
                return result
            if status["status"] == "PARTIAL" and best_partial is None:
                best_partial = result
        if best_partial:
            return best_partial
        raise ApiError(
            "INSUFFICIENT_QUALIFIED_CANDIDATES",
            "Unable to generate at least 3 qualified candidates.",
            status_code=409,
            details={"shown_names_excluded": len(exclude_names)},
        )

    @staticmethod
    def _result_contract(result: dict, top3: list[dict], backup7: list[dict]) -> dict:
        top3_count = len(top3)
        backup_count = len(backup7)
        qualified = int(result.get("qualified_count") or len(result.get("top10") or []) or top3_count + backup_count)
        counts = {"top3": top3_count, "backup": backup_count, "qualified": qualified, "required": 10}
        if top3_count == 3 and backup_count == 7:
            return {"status": "COMPLETED", "result_status": "COMPLETE", "counts": counts}
        if top3_count == 3:
            return {"status": "PARTIAL", "result_status": "INSUFFICIENT_QUALIFIED_CANDIDATES", "counts": counts}
        return {"status": "FAILED", "result_status": "INSUFFICIENT_QUALIFIED_CANDIDATES", "counts": counts}

    @staticmethod
    def _select_visible_candidates(result: dict, exclude_names: set[str]) -> tuple[list[dict], list[dict]]:
        raise RuntimeError("_select_visible_candidates is disabled; RankingEngine result is the only visible-result source.")

    def _shown_names(self, request_id: str) -> set[str]:
        names: set[str] = set()
        for row in self.repo.list_candidates_for_session(request_id):
            names.add(row.full_name)
            names.add(row.given_name)
        return names

    @staticmethod
    def _unused_legacy_select_visible_candidates(result: dict, exclude_names: set[str]) -> tuple[list[dict], list[dict]]:
        if result or exclude_names:
            raise ApiError(
                "GENERATION_FAILED",
                "Application-layer reranking is disabled.",
                status_code=500,
            )
        return [], []

    @staticmethod
    def _validate_supported_city(city: str) -> None:
        normalized = city.replace("广东省", "").replace("广东", "").strip()
        if normalized not in CITY_COORDINATES:
            raise ApiError(
                "LOCATION_DATA_MISSING",
                "当前MVP仅支持汕头市、潮州市、揭阳市的真太阳时计算。",
                status_code=422,
                field="birth_city",
                details={"supported_cities": ["汕头市", "潮州市", "揭阳市"]},
            )

    @staticmethod
    def _map_generation_error(exc: Exception) -> ApiError:
        message = str(exc)
        lower = message.lower()
        if "leap" in lower or "闰" in message:
            return ApiError("INVALID_LEAP_MONTH", "Invalid lunar leap month.", status_code=422, field="is_leap_month")
        if "lunar" in lower or "农历" in message:
            return ApiError("INVALID_LUNAR_DATE", "Invalid lunar date.", status_code=422)
        if "1900" in message or "2100" in message:
            return ApiError("UNSUPPORTED_DATE_RANGE", "Unsupported date range.", status_code=422)
        return ApiError("GENERATION_FAILED", "Name generation failed.", status_code=500)

    @staticmethod
    def _warnings(result: dict) -> list[str]:
        warnings: list[str] = []
        fortune = result.get("fortune") or {}
        warnings.extend((fortune.get("fusion") or {}).get("warnings") or [])
        warnings.extend((fortune.get("true_solar_time") or {}).get("warnings") or [])
        return list(dict.fromkeys(str(item) for item in warnings if item))

    @staticmethod
    def _limitations(result: dict) -> list[str]:
        limitations: list[str] = []
        fortune = result.get("fortune") or {}
        limitations.extend((fortune.get("fusion") or {}).get("limitations") or [])
        limitations.extend((fortune.get("five_elements") or {}).get("limitations") or [])
        limitations.append("传统命理、生肖及五格内容仅供文化参考。")
        return list(dict.fromkeys(str(item) for item in limitations if item))

    @staticmethod
    def _profile_summary(payload: dict, summary: dict) -> dict:
        return {
            "surname": payload.get("surname"),
            "gender": payload.get("gender"),
            "calendar_type": payload.get("calendar_type"),
            "birth_time": f"{payload.get('birth_year')}-{payload.get('birth_month')}-{payload.get('birth_day')} {payload.get('birth_hour')}:{payload.get('birth_minute')}",
            "birth_city": payload.get("birth_city"),
            "region": payload.get("region"),
            "style_preferences": payload.get("style_preferences", []),
            "baby_profile": summary.get("baby_profile"),
        }

    @staticmethod
    def _fortune_summary(summary: dict) -> dict:
        fortune = summary.get("fortune") or {}
        four = fortune.get("four_pillars") or {}
        five = fortune.get("five_elements") or {}
        zodiac = fortune.get("zodiac") or {}
        true_solar = fortune.get("true_solar_time") or {}
        return {
            "status": fortune.get("status"),
            "four_pillars": four.get("pillars") or four,
            "day_master": four.get("day_master"),
            "five_elements": five.get("element_counts") or five.get("normalized_distribution") or {},
            "supportive_elements": five.get("supportive_elements", []),
            "zodiac": zodiac.get("bazi_zodiac") or zodiac.get("folk_zodiac"),
            "true_solar_time": true_solar,
            "calculation_status": fortune.get("status"),
        }
