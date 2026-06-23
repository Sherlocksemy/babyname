from __future__ import annotations

from app.schemas.candidate import NameCandidate


class CandidateReconstructionValidator:
    def validate(self, candidate: NameCandidate, first_pool_chars: set[str], second_pool_chars: set[str]) -> dict:
        failures: list[str] = []
        steps: list[str] = []
        if candidate.was_example_name:
            failures.append("EXAMPLE_NAME_SOURCE")
        if candidate.was_golden_fixture:
            failures.append("GOLDEN_FIXTURE_SOURCE")
        if candidate.was_direct_name_candidate:
            failures.append("DIRECT_NAME_CANDIDATE_SOURCE")
        if candidate.given_name[0] not in first_pool_chars:
            failures.append("FIRST_CHAR_NOT_IN_POOL")
        else:
            steps.append("first char is reconstructable from first char pool")
        if candidate.given_name[1] not in second_pool_chars:
            failures.append("SECOND_CHAR_NOT_IN_POOL")
        else:
            steps.append("second char is reconstructable from second char pool")
        if not candidate.semantic_role_first or not candidate.semantic_role_second:
            failures.append("SEMANTIC_ROLES_MISSING")
        else:
            steps.append("semantic roles are present before scoring")
        if not candidate.combined_meaning or candidate.meaning_completeness < 72:
            failures.append("COMBINED_MEANING_NOT_ESTABLISHED")
        else:
            steps.append("combined meaning is established before ranking")
        if not candidate.culture_evidence_ids or not candidate.evidences:
            failures.append("CULTURE_EVIDENCE_MISSING")
        elif not self._evidence_supports_candidate(candidate):
            failures.append("CHARS_NOT_RECONSTRUCTABLE_FROM_EVIDENCE")
        else:
            steps.append("both chars can be selected from current culture evidence")
        if candidate.generation_mode not in {"semantic_culture_derivation", "direct_expression", "semantic_role_composition", "imagery_transformation"}:
            failures.append("UNSUPPORTED_GENERATION_MODE")
        else:
            steps.append("generation mode is rule derivation, not fixture lookup")
        return {
            "reconstructable": not failures,
            "source_independent": not any(failure in failures for failure in {"EXAMPLE_NAME_SOURCE", "GOLDEN_FIXTURE_SOURCE", "DIRECT_NAME_CANDIDATE_SOURCE"}),
            "reconstruction_steps": steps,
            "failures": failures,
        }

    @staticmethod
    def _evidence_supports_candidate(candidate: NameCandidate) -> bool:
        if any(all(char in evidence.original_text for char in candidate.given_name) for evidence in candidate.evidences):
            return True
        if candidate.generation_mode in {"semantic_role_composition", "imagery_transformation"}:
            evidence_text = "".join(evidence.original_text for evidence in candidate.evidences)
            return all(char in evidence_text for char in candidate.given_name)
        return False
