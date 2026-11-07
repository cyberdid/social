from __future__ import annotations

import json

import pytest

from src.analysis.claim_verification import (
    append_verification_result,
    aggregate_verification,
    create_evidence_assessment,
    export_verification_package,
    retrieve_evidence_candidates,
)
from src.evidence_ledger import EvidenceLedger


def claim(**overrides):
    result = {
        "claim_id": "claim_1",
        "statement": "40 people were held in the building",
        "scope": {"place_id": "building_1", "event_date": "2026-11-02"},
        "key_values": {"count": {"value": 40, "operator": "eq"}},
        "query_variants": ["40 people held building"],
    }
    result.update(overrides)
    return result


def passage(passage_id, text, *, source="source_1", captured="2026-11-02T20:00:00Z", root=None, family=None, offset=0):
    return {
        "passage_id": passage_id,
        "artifact_id": f"artifact_{passage_id}",
        "source_id": source,
        "captured_at_utc": captured,
        "text": text,
        "artifact_start_offset": offset,
        "independent_root_id": root,
        "lineage_family_id": family,
    }


def retrieve(c, passages, as_of="2026-11-05T00:00:00Z"):
    return retrieve_evidence_candidates(c, passages, as_of_utc=as_of, top_k=10)


def accepted(assessment_id, relation, evidence_id, root_id, assessed_at, *, c=None, scope=None, correction=False):
    c = c or claim()
    return {
        "assessment_id": assessment_id,
        "claim_id": c["claim_id"],
        "relation": relation,
        "decision": "accepted",
        "assessment_source": "human_adjudication",
        "assessor_id": "reviewer:test",
        "scope": scope if scope is not None else c["scope"],
        "scope_matches_claim": scope is None or scope == c["scope"],
        "evidence_id": evidence_id,
        "citation": {"passage_id": evidence_id, "start_offset": 0, "end_offset": 1, "quote": "x"},
        "independent_root_id": root_id,
        "independence_status": "confirmed_independent",
        "asserted_values": c.get("key_values", {}),
        "assessed_at_utc": assessed_at,
        "is_correction": correction,
    }


def test_retrieval_runs_claim_and_correction_queries_and_keeps_candidates_unassessed():
    exact = passage("p1", "Officials held 40 people in the building.")
    correction = passage("p2", "Correction: officials said no people were held in the building.", source="source_2")
    future = passage("p3", "Officials held 40 people in the building.", captured="2026-11-06T00:00:00Z")
    result = retrieve(claim(), [exact, correction, future])

    assert result["search_receipt"]["directions"] == ["claim_terms", "counterevidence_terms"]
    assert result["search_receipt"]["excluded_future_count"] == 1
    hits = {hit["passage_id"]: hit for hit in result["candidates"]}
    assert {"p1", "p2"} <= set(hits)
    assert "claim_terms" in hits["p1"]["search_directions"]
    assert "counterevidence_terms" in hits["p2"]["search_directions"]
    assert "counterevidence_terms" not in hits["p1"]["search_directions"]
    assert all(hit["relation"] == "unassessed" for hit in result["candidates"])
    assert all(hit["verification_status"] == "unverified" for hit in result["candidates"])


def test_counterevidence_candidate_must_overlap_claim_terms_and_correction_cue():
    unrelated_correction = passage("unrelated", "Correction: the court cancelled an unrelated hearing.")
    result = retrieve(claim(), [unrelated_correction])
    assert result["candidates"] == []
    assert result["search_receipt"]["counterevidence_no_claim_overlap_count"] == 1


def test_candidate_citation_offsets_point_to_exact_original_text():
    source_text = "prefix material. Officials held 40 people in the building. trailing material."
    p = passage("p1", source_text, offset=125)
    hit = next(hit for hit in retrieve(claim(), [p])["candidates"] if hit["passage_id"] == "p1")
    assert p["text"][hit["start_offset"]:hit["end_offset"]] == hit["quote"]
    assert hit["artifact_start_offset"] == 125 + hit["start_offset"]


def test_future_only_material_is_not_used_in_as_of_retrieval():
    p = passage("future", "Officials held 40 people in the building.", captured="2026-11-06T00:00:00Z")
    result = retrieve(claim(), [p], as_of="2026-11-05T00:00:00Z")
    assert result["candidates"] == []
    assert result["search_receipt"]["status"] == "no_candidates_found"


