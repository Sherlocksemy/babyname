from __future__ import annotations

from collections import Counter

from app.engines.archetype_engine import ArchetypeEngine
from app.engines.candidate_quality_scorer import CandidateQualityScorer
from app.engines.candidate_reconstruction_validator import CandidateReconstructionValidator
from app.engines.char_pool_builder import CharPoolBuilder
from app.engines.culture_retriever import CultureRetriever
from app.engines.name_composer import NameComposer
from app.engines.profile_specificity_engine import ProfileSpecificityEngine
from app.engines.quality_guard import QualityGuard
from app.engines.ranking_engine import RankingEngine
from app.engines.surname_fit_evaluator import SurnameFitEvaluator
from app.engines.structure_engine import StructureEngine
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

    def run(self, payload: NamingInput | dict) -> dict:
        naming_input = payload if isinstance(payload, NamingInput) else NamingInput.from_dict(payload)
        errors = naming_input.validate()
        if errors:
            return {"ok": False, "errors": errors}

        context = NamingContext(naming_input=naming_input)
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
        pools = self.char_pool_builder.build(naming_input, context.structures, context.archetypes, context.culture_evidences)
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
            if candidate.profile_specificity_score < 70:
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
            candidate.score = self.scorer.score(candidate)
            context.passed_candidates.append(candidate)
        context.filter_reasons = dict(reason_counter)

        ranking = self.ranker.rank(context.passed_candidates)
        context.top20 = ranking["top20"]
        context.top10 = ranking["top10"]
        context.top3 = ranking["top3"]
        context.diversity_status = ranking["diversity_status"]
        context.diversity_reason = ranking["reason"]
        response = self._to_response(context, structure_result, archetype_result, profile)
        response["top1"] = ranking["top1"].to_dict() if ranking["top1"] else None
        response["top1_status"] = ranking["top1_status"]
        response["rejected_candidates"] = [
            candidate.to_dict()
            for candidate in context.candidates
            if candidate.quality_guard and not candidate.quality_guard.get("passed")
        ]
        return response

    @staticmethod
    def _to_response(context: NamingContext, structure_result: dict, archetype_result: dict, profile: dict) -> dict:
        return {
            "ok": True,
            "input": context.naming_input.__dict__,
            "profile": profile,
            "fortune_status": context.fortune_status,
            "fortune": {
                "fortune_status": context.fortune_status,
                "reason": context.fortune_reason,
            },
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
        }
