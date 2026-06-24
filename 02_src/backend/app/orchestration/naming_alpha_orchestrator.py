from __future__ import annotations

from collections import Counter

from app.engines.archetype_engine import ArchetypeEngine
from app.engines.calendar_engine import CalendarEngine
from app.engines.candidate_quality_scorer import CandidateQualityScorer
from app.engines.candidate_reconstruction_validator import CandidateReconstructionValidator
from app.engines.char_pool_builder import CharPoolBuilder
from app.engines.culture_retriever import CultureRetriever
from app.engines.five_elements_engine import FiveElementsEngine
from app.engines.fortune_fusion_engine import FortuneFusionEngine
from app.engines.four_pillars_engine import FourPillarsEngine
from app.engines.name_composer import NameComposer
from app.engines.profile_specificity_engine import ProfileSpecificityEngine
from app.engines.quality_guard import QualityGuard
from app.engines.ranking_engine import RankingEngine
from app.engines.surname_fit_evaluator import SurnameFitEvaluator
from app.engines.structure_engine import StructureEngine
from app.engines.true_solar_time_engine import TrueSolarTimeEngine
from app.engines.wuge_engine import WugeEngine
from app.engines.zodiac_engine import ZodiacEngine
from app.schemas.baby_profile import BabyProfile
from app.schemas.fortune import FortuneContext
from app.schemas.naming_context import NamingContext
from app.schemas.naming_input import NamingInput


