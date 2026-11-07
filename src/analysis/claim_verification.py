"""Deterministic retrieval and scoped evidence aggregation for incident claims.

Search results are candidates only. Passage relations become usable for an
aggregate verification result only after an explicit accepted assessment with
matching scope and independent-root provenance. This module does not call an
LLM, infer truth from search rank, or treat absent evidence as refutation.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RELATIONS = frozenset({
    "supports", "contradicts", "mentions", "quotes", "contextualizes",
    "rebuts", "ambiguous", "insufficient_context",
})
STATUSES = frozenset({
    "unverified", "supported_within_scope", "refuted_within_scope",
    "conflicting_evidence", "insufficient_evidence", "not_verifiable", "superseded",
})
_TOKEN = re.compile(r"[^\W_]+", re.UNICODE)
_STOPWORDS = frozenset({
    "і", "й", "та", "або", "що", "це", "у", "в", "на", "до", "з", "із", "за", "для", "про", "від", "по",
    "the", "a", "an", "and", "or", "that", "this", "in", "on", "at", "to", "of", "for", "from",
    "и", "а", "но", "что", "это", "в", "на", "к", "из", "за", "для", "о", "от", "по",
})
_COUNTER_CUES = (
    "спростування", "спростував", "спростувала", "спростували", "не було", "не було підтверджено",
    "не підтвердив", "не підтвердила", "не підтвердили", "відсутні", "відкидає", "відкинули",
    "уточнення", "уточнив", "уточнила", "виправлення", "виправив", "відкликав", "відкликала",
    "correction", "corrected", "retraction", "retracted", "disputed", "denied", "refuted", "debunked",
    "помилково", "фейк", "спростовали", "опровержение", "опроверг", "опровергла", "не было",
    "не подтвердил", "не подтвердила", "уточнение", "исправление", "отозвал", "ложно",
)


def _parse_utc(value: Any, field: str) -> tuple[datetime, str]:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a timezone-aware ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError(f"{field} must be UTC")
    parsed = parsed.astimezone(timezone.utc)
    text = parsed.isoformat(timespec="microseconds" if parsed.microsecond else "seconds").replace("+00:00", "Z")
    return parsed, text


def _tokens(text: str) -> list[tuple[str, int, int]]:
    return [
        (unicodedata.normalize("NFKC", match.group(0)).casefold(), match.start(), match.end())
        for match in _TOKEN.finditer(text)
        if unicodedata.normalize("NFKC", match.group(0)).casefold() not in _STOPWORDS
    ]


def _terms(text: str) -> list[str]:
    return [token for token, _, _ in _tokens(text)]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(*parts: str, prefix: str) -> str:
    payload = "\x1f".join(parts)
    return prefix + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _bm25(query_terms: list[str], document_terms: list[str], df: Counter, total_documents: int,
          average_length: float, *, k1: float = 1.2, b: float = 0.75) -> float:
    if not query_terms or not document_terms or total_documents == 0:
        return 0.0
    frequencies = Counter(document_terms)
    length = len(document_terms)
    score = 0.0
    for term, qtf in Counter(query_terms).items():
        tf = frequencies.get(term, 0)
        if not tf:
            continue
        doc_frequency = df.get(term, 0)
        idf = math.log(1.0 + (total_documents - doc_frequency + 0.5) / (doc_frequency + 0.5))
        denominator = tf + k1 * (1.0 - b + b * length / max(average_length, 1.0))
        score += idf * (tf * (k1 + 1.0) / denominator) * (1.0 + math.log(qtf))
    return score


def _claim_query_variants(claim: dict) -> list[str]:
    statement = str(claim.get("statement") or "").strip()
    variants = [statement]
    for value in claim.get("query_variants") or []:
        if isinstance(value, str) and value.strip():
            variants.append(value.strip())
    return list(dict.fromkeys(variants))


def retrieve_evidence_candidates(
    claim: dict,
    passages: list[dict],
    *,
    as_of_utc: str,
    top_k: int = 20,
    counterevidence_terms: tuple[str, ...] = _COUNTER_CUES,
) -> dict:
    """Search claim and rebuttal/correction directions using local BM25.

    ``captured_at_utc`` is the knowledge-time cutoff field. The returned
    candidates are never labeled as supporting or contradicting evidence.
    At most one candidate per explicitly supplied lineage family is retained
    per search direction; unlinked candidates remain separate and unknown.
    """
    claim_id = str(claim.get("claim_id") or "").strip()
    if not claim_id or not str(claim.get("statement") or "").strip():
        raise ValueError("claim_id and non-empty statement are required")
    if type(top_k) is not int or top_k < 1:
        raise ValueError("top_k must be a positive integer")
    as_of, as_of_text = _parse_utc(as_of_utc, "as_of_utc")
    variants = _claim_query_variants(claim)
    if not variants:
        raise ValueError("at least one claim query is required")

    future_count = 0
    passages_by_id = {}
    eligible = []
    snapshot_rows = []
    for raw in passages:
        passage_id = str(raw.get("passage_id") or "").strip()
        source_id = str(raw.get("source_id") or "").strip()
        text = raw.get("text")
        if not passage_id or not source_id or not isinstance(text, str) or not text.strip():
            raise ValueError("each passage requires passage_id, source_id, and non-empty text")
        if passage_id in passages_by_id:
            raise ValueError(f"duplicate passage_id: {passage_id}")
        artifact_offset = raw.get("artifact_start_offset", 0)
        if type(artifact_offset) is not int or artifact_offset < 0:
            raise ValueError(f"{passage_id}.artifact_start_offset must be a non-negative integer")
        captured, captured_text = _parse_utc(raw.get("captured_at_utc"), f"{passage_id}.captured_at_utc")
        passages_by_id[passage_id] = raw
        snapshot_rows.append({
            "passage_id": passage_id,
            "source_id": source_id,
            "artifact_id": raw.get("artifact_id"),
            "captured_at_utc": captured_text,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "artifact_start_offset": artifact_offset,
            "lineage_family_id": raw.get("lineage_family_id"),
            "independent_root_id": raw.get("independent_root_id"),
        })
        if captured > as_of:
            future_count += 1
            continue
        doc_tokens = _tokens(text)
        eligible.append({**raw, "passage_id": passage_id, "source_id": source_id,
                         "captured_at_utc": captured_text, "_tokens": doc_tokens,
                         "_token_values": [token for token, _, _ in doc_tokens]})

    total = len(eligible)
    snapshot_rows.sort(key=lambda row: row["passage_id"])
    input_snapshot_sha256 = hashlib.sha256(_canonical(snapshot_rows).encode("utf-8")).hexdigest()
    document_frequency = Counter()
    for row in eligible:
        document_frequency.update(set(row["_token_values"]))
    average_length = sum(len(row["_token_values"]) for row in eligible) / total if total else 0.0

    direction_queries = {
        "claim_terms": [_terms(variant) for variant in variants],
        "counterevidence_terms": [_terms(variant + " " + " ".join(counterevidence_terms)) for variant in variants],
    }
    counter_cue_tokens = set(term for cue in counterevidence_terms for term in _terms(cue))
    claim_query_tokens = set(term for variant in variants for term in _terms(variant))
    scores_by_direction: dict[str, list[tuple[float, dict, set[str]]]] = {}
    unique_roots_skipped = Counter()
    counter_no_claim_overlap_count = 0
    counter_no_cue_count = 0
    for direction, queries in direction_queries.items():
        ranked = []
        all_query_terms = set(term for query in queries for term in query)
        for row in eligible:
            if direction == "counterevidence_terms":
                document_terms = set(row["_token_values"])
                if not counter_cue_tokens & document_terms:
                    counter_no_cue_count += 1
                    continue
                if not claim_query_tokens & document_terms:
                    counter_no_claim_overlap_count += 1
                    continue
            score = max((_bm25(query, row["_token_values"], document_frequency, total, average_length) for query in queries), default=0.0)
            if score <= 0:
                continue
            ranked.append((score, row, all_query_terms))
        ranked.sort(key=lambda item: (-item[0], item[1]["passage_id"]))
        selected = []
        seen_known_families = set()
        for item in ranked:
            row = item[1]
            family = row.get("lineage_family_id")
            if family:
                if family in seen_known_families:
                    unique_roots_skipped[direction] += 1
                    continue
                seen_known_families.add(family)
            selected.append(item)
            if len(selected) >= top_k:
                break
        scores_by_direction[direction] = selected

    merged: dict[str, dict] = {}
    for direction, items in scores_by_direction.items():
        for score, row, query_terms in items:
            passage_id = row["passage_id"]
            tokens = row["_tokens"]
            matching = [(start, end) for token, start, end in tokens if token in query_terms]
            if not matching:
                continue
            start = min(a for a, _ in matching)
            end = max(b for _, b in matching)
            # Keep citations concise while preserving exact source offsets.
            if end - start > 500:
                first_start, first_end = matching[0]
                start, end = max(0, first_start - 120), min(len(row["text"]), first_end + 240)
            quote = row["text"][start:end]
            passage_text_hash = hashlib.sha256(row["text"].encode("utf-8")).hexdigest()
            candidate_id = _digest(
                claim_id, passage_id, passage_text_hash, str(row.get("artifact_start_offset", 0)),
                prefix="candidate:",
            )
            candidate = merged.setdefault(passage_id, {
                "candidate_id": candidate_id,
                "claim_id": claim_id,
                "passage_id": passage_id,
                "artifact_id": row.get("artifact_id"),
                "source_id": row["source_id"],
                "captured_at_utc": row["captured_at_utc"],
                "lineage_family_id": row.get("lineage_family_id"),
                "lineage_status": "known_dependency_family" if row.get("lineage_family_id") else "unknown",
                "independent_root_id": row.get("independent_root_id"),
                "search_directions": [],
                "direction_scores": {},
                "quote": quote,
                "start_offset": start,
                "end_offset": end,
                "artifact_start_offset": row.get("artifact_start_offset", 0) + start,
                "offset_unit": "unicode_codepoint",
                "relation": "unassessed",
                "verification_status": "unverified",
                "limitations": [
                    "Lexical retrieval identifies a candidate passage; rank is not evidence of support or truth.",
                    "No independent root is inferred from source identity or absence of a detected copy.",
                ],
            })
            if direction not in candidate["search_directions"]:
                candidate["search_directions"].append(direction)
            candidate["direction_scores"][direction] = round(score, 8)
            # If both query tracks hit, use the shorter exact quote while keeping
            # all matching spans from each route in the search receipt.
            if len(quote) < len(candidate["quote"]):
                candidate["quote"] = quote
                candidate["start_offset"] = start
                candidate["end_offset"] = end
                candidate["artifact_start_offset"] = row.get("artifact_start_offset", 0) + start

    candidates = sorted(merged.values(), key=lambda row: (-max(row["direction_scores"].values()), row["passage_id"]))
    for candidate in candidates:
        candidate["search_directions"].sort()
    known_families = {row["lineage_family_id"] for row in candidates if row["lineage_family_id"]}
    return {
        "schema_version": "1.0",
        "claim_id": claim_id,
        "as_of_utc": as_of_text,
        "candidates": candidates,
        "search_receipt": {
            "status": "candidates_found" if candidates else "no_candidates_found",
            "directions": list(direction_queries),
            "query_terms": {direction: [sorted(set(query)) for query in queries]
                            for direction, queries in direction_queries.items()},
            "query_variant_count": len(variants),
            "input_passage_count": len(passages),
            "eligible_passage_count": total,
            "excluded_future_count": future_count,
            "counterevidence_no_claim_overlap_count": counter_no_claim_overlap_count,
            "counterevidence_no_cue_count": counter_no_cue_count,
            "candidate_count": len(candidates),
            "input_snapshot_sha256": input_snapshot_sha256,
            "known_dependency_family_count": len(known_families),
            "lineage_unknown_candidate_count": sum(row["lineage_status"] == "unknown" for row in candidates),
            "redundant_family_candidates_skipped": dict(unique_roots_skipped),
            "retriever": "deterministic_local_bm25_v1",
            "top_k_per_direction": top_k,
            "bm25_parameters": {"k1": 1.2, "b": 0.75},
            "counterevidence_cue_terms": sorted(counter_cue_tokens),
            "limitations": [
                "Lexical retrieval can miss paraphrases and can retrieve irrelevant passages.",
                "The source corpus is the supplied passage set; this is not a claim that all relevant sources were searched.",
                "Separate query directions do not encode passage stance or claim verification.",
                "Lineage-family deduplication affects candidate ranking only; it does not prove independence.",
            ],
        },
    }


def create_evidence_assessment(
    claim: dict,
    candidate: dict,
    passage: dict,
    *,
    relation: str,
    decision: str,
    scope: dict,
    assessed_at_utc: str,
    assessor_id: str,
    acceptance_basis: str | None = None,
    validated_rule_id: str | None = None,
    asserted_values: dict | None = None,
    independent_root_id: str | None = None,
    independence_status: str = "unknown",
    limitations: list[str] | None = None,
) -> dict:
    """Create a passage-level assessment after validating exact citation spans.

    ``decision=accepted`` is reserved for explicit human adjudication or a
    documented validated rule. Model-only labels remain candidates.
    """
    claim_id = str(claim.get("claim_id") or "")
    if candidate.get("claim_id") != claim_id:
        raise ValueError("candidate claim_id does not match the claim")
    if candidate.get("passage_id") != passage.get("passage_id"):
        raise ValueError("candidate passage_id does not match passage")
    start, end = candidate.get("start_offset"), candidate.get("end_offset")
    text = passage.get("text")
    quote = candidate.get("quote")
    if not isinstance(start, int) or not isinstance(end, int) or not isinstance(text, str) or not isinstance(quote, str):
        raise ValueError("candidate requires exact integer citation offsets and quote")
    if start < 0 or end <= start or end > len(text) or text[start:end] != quote:
        raise ValueError("exact citation span does not match the original passage text")
    if relation not in RELATIONS:
        raise ValueError(f"unsupported evidence relation: {relation}")
    if decision not in {"candidate", "accepted"}:
        raise ValueError("decision must be candidate or accepted")
    if not isinstance(scope, dict) or not scope:
        raise ValueError("assessment scope must be a non-empty object")
    if decision == "accepted":
        if acceptance_basis not in {"human_adjudication", "validated_rule"}:
            raise ValueError("accepted assessments require human_adjudication or validated_rule basis")
        if acceptance_basis == "validated_rule" and not validated_rule_id:
            raise ValueError("validated_rule acceptance requires validated_rule_id")
        if not assessor_id:
            raise ValueError("accepted assessments require assessor_id")
    if independence_status not in {"unknown", "candidate", "confirmed_independent"}:
        raise ValueError("unsupported independence_status")
    if independence_status == "confirmed_independent" and not independent_root_id:
        raise ValueError("confirmed independent status requires independent_root_id")
    assessed_dt, assessed_at = _parse_utc(assessed_at_utc, "assessed_at_utc")
    captured_dt, _ = _parse_utc(passage.get("captured_at_utc"), "passage.captured_at_utc")
    if captured_dt > assessed_dt:
        raise ValueError("assessment time cannot precede evidence capture time")

    final_relation = relation
    final_decision = decision
    reasons = []
    expected_values = claim.get("key_values") or {}
    asserted_values = asserted_values or {}
    if final_relation == "supports":
        for key, expected in expected_values.items():
            if key not in asserted_values:
                final_relation = "ambiguous"
                final_decision = "candidate"
                reasons.append(f"missing_asserted_value:{key}")
                continue
            actual = asserted_values[key]
            if _canonical(actual) != _canonical(expected):
                final_relation = "ambiguous"
                final_decision = "candidate"
                reasons.append(f"value_mismatch:{key}")
    scope_matches = _canonical(scope) == _canonical(claim.get("scope"))
    if not scope_matches and final_decision == "accepted":
        final_decision = "candidate"
        reasons.append("scope_mismatch")
    root_id = independent_root_id or passage.get("independent_root_id")
    assessment = {
        "schema_version": "1.0",
        "claim_id": claim_id,
        "candidate_id": candidate["candidate_id"],
        "evidence_id": candidate["passage_id"],
        "source_id": candidate["source_id"],
        "relation": final_relation,
        "decision": final_decision,
        "scope": scope,
        "scope_matches_claim": scope_matches,
        "asserted_values": asserted_values,
        "independent_root_id": root_id,
        "independence_status": independence_status if root_id else "unknown",
        "assessment_source": acceptance_basis if final_decision == "accepted" else "candidate_only",
        "assessor_id": assessor_id,
        "validated_rule_id": validated_rule_id,
        "assessed_at_utc": assessed_at,
        "citation": {
            "passage_id": candidate["passage_id"],
            "start_offset": start,
            "end_offset": end,
            "quote": quote,
            "offset_unit": "unicode_codepoint",
        },
        "reasons": reasons,
        "limitations": list(limitations or []) + [
            "A passage-level relation is not by itself proof that the real-world claim is true or false.",
            "A declared root ID is provenance input; this function does not establish the root's independence.",
        ],
    }
    assessment["assessment_id"] = _digest(
        claim_id, candidate["candidate_id"], _canonical(assessment), prefix="assessment:"
    )
    return assessment


def aggregate_verification(
    claim: dict,
    assessments: list[dict],
    *,
    as_of_utc: str,
    search_complete: bool,
    minimum_independent_roots: int = 2,
    supersedes_result_id: str | None = None,
) -> dict:
    """Produce an as-of claim status from accepted, scope-matched assessments.

    Independent-root counts use only explicit ``independent_root_id`` values.
    Repeated passages from a common root do not increase the count. Unknown
    roots never become independent by default.
    """
    claim_id = str(claim.get("claim_id") or "").strip()
    if not claim_id or not isinstance(claim.get("scope"), dict) or not claim["scope"]:
        raise ValueError("claim_id and non-empty claim scope are required")
    if type(search_complete) is not bool:
        raise ValueError("search_complete must be boolean")
    if type(minimum_independent_roots) is not int or minimum_independent_roots < 1:
        raise ValueError("minimum_independent_roots must be a positive integer")
    assessment_ids = [row.get("assessment_id") for row in assessments
                      if isinstance(row.get("assessment_id"), str) and row["assessment_id"].strip()]
    if len(assessment_ids) != len(set(assessment_ids)):
        raise ValueError("duplicate assessment_id")
    as_of, as_of_text = _parse_utc(as_of_utc, "as_of_utc")
    if claim.get("observability") == "not_verifiable":
        status = "not_verifiable"
        usable = []
        excluded = [
            {"assessment_id": row.get("assessment_id"), "reason": "claim_not_verifiable"}
            for row in assessments
        ]
    else:
        usable = []
        excluded = []
        for assessment in assessments:
            if not isinstance(assessment.get("assessment_id"), str) or not assessment["assessment_id"].strip():
                excluded.append({"assessment_id": assessment.get("assessment_id"), "reason": "missing_assessment_id"})
                continue
            try:
                assessed, _ = _parse_utc(assessment.get("assessed_at_utc"), "assessment.assessed_at_utc")
            except ValueError:
                excluded.append({"assessment_id": assessment.get("assessment_id"), "reason": "invalid_assessment_time"})
                continue
            reason = None
            if assessment.get("claim_id") != claim_id:
                reason = "claim_mismatch"
            elif assessed > as_of:
                reason = "assessment_after_as_of"
            elif assessment.get("decision") != "accepted":
                reason = "candidate_only"
            elif assessment.get("assessment_source") not in {"human_adjudication", "validated_rule"}:
                reason = "missing_acceptance_provenance"
            elif not assessment.get("assessor_id"):
                reason = "missing_assessor_id"
            elif assessment.get("assessment_source") == "validated_rule" and not assessment.get("validated_rule_id"):
                reason = "missing_validated_rule_id"
            elif assessment.get("relation") not in {"supports", "contradicts"}:
                reason = "non_verdict_relation"
            elif assessment.get("relation") == "supports" and _support_value_problem(claim, assessment):
                reason = _support_value_problem(claim, assessment)
            elif _canonical(assessment.get("scope")) != _canonical(claim["scope"]):
                reason = "scope_mismatch"
            elif assessment.get("scope_matches_claim") is False:
                reason = "scope_mismatch"
            elif not assessment.get("evidence_id"):
                reason = "missing_evidence_id"
            elif not _valid_citation(assessment):
                reason = "missing_or_invalid_citation"
            if reason:
                excluded.append({"assessment_id": assessment.get("assessment_id"), "reason": reason})
            else:
                usable.append(assessment)
        support = [row for row in usable if row["relation"] == "supports"]
        contradict = [row for row in usable if row["relation"] == "contradicts"]
        support_roots = {row["independent_root_id"] for row in support
                         if row.get("independence_status") == "confirmed_independent" and row.get("independent_root_id")}
        contradict_roots = {row["independent_root_id"] for row in contradict
                            if row.get("independence_status") == "confirmed_independent" and row.get("independent_root_id")}
        shared_roots = support_roots & contradict_roots
        if support_roots and contradict_roots:
            status = "conflicting_evidence"
        elif len(support_roots) >= minimum_independent_roots:
            status = "supported_within_scope"
        elif len(contradict_roots) >= minimum_independent_roots:
            status = "refuted_within_scope"
        elif not search_complete:
            status = "unverified"
        else:
            status = "insufficient_evidence"

    support_rows = [row for row in usable if row["relation"] == "supports"] if status != "not_verifiable" else []
    contradict_rows = [row for row in usable if row["relation"] == "contradicts"] if status != "not_verifiable" else []
    support_ids = sorted({row["evidence_id"] for row in support_rows})
    contradict_ids = sorted({row["evidence_id"] for row in contradict_rows})
    support_roots = sorted({row["independent_root_id"] for row in support_rows
                            if row.get("independence_status") == "confirmed_independent" and row.get("independent_root_id")})
    contradict_roots = sorted({row["independent_root_id"] for row in contradict_rows
                               if row.get("independence_status") == "confirmed_independent" and row.get("independent_root_id")})
    assessments_used = sorted(row["assessment_id"] for row in usable if row.get("assessment_id"))
    exclusion_by_id = {row.get("assessment_id"): row["reason"] for row in excluded}
    used_id_set = set(assessments_used)
    assessment_provenance = [
        _assessment_audit_record(
            row,
            row.get("assessment_id") in used_id_set,
            exclusion_by_id.get(row.get("assessment_id")),
        )
        for row in sorted(assessments, key=lambda item: (str(item.get("assessment_id") or ""), _canonical(item)))
    ]
    material = _canonical({
        "claim_id": claim_id,
        "claim_statement": claim.get("statement"),
        "scope": claim["scope"],
        "key_values": claim.get("key_values", {}),
        "as_of_utc": as_of_text,
        "status": status,
        "assessment_ids": sorted(assessments_used),
        "assessment_provenance": assessment_provenance,
        "excluded_assessment_ids": sorted(row["assessment_id"] for row in excluded if row.get("assessment_id")),
        "minimum_independent_roots": minimum_independent_roots,
        "search_complete": bool(search_complete),
        "observability": claim.get("observability"),
        "supersedes": supersedes_result_id,
    })
    result_id = "verification:" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return {
        "schema_version": "1.0",
        "result_id": result_id,
        "claim_id": claim_id,
        "scope": claim["scope"],
        "as_of_utc": as_of_text,
        "status": status,
        "search_complete": bool(search_complete),
        "supporting_evidence_ids": support_ids,
        "contradicting_evidence_ids": contradict_ids,
        "supporting_root_count": len(support_roots),
        "contradicting_root_count": len(contradict_roots),
        "shared_root_ids": sorted(set(support_roots) & set(contradict_roots)),
        "independent_support_roots": len(support_roots),
        "independent_contradiction_roots": len(contradict_roots),
        "minimum_independent_roots": minimum_independent_roots,
        "assessment_ids": assessments_used,
        "assessment_provenance": assessment_provenance,
        "excluded_assessments": excluded,
        "excluded_assessment_ids": sorted(row["assessment_id"] for row in excluded if row.get("assessment_id")),
        "supersedes": supersedes_result_id,
        "rationale": _status_rationale(
            status, len(support_roots), len(contradict_roots), minimum_independent_roots,
            search_complete, len(set(support_roots) & set(contradict_roots)),
        ),
        "limitations": [
            "This result is limited to the exact claim scope and supplied evidence corpus.",
            "Retrieval rank, publication volume, and model agreement are not evidence of truth.",
            "Only explicitly supplied independent_root_id values count toward the root threshold; their independence is not established here.",
            "insufficient_evidence and unverified are not refutations.",
        ],
    }


def append_verification_result(
    ledger: Any,
    result: dict,
    *,
    producer: str,
    run_id: str,
) -> dict:
    """Append a projection to the existing immutable EvidenceLedger.

    The ledger checks that the claim and all evidence IDs already exist. The
    serialized scope is kept as canonical JSON because the ledger's current
    contract stores scope as text.
    """
    if result.get("status") not in STATUSES:
        raise ValueError("unsupported verification result status")
    if not result.get("result_id") or not result.get("claim_id"):
        raise ValueError("verification result requires result_id and claim_id")
    rationale_payload = {
        "summary": result.get("rationale"),
        "assessment_ids": result.get("assessment_ids", []),
        "assessment_provenance": result.get("assessment_provenance", []),
        "excluded_assessment_ids": result.get("excluded_assessment_ids", []),
        "excluded_assessments": result.get("excluded_assessments", []),
        "verification_parameters": {
            "as_of_utc": result.get("as_of_utc"),
            "search_complete": result.get("search_complete"),
            "minimum_independent_roots": result.get("minimum_independent_roots"),
            "status": result.get("status"),
            "supporting_root_count": result.get("supporting_root_count"),
            "contradicting_root_count": result.get("contradicting_root_count"),
            "shared_root_ids": result.get("shared_root_ids", []),
        },
    }
    existing = ledger.get_record(result["result_id"])
    return ledger.add_verification_result(
        result["result_id"],
        claim_id=result["claim_id"],
        scope=_canonical(result["scope"]),
        as_of=result["as_of_utc"],
        status=result["status"],
        supporting_evidence_ids=result.get("supporting_evidence_ids", []),
        contradicting_evidence_ids=result.get("contradicting_evidence_ids", []),
        rationale=json.dumps(rationale_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        supersedes=result.get("supersedes"),
        producer=producer,
        run_id=run_id,
        limitations=result.get("limitations", []),
        created_at=existing["created_at"] if existing else None,
    )


def _status_rationale(
    status: str,
    support_count: int,
    contradict_count: int,
    minimum: int,
    search_complete: bool,
    shared_root_count: int = 0,
) -> str:
    if status == "supported_within_scope":
        return f"Accepted, scope-matched support from {support_count} explicit roots meets threshold {minimum}; no independent contradiction root was accepted."
    if status == "refuted_within_scope":
        return f"Accepted, scope-matched contradictory evidence from {contradict_count} explicit roots meets threshold {minimum}; no independent support root was accepted."
    if status == "conflicting_evidence":
        return (
            f"Accepted, scope-matched support and contradiction have explicit roots "
            f"({support_count} and {contradict_count}); {shared_root_count} root(s) occur on both sides."
        )
    if status == "not_verifiable":
        return "The claim is explicitly marked outside the observable scope of this workflow."
    if not search_complete:
        return "Evidence search is incomplete; no final truth assessment is available."
    return "The supplied evidence does not meet the explicit independent-root threshold; absence of evidence is not refutation."


def _support_value_problem(claim: dict, assessment: dict) -> str | None:
    """Return why an asserted support relation fails exact claim value checks."""
    expected_values = claim.get("key_values") or {}
    asserted_values = assessment.get("asserted_values") or {}
    for key, expected in expected_values.items():
        if key not in asserted_values:
            return f"missing_asserted_value:{key}"
        if _canonical(asserted_values[key]) != _canonical(expected):
            return f"value_mismatch:{key}"
    return None


def _assessment_audit_record(assessment: dict, included: bool, exclusion_reason: str | None) -> dict:
    fields = (
        "assessment_id", "claim_id", "candidate_id", "evidence_id", "source_id", "relation", "decision",
        "scope", "scope_matches_claim", "asserted_values", "independent_root_id", "independence_status",
        "assessment_source", "assessor_id", "validated_rule_id", "assessed_at_utc", "citation", "reasons",
    )
    record = {field: assessment[field] for field in fields if field in assessment}
    record["included_in_verification"] = included
    record["exclusion_reason"] = exclusion_reason
    return record


def export_verification_package(
    search_result: dict,
    assessments: list[dict],
    verification_result: dict,
    output_dir: str | Path,
) -> dict[str, Path]:
    """Write deterministic JSONL exports, claim matrix, and unresolved queue."""
    claim_id = str(verification_result.get("claim_id") or "")
    if not claim_id or search_result.get("claim_id") != claim_id:
        raise ValueError("search result and verification result must share a claim_id")
    if not isinstance(search_result.get("candidates"), list):
        raise ValueError("search_result.candidates must be a list")
    if not isinstance(search_result.get("search_receipt"), dict):
        raise ValueError("search_result.search_receipt must be an object")
    candidates = search_result["candidates"]
    candidate_ids = {row.get("candidate_id") for row in candidates}
    included_candidate_ids = {
        row.get("candidate_id") for row in verification_result.get("assessment_provenance", [])
        if row.get("included_in_verification") and row.get("candidate_id")
    }
    unassessed_candidate_ids = sorted(candidate_ids - included_candidate_ids)
    unresolved_statuses = {
        "unverified", "insufficient_evidence", "conflicting_evidence", "not_verifiable", "superseded",
    }
    queue_rows = []
    if verification_result.get("status") in unresolved_statuses or unassessed_candidate_ids:
        reasons = []
        if verification_result.get("status") in unresolved_statuses:
            reasons.append(f"verification_status:{verification_result.get('status')}")
        if unassessed_candidate_ids:
            reasons.append("candidate_passages_without_accepted_assessment")
        queue_rows.append({
            "schema_version": "1.0",
            "claim_id": claim_id,
            "as_of_utc": verification_result.get("as_of_utc"),
            "verification_status": verification_result.get("status"),
            "candidate_ids_to_review_or_retrieve": unassessed_candidate_ids,
            "reason_codes": reasons,
            "targeted_next_steps": _unresolved_next_steps(verification_result),
            "search_snapshot_sha256": (search_result.get("search_receipt") or {}).get("input_snapshot_sha256"),
        })

    scope_text = _markdown_cell(_canonical(verification_result.get("scope")))
    support_text = _markdown_cell(", ".join(verification_result.get("supporting_evidence_ids", [])) or "—")
    contradict_text = _markdown_cell(", ".join(verification_result.get("contradicting_evidence_ids", [])) or "—")
    assessment_text = _markdown_cell(", ".join(verification_result.get("assessment_ids", [])) or "—")
    matrix = "\n".join([
        "# Матриця перевірки тверджень",
        "",
        "Експорт містить статус у межах заданого scope та доступного корпусу; це не оцінка всіх можливих джерел.",
        "",
        "| Claim ID | Статус | Scope | As of (UTC) | Докази за | Докази проти | Assessments | Пояснення |",
        "|---|---|---|---|---|---|---|---|",
        "| " + " | ".join([
            _markdown_cell(claim_id),
            _markdown_cell(str(verification_result.get("status", "unknown"))),
            scope_text,
            _markdown_cell(str(verification_result.get("as_of_utc", ""))),
            support_text,
            contradict_text,
            assessment_text,
            _markdown_cell(str(verification_result.get("rationale", ""))),
        ]) + " |",
        "",
        f"Пошукових кандидатів: {len(candidates)}. Прийнятих assessment: {len(verification_result.get('assessment_ids', []))}. Відкритих retrieval-запитів: {len(queue_rows)}.",
    ]) + "\n"

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    payloads = {
        "candidates": _jsonl(candidates),
        "assessments": _jsonl(assessments),
        "results": _jsonl([verification_result]),
        "search_receipt": json.dumps(search_result["search_receipt"], ensure_ascii=False,
                                      sort_keys=True, separators=(",", ":")) + "\n",
        "claim_matrix": matrix,
        "unresolved_queue": _jsonl(queue_rows),
    }
    filenames = {
        "candidates": "evidence_candidates.jsonl",
        "assessments": "evidence_assessments.jsonl",
        "results": "verification_results.jsonl",
        "search_receipt": "search_receipt.json",
        "claim_matrix": "claim_matrix.md",
        "unresolved_queue": "unresolved_retrieval_queue.jsonl",
    }
    paths = {name: directory / filename for name, filename in filenames.items()}
    if len({path.resolve() for path in paths.values()}) != len(paths):
        raise ValueError("verification package output paths collide")
    for name, path in paths.items():
        _write_text_atomic(path, payloads[name])
    return paths


def _jsonl(rows: list[dict]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)


def _markdown_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def _write_text_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _unresolved_next_steps(result: dict) -> list[str]:
    status = result.get("status")
    if status == "conflicting_evidence":
        return ["Знайти незалежні першоджерела для протилежних версій.", "Перевірити чи одна з версій була уточнена або відкликана."]
    if status in {"unverified", "insufficient_evidence"}:
        return ["Розширити пошук на первинні документи, офіційні уточнення та незалежні повідомлення.", "Перевірити пропущені джерельні сім'ї та часові зрізи."]
    if status == "not_verifiable":
        return ["Зафіксувати, які додаткові непублічні або поза корпусом докази були б потрібні; не трактувати відсутність даних як спростування."]
    return ["Повторно оцінити нові матеріали окремим версійованим запуском."]


def _valid_citation(assessment: dict) -> bool:
    citation = assessment.get("citation")
    if not isinstance(citation, dict):
        return False
    start, end = citation.get("start_offset"), citation.get("end_offset")
    quote = citation.get("quote")
    return (
        citation.get("passage_id") == assessment.get("evidence_id")
        and type(start) is int and type(end) is int and start >= 0 and end > start
        and isinstance(quote, str) and bool(quote)
    )