def test_retrieval_keeps_one_candidate_per_explicit_lineage_family_per_direction():
    first = passage("p1", "Officials held 40 people in the building.", family="family_1")
    copy = passage("p2", "Officials held 40 people in the building.", source="source_2", family="family_1")
    result = retrieve(claim(), [first, copy])
    assert [row["passage_id"] for row in result["candidates"]] == ["p1"]
    assert result["search_receipt"]["redundant_family_candidates_skipped"]["claim_terms"] == 1


def test_search_receipt_hashes_input_snapshot_and_records_query_terms():
    p = passage("p1", "Officials held 40 people in the building.")
    first = retrieve(claim(), [p])
    changed = retrieve(claim(), [passage("p1", "Officials held 4 people in the building.")])
    receipt = first["search_receipt"]
    assert receipt["input_snapshot_sha256"] != changed["search_receipt"]["input_snapshot_sha256"]
    assert receipt["query_terms"]["claim_terms"]
    assert receipt["query_terms"]["counterevidence_terms"]
    assert first["candidates"][0]["candidate_id"] != changed["candidates"][0]["candidate_id"]


def test_aggregate_rejects_accepted_assessment_without_assessor_provenance():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    assessment.pop("assessor_id")
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z",
                                    search_complete=True, minimum_independent_roots=1)
    assert result["status"] == "insufficient_evidence"
    assert result["excluded_assessments"] == [{"assessment_id": "a1", "reason": "missing_assessor_id"}]


def test_aggregate_rejects_accepted_assessment_without_its_own_id():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    assessment.pop("assessment_id")
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z",
                                    search_complete=True, minimum_independent_roots=1)
    assert result["status"] == "insufficient_evidence"
    assert result["excluded_assessments"] == [{"assessment_id": None, "reason": "missing_assessment_id"}]


def test_aggregate_rejects_duplicate_assessment_ids():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    with pytest.raises(ValueError, match="duplicate assessment_id"):
        aggregate_verification(claim(), [assessment, dict(assessment)],
                               as_of_utc="2026-11-05T00:00:00Z", search_complete=True)


def test_accepted_support_requires_every_numeric_claim_value():
    p = passage("p1", "Officials held 40 people in the building.")
    hit = next(hit for hit in retrieve(claim(), [p])["candidates"] if hit["passage_id"] == "p1")
    assessment = create_evidence_assessment(
        claim(), hit, p, relation="supports", decision="accepted", scope=claim()["scope"],
        assessed_at_utc="2026-11-03T00:00:00Z", assessor_id="reviewer:test",
        acceptance_basis="human_adjudication",
    )
    assert assessment["relation"] == "ambiguous"
    assert assessment["decision"] == "candidate"
    assert "missing_asserted_value:count" in assessment["reasons"]


def test_assessment_id_captures_provenance_and_root_changes():
    c = claim()
    p = passage("p1", "Officials held 40 people in the building.")
    hit = next(hit for hit in retrieve(c, [p])["candidates"] if hit["passage_id"] == "p1")
    common = {
        "relation": "supports", "decision": "accepted", "scope": c["scope"],
        "assessed_at_utc": "2026-11-03T00:00:00Z", "assessor_id": "reviewer:test",
        "acceptance_basis": "human_adjudication", "asserted_values": c["key_values"],
        "independence_status": "confirmed_independent",
    }
    first = create_evidence_assessment(c, hit, p, independent_root_id="root_1", **common)
    changed = create_evidence_assessment(c, hit, p, independent_root_id="root_2", **common)
    assert first["assessment_id"] != changed["assessment_id"]


def test_aggregate_rechecks_numeric_values_in_serialized_accepted_assessments():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    assessment.pop("asserted_values")
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z",
                                    search_complete=True, minimum_independent_roots=1)
    assert result["status"] == "insufficient_evidence"
    assert result["excluded_assessments"] == [{"assessment_id": "a1", "reason": "missing_asserted_value:count"}]


def test_aggregate_rejects_mismatched_serialized_numeric_support():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    assessment["asserted_values"] = {"count": {"value": 4, "operator": "eq"}}
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z",
                                    search_complete=True, minimum_independent_roots=1)
    assert result["status"] == "insufficient_evidence"
    assert result["excluded_assessments"] == [{"assessment_id": "a1", "reason": "value_mismatch:count"}]