class NamingAlphaOrchestrator:
    def __init__(self) -> None:
        self.structure_engine = StructureEngine()
        self.archetype_engine = ArchetypeEngine()
        self.culture_retriever = CultureRetriever()
        self.char_pool_builder = CharPoolBuilder()
        self.name_composer = NameComposer(self.culture_retriever)
        self.quality_guard = QualityGuard()
        self.reconstruction_validator = CandidateReconstructionValidator()
        self.profile_engine = ProfileSpecificityEngine()
        self.surname_fit_evaluator = SurnameFitEvaluator()
        self.scorer = CandidateQualityScorer()
        self.ranker = RankingEngine()
        self.calendar_engine = CalendarEngine()
        self.true_solar_time_engine = TrueSolarTimeEngine()
        self.four_pillars_engine = FourPillarsEngine()
        self.five_elements_engine = FiveElementsEngine()
        self.zodiac_engine = ZodiacEngine()
        self.wuge_engine = WugeEngine()
        self.fortune_fusion_engine = FortuneFusionEngine()

    def run(self, payload: NamingInput | dict) -> dict:
        baby_profile = self._baby_profile(payload)
        profile_errors = baby_profile.validate()
        if profile_errors:
            return {"ok": False, "errors": profile_errors}
        naming_input = baby_profile.to_naming_input()
        errors = naming_input.validate()
        if errors:
            return {"ok": False, "errors": errors}

        context = NamingContext(naming_input=naming_input)
        fortune_context = self._build_fortune_context(baby_profile)
        profile = self.profile_engine.build(naming_input)
        structure_result = self.structure_engine.select(naming_input)
        context.structures = structure_result["candidate_structures"]
        archetype_result = self.archetype_engine.select(structure_result["top_structures"], naming_input)
        context.archetypes = archetype_result["candidate_archetypes"]
        context.culture_evidences = self.culture_retriever.retrieve(
            context.structures,
            context.archetypes,
            naming_input.style_preferences,
        )
        pools = self.char_pool_builder.build(naming_input, context.structures, context.archetypes, context.culture_evidences, fortune_context.to_dict())
        context.first_char_pool = pools["first_pool"]
        context.second_char_pool = pools["second_pool"]
        context.candidates = self.name_composer.compose(
            naming_input,
            context.first_char_pool,
            context.second_char_pool,
            context.structures,
            context.archetypes,
        )

        reason_counter: Counter[str] = Counter()
        first_pool_chars = {item.char for item in context.first_char_pool}
        second_pool_chars = {item.char for item in context.second_char_pool}
        for candidate in context.candidates:
            guard_result = self.quality_guard.evaluate(candidate, naming_input)
            candidate.quality_guard = guard_result
            candidate.reconstruction = self.reconstruction_validator.validate(candidate, first_pool_chars, second_pool_chars)
            candidate.surname_fit = self.surname_fit_evaluator.evaluate(naming_input.surname, candidate)
            candidate.surname_fit_score = candidate.surname_fit["surname_fit_score"]
            profile_fit = self.profile_engine.evaluate_candidate(candidate, profile, naming_input)
            candidate.style_fit_score = profile_fit["style_fit_score"]
            candidate.gender_tone_fit_score = profile_fit["gender_tone_fit_score"]
            candidate.gender_tone_reason_codes = profile_fit["gender_tone_reason_codes"]
            candidate.imagery_fit_score = profile_fit["imagery_fit_score"]
            candidate.profile_specificity_score = profile_fit["profile_specificity_score"]
            candidate.profile_fit_reasons = profile_fit["profile_fit_reasons"]
            candidate.profile_conflicts = profile_fit["profile_conflicts"]
            candidate.universal_candidate_risk = profile_fit["universal_candidate_risk"]
            candidate.cross_profile_dominance_risk = profile_fit["cross_profile_dominance_risk"]
            if candidate.profile_specificity_score < 45:
                guard_result["passed"] = False
                guard_result["hard_failures"].append("LOW_PROFILE_SPECIFICITY")
            if candidate.profile_conflicts:
                guard_result["soft_warnings"].extend(candidate.profile_conflicts)
            if not candidate.reconstruction["reconstructable"]:
                guard_result["passed"] = False
                guard_result["hard_failures"].extend(candidate.reconstruction["failures"])
            if not guard_result["passed"]:
                context.filtered_count += 1
                reason_counter.update(guard_result["hard_failures"])
                continue
            candidate_wuge = self.wuge_engine.calculate(naming_input.surname, candidate.given_name)
            fusion = self.fortune_fusion_engine.evaluate(
                candidate,
                fortune_context.five_elements,
                fortune_context.zodiac,
                candidate_wuge,
            )
            candidate.fortune_evaluation = fusion.to_dict()
            candidate.fortune_score = fusion.score
            candidate.fortune_status = fusion.status
            candidate.score = self.scorer.score(candidate)
            context.passed_candidates.append(candidate)
        context.filter_reasons = dict(reason_counter)

        ranking = self.ranker.rank(context.passed_candidates)
        context.top20 = ranking["top20"]
        context.top10 = ranking["top10"]
        context.top3 = ranking["top3"]
        context.diversity_status = ranking["diversity_status"]
        context.diversity_reason = ranking["reason"]
        response = self._to_response(context, structure_result, archetype_result, profile, baby_profile, fortune_context)
        response["top1"] = ranking["top1"].to_dict() if ranking["top1"] else None
        response["top1_status"] = ranking["top1_status"]
        response["rejected_candidates"] = [
            candidate.to_dict()
            for candidate in context.candidates
            if candidate.quality_guard and not candidate.quality_guard.get("passed")
        ]
        return response

    def _build_fortune_context(self, baby_profile: BabyProfile) -> FortuneContext:
        calendar = self.calendar_engine.normalize(baby_profile)
        true_solar = self.true_solar_time_engine.calculate(calendar.solar_datetime, baby_profile.birth_city)
        true_dt = true_solar.true_solar_time if true_solar.true_solar_time else calendar.solar_datetime
        four_pillars = self.four_pillars_engine.calculate(calendar.solar_datetime, true_dt)
        five_elements = self.five_elements_engine.analyze(four_pillars)
        zodiac = self.zodiac_engine.analyze(four_pillars, calendar.lunar_date)
        status = "COMPLETE" if true_solar.status == "COMPLETE" and four_pillars["status"] == "COMPLETE" else "PARTIAL"
        fusion_context = {
            "module_id": "fortune_context",
            "status": status,
            "score": None,
            "available_score": 0,
            "max_score": 10,
            "warnings": true_solar.warnings + four_pillars.get("warnings", []) + zodiac.get("warnings", []),
            "limitations": five_elements.get("limitations", []),
        }
        return FortuneContext(
            calendar=calendar.to_dict(),
            true_solar_time=true_solar.to_dict(),
            four_pillars=four_pillars,
            five_elements=five_elements,
            zodiac=zodiac,
            fusion=fusion_context,
            status=status,
        )

    @staticmethod
    def _baby_profile(payload: NamingInput | dict) -> BabyProfile:
        if isinstance(payload, NamingInput):
            return BabyProfile.from_dict(payload.__dict__)
        return BabyProfile.from_dict(payload)

    @staticmethod
    def _to_response(context: NamingContext, structure_result: dict, archetype_result: dict, profile: dict, baby_profile: BabyProfile, fortune_context: FortuneContext) -> dict:
        backup7 = [candidate for candidate in context.top10 if candidate not in context.top3][:7]
        qualified_count = len(context.top10)
        return {
            "ok": True,
            "input": context.naming_input.__dict__,
            "baby_profile": baby_profile.to_dict(),
            "profile": profile,
            "fortune_status": fortune_context.status,
            "fortune": fortune_context.to_dict(),
            "structure_result": {
                "primary_structure": structure_result["primary_structure"],
                "secondary_structures": structure_result["secondary_structures"],
            },
            "archetype_result": {
                "primary_archetype": archetype_result["primary_archetype"],
                "secondary_archetypes": archetype_result["secondary_archetypes"],
            },
            "catalog_counts": {"structures": 12, "archetypes": 12},
            "culture_evidence_count": len(context.culture_evidences),
            "culture_sources_returned": sorted({item.source_type for item in context.culture_evidences}),
            "char_pool_counts": {
                "first_pool": len(context.first_char_pool),
                "second_pool": len(context.second_char_pool),
            },
            "generated_candidates_count": len(context.candidates),
            "passed_candidates_count": len(context.passed_candidates),
            "filtered_count": context.filtered_count,
            "filter_reasons": context.filter_reasons,
            "diversity_status": context.diversity_status,
            "diversity_reason": context.diversity_reason,
            "top20": [candidate.to_dict() for candidate in context.top20],
            "top10": [candidate.to_dict() for candidate in context.top10],
            "top3": [candidate.to_dict() for candidate in context.top3],
            "backup7": [candidate.to_dict() for candidate in backup7],
            "result_status": "OK" if len(context.top3) == 3 and qualified_count >= 10 else "INSUFFICIENT_QUALIFIED_CANDIDATES",
            "qualified_count": qualified_count,
        }