def test_copies_of_one_root_do_not_meet_independent_support_threshold():
    assessments = [
        accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z"),
        accepted("a2", "supports", "p2", "root_1", "2026-11-03T00:00:00Z"),
    ]
    result = aggregate_verification(claim(), assessments, as_of_utc="2026-11-05T00:00:00Z", search_complete=True)
    assert result["status"] == "insufficient_evidence"
    assert result["independent_support_roots"] == 1
    assert result["supporting_evidence_ids"] == ["p1", "p2"]


def test_numeric_mismatch_cannot_be_accepted_as_support():
    p = passage("p1", "Officials held 4 people in the building.")
    hit = next(hit for hit in retrieve(claim(), [p])["candidates"] if hit["passage_id"] == "p1")
    assessment = create_evidence_assessment(
        claim(), hit, p, relation="supports", decision="accepted", scope=claim()["scope"],
        assessed_at_utc="2026-11-03T00:00:00Z", assessor_id="rule:test",
        acceptance_basis="validated_rule", validated_rule_id="numeric_scope_v1",
        asserted_values={"count": {"value": 4, "operator": "eq"}},
    )
    assert assessment["relation"] == "ambiguous"
    assert assessment["decision"] == "candidate"
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z", search_complete=True,
                                   minimum_independent_roots=1)
    assert result["status"] == "insufficient_evidence"


def test_exact_scope_and_independent_support_can_support_only_within_scope():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z", search_complete=True,
                                    minimum_independent_roots=1)
    assert result["status"] == "supported_within_scope"
    assert result["scope"] == claim()["scope"]


def test_scope_mismatch_is_excluded_from_verification():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z",
                          scope={"place_id": "different_place", "event_date": "2026-11-02"})
    result = aggregate_verification(claim(), [assessment], as_of_utc="2026-11-05T00:00:00Z", search_complete=True,
                                    minimum_independent_roots=1)
    assert result["status"] == "insufficient_evidence"
    assert result["excluded_assessment_ids"] == ["a1"]


def test_correction_changes_as_of_projection_but_preserves_prior_result_link():
    initial = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    correction = accepted("a2", "contradicts", "p2", "root_2", "2026-11-04T00:00:00Z", correction=True)
    before = aggregate_verification(claim(), [initial, correction], as_of_utc="2026-11-03T12:00:00Z",
                                    search_complete=True, minimum_independent_roots=1)
    after = aggregate_verification(claim(), [initial, correction], as_of_utc="2026-11-05T00:00:00Z",
                                   search_complete=True, minimum_independent_roots=1,
                                   supersedes_result_id=before["result_id"])
    assert before["status"] == "supported_within_scope"
    assert after["status"] == "conflicting_evidence"
    assert after["supersedes"] == before["result_id"]
    assert after["as_of_utc"] > before["as_of_utc"]


def test_same_root_support_and_contradiction_remain_a_conflict_with_consistent_counts():
    assessments = [
        accepted("s1", "supports", "p1", "shared_root", "2026-11-03T00:00:00Z"),
        accepted("s2", "supports", "p2", "support_root", "2026-11-03T00:00:00Z"),
        accepted("c1", "contradicts", "p3", "shared_root", "2026-11-04T00:00:00Z"),
    ]
    result = aggregate_verification(claim(), assessments, as_of_utc="2026-11-05T00:00:00Z",
                                    search_complete=True, minimum_independent_roots=1)
    assert result["status"] == "conflicting_evidence"
    assert result["supporting_root_count"] == 2
    assert result["contradicting_root_count"] == 1
    assert result["shared_root_ids"] == ["shared_root"]
    assert "root(s) occur on both sides" in result["rationale"]


def test_no_evidence_is_insufficient_not_refuted_and_no_search_is_unverified():
    no_search = aggregate_verification(claim(), [], as_of_utc="2026-11-05T00:00:00Z", search_complete=False)
    searched = aggregate_verification(claim(), [], as_of_utc="2026-11-05T00:00:00Z", search_complete=True)
    assert no_search["status"] == "unverified"
    assert searched["status"] == "insufficient_evidence"
    assert searched["status"] != "refuted_within_scope"


def test_non_boolean_search_complete_is_rejected():
    with pytest.raises(ValueError, match="search_complete must be boolean"):
        aggregate_verification(claim(), [], as_of_utc="2026-11-05T00:00:00Z", search_complete="yes")


def test_not_verifiable_assessments_are_retained_as_excluded_provenance():
    assessment = accepted("a1", "supports", "p1", "root_1", "2026-11-03T00:00:00Z")
    result = aggregate_verification({**claim(), "observability": "not_verifiable"}, [assessment],
                                    as_of_utc="2026-11-05T00:00:00Z", search_complete=True)
    assert result["status"] == "not_verifiable"
    assert result["excluded_assessments"] == [{"assessment_id": "a1", "reason": "claim_not_verifiable"}]
    assert result["assessment_provenance"][0]["included_in_verification"] is False


def test_result_id_changes_when_scope_or_decision_parameters_change():
    c = claim()
    first = aggregate_verification(c, [], as_of_utc="2026-11-05T00:00:00Z", search_complete=False,
                                   minimum_independent_roots=1)
    changed_threshold = aggregate_verification(c, [], as_of_utc="2026-11-05T00:00:00Z", search_complete=False,
                                               minimum_independent_roots=2)
    changed_search = aggregate_verification(c, [], as_of_utc="2026-11-05T00:00:00Z", search_complete=True,
                                            minimum_independent_roots=1)
    changed_scope = aggregate_verification({**c, "scope": {"place_id": "other"}}, [],
                                           as_of_utc="2026-11-05T00:00:00Z", search_complete=False,
                                           minimum_independent_roots=1)
    assert first["status"] == changed_threshold["status"] == "unverified"
    assert first["result_id"] != changed_threshold["result_id"]
    assert first["result_id"] != changed_search["result_id"]
    assert first["result_id"] != changed_scope["result_id"]


def test_result_id_changes_when_excluded_assessment_provenance_changes():
    c = claim()
    as_of = "2026-11-05T00:00:00Z"
    without_future = aggregate_verification(c, [], as_of_utc=as_of, search_complete=True)
    future = accepted("future", "supports", "p1", "root_1", "2026-11-06T00:00:00Z", c=c)
    with_future = aggregate_verification(c, [future], as_of_utc=as_of, search_complete=True)
    assert without_future["status"] == with_future["status"] == "insufficient_evidence"
    assert without_future["result_id"] != with_future["result_id"]


def test_quote_mismatch_is_rejected_even_if_candidate_offsets_look_valid():
    c = claim()
    p = passage("p1", "Officials held 40 people in the building.")
    hit = next(hit for hit in retrieve(c, [p])["candidates"] if hit["passage_id"] == "p1")
    tampered = {**hit, "quote": "Officials held 4 people"}
    with pytest.raises(ValueError, match="exact citation"):
        create_evidence_assessment(c, tampered, p, relation="supports", decision="accepted", scope=c["scope"],
                                   assessed_at_utc="2026-11-03T00:00:00Z", assessor_id="rule:test")


def test_verification_projection_appends_to_existing_immutable_ledger():
    with EvidenceLedger() as ledger:
        ledger.add_source("source_1", uri="https://example.org/post", title="Public post")
        ledger.add_artifact("artifact_1", source_id="source_1", path="archive/post.html",
                            sha256="a" * 64, media_type="text/html", captured_at="2026-11-02T20:00:00Z",
                            producer="test", run_id="run_1", limitations=[])
        ledger.add_passage("passage_1", artifact_id="artifact_1", text="Exact passage",
                           producer="test", run_id="run_1", limitations=[])
        ledger.add_claim("claim_1", statement="A public post exists", claim_type="published_claim",
                         source_id="source_1")
        result = aggregate_verification(
            {"claim_id": "claim_1", "statement": "A public post exists", "scope": {"platform": "web"}},
            [], as_of_utc="2026-11-05T00:00:00Z", search_complete=True,
        )
        record = append_verification_result(ledger, result, producer="test", run_id="run_1")
        repeated = append_verification_result(ledger, result, producer="test", run_id="run_1")
        assert record["record_type"] == "VerificationResult"
        assert ledger.get_record(result["result_id"]) == record
        assert repeated == record


def test_ledger_projection_retains_accepted_assessment_provenance():
    c = {"claim_id": "claim_1", "statement": "Public claim", "scope": {"place_id": "building_1"}}
    assessments = [
        accepted("a1", "supports", "passage_1", "root_1", "2026-11-03T00:00:00Z", c=c),
        accepted("a2", "supports", "passage_2", "root_2", "2026-11-03T01:00:00Z", c=c),
        accepted("a3", "supports", "passage_3", "root_3", "2026-11-03T02:00:00Z",
                 c=c, scope={"place_id": "other"}),
    ]
    assessments[1]["assessment_source"] = "validated_rule"
    assessments[1]["assessor_id"] = "rule:count"
    assessments[1]["validated_rule_id"] = "count-extract-v1"
    result = aggregate_verification(c, assessments, as_of_utc="2026-11-05T00:00:00Z", search_complete=True)
    with EvidenceLedger() as ledger:
        ledger.add_source("source_1", uri="https://example.org/post", title="Public post")
        for index in (1, 2, 3):
            ledger.add_artifact(f"artifact_{index}", source_id="source_1", path=f"archive/{index}.html",
                                sha256=str(index) * 64, media_type="text/html", captured_at="2026-11-02T20:00:00Z",
                                producer="test", run_id="run_1", limitations=[])
            ledger.add_passage(f"passage_{index}", artifact_id=f"artifact_{index}", text=f"Exact passage {index}",
                               producer="test", run_id="run_1", limitations=[])
        ledger.add_claim("claim_1", statement="Public claim", claim_type="published_claim", source_id="source_1")
        record = append_verification_result(ledger, result, producer="test", run_id="run_1")
    provenance = json.loads(record["rationale"])
    assert provenance["assessment_ids"] == ["a1", "a2"]
    assert [item["assessed_at_utc"] for item in provenance["assessment_provenance"]] == [
        "2026-11-03T00:00:00Z", "2026-11-03T01:00:00Z", "2026-11-03T02:00:00Z",
    ]
    assert [item["independent_root_id"] for item in provenance["assessment_provenance"]] == ["root_1", "root_2", "root_3"]
    rule_record = next(item for item in provenance["assessment_provenance"] if item["assessment_id"] == "a2")
    assert rule_record["assessor_id"] == "rule:count"
    assert rule_record["validated_rule_id"] == "count-extract-v1"
    assert provenance["excluded_assessments"] == [{"assessment_id": "a3", "reason": "scope_mismatch"}]
    assert next(item for item in provenance["assessment_provenance"] if item["assessment_id"] == "a3")["included_in_verification"] is False


def test_export_writes_assessments_results_claim_matrix_and_unresolved_queue(tmp_path):
    c = claim()
    search = retrieve(c, [passage("p1", "Officials held 40 people in the building.")])
    result = aggregate_verification(c, [], as_of_utc="2026-11-05T00:00:00Z", search_complete=True)
    paths = export_verification_package(search, [], result, tmp_path)
    assert set(paths) == {"candidates", "assessments", "results", "search_receipt", "claim_matrix", "unresolved_queue"}
    assert paths["candidates"].read_text().count("\n") == 1
    assert paths["assessments"].read_text() == ""
    assert '"retriever":"deterministic_local_bm25_v1"' in paths["search_receipt"].read_text()
    assert "insufficient_evidence" in paths["claim_matrix"].read_text()
    assert "claim_1" in paths["unresolved_queue"].read_text()


def test_export_queue_keeps_assessments_excluded_by_as_of(tmp_path):
    c = claim()
    search = retrieve(c, [passage("p1", "Officials held 40 people in the building.")])
    candidate = search["candidates"][0]
    assessment = accepted("late", "supports", "p1", "root_1", "2026-11-06T00:00:00Z")
    assessment["candidate_id"] = candidate["candidate_id"]
    result = aggregate_verification(c, [assessment], as_of_utc="2026-11-05T00:00:00Z", search_complete=True)
    assert result["excluded_assessment_ids"] == ["late"]
    paths = export_verification_package(search, [assessment], result, tmp_path)
    queue = json.loads(paths["unresolved_queue"].read_text())
    assert queue["candidate_ids_to_review_or_retrieve"] == [candidate["candidate_id"]]
