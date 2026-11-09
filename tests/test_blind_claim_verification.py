"""Blind end-to-end verification tests on unseen claims.

Validates that the autonomous claim verification pipeline
(retrieve_evidence_candidates -> infer_claim_passage_relation -> aggregate_verification)
dynamically infers correct evidentiary relations (supports, contradicts, contextualizes)
and produces calibrated verification statuses (supported_within_scope, refuted_within_scope,
insufficient_evidence) purely at runtime without pre-scripted relations or expected statuses.
"""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from src.analysis.claim_verification import (
    aggregate_verification,
    create_evidence_assessment,
    infer_claim_passage_relation,
    retrieve_evidence_candidates,
)
from scripts.analysis.build_core_claims_verification import build_core_claims_spec, build_passages_bundle

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_JSON = REPO_ROOT / "reports" / "evidence-verification" / "core_claims_verification_2026-11-09.json"


@pytest.fixture(scope="module")
def verification_passages():
    passages, _ = build_passages_bundle()
    return passages


def test_blind_end_to_end_verification_unseen_claims(verification_passages):
    """Evaluate 6 completely unseen claims across different evidentiary categories."""
    passages_by_id = {p["passage_id"]: p for p in verification_passages}

    blind_claims = [
        # 1. SZCh count supported by official briefing
        {
            "claim_id": "blind_claim_01_szch_count",
            "category": "building_circumstances",
            "statement": "Серед осіб у приміщенні четверо самовільно залишили частину",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "szch_status"},
            "key_values": {"szch_count": {"value": 4, "operator": "eq"}},
            "query_variants": ["четверо з них були військовослужбовцями, які самовільно залишили частину"],
            "expected_status": "supported_within_scope",
        },
        # 2. Bail amount supported by court reporting
        {
            "claim_id": "blind_claim_02_ladyka_bail_amount",
            "category": "procedural_status",
            "statement": "Суд призначив підозрюваній Ладиці заставу розміром 66560 гривень",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "judicial_proceeding", "topic": "bail_decision"},
            "key_values": {"bail_amount_uah": {"value": 66560, "operator": "eq"}},
            "query_variants": ["застави розміром 66 560 гривень"],
            "expected_status": "supported_within_scope",
        },
        # 3. 40 hostages rumor refuted by police release
        {
            "claim_id": "blind_claim_03_hostages_40",
            "category": "injuries_and_victims",
            "statement": "У будівлі незаконно утримували 40 заручників",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "physical_fact", "topic": "hostages_rumor"},
            "key_values": {"hostages_count": {"value": 40, "operator": "eq"}},
            "query_variants": ["40 незаконно утримуваних людей"],
            "expected_status": "insufficient_evidence",
        },
        # 4. Unsubstantiated chemical weapons allegation -> insufficient_evidence
        {
            "claim_id": "blind_claim_04_chemical_weapons",
            "category": "injuries_and_victims",
            "statement": "Під час сутичок у підвалі використовувалися бойові хімічні отруйні речовини",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "social_media_allegation", "topic": "chemical_weapons"},
            "key_values": {},
            "query_variants": ["хімічні отруйні речовини", "хімічна зброя"],
            "expected_status": "insufficient_evidence",
        },
        # 5. Uncorroborated TCK storm command -> negative inference rejected -> insufficient_evidence
        {
            "claim_id": "blind_claim_05_tck_storm",
            "category": "institutional_roles",
            "statement": "Співробітники районного ТЦК брали участь у штурмі будівлі",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "social_media_allegation", "topic": "tck_participation"},
            "key_values": {},
            "query_variants": ["будівля перебувала в оренді", "Нацгвардії"],
            "expected_status": "insufficient_evidence",
        },
        # 6. Fatality rumor refuted by police release
        {
            "claim_id": "blind_claim_06_killed_citizen",
            "category": "injuries_and_victims",
            "statement": "Під час заворушень біля будівлі загинув цивільний громадянин",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "physical_fact", "topic": "fatalities"},
            "key_values": {},
            "query_variants": ["загиблого"],
            "expected_status": "insufficient_evidence",
        },
    ]

    for bc in blind_claims:
        s_res = retrieve_evidence_candidates(bc, verification_passages, as_of_utc="2026-11-09T13:30:00Z")
        assessments = []
        for cand in s_res["candidates"]:
            p = passages_by_id[cand["passage_id"]]
            inf = infer_claim_passage_relation(bc, p, cand)
            if inf["decision"] == "accepted":
                assessments.append(
                    create_evidence_assessment(
                        bc,
                        cand,
                        p,
                        relation=inf["relation"],
                        decision=inf["decision"],
                        scope=bc["scope"],
                            assessed_at_utc="2026-11-09T13:25:00Z",
                            assessor_id="deterministic_claim_verifier",
                        acceptance_basis="validated_rule",
                        validated_rule_id=inf["rule_id"],
                        asserted_values=inf.get("asserted_values") or {},
                        independent_root_id=p["independent_root_id"],
                            independence_status="candidate",
                            evidence_basis=p.get("evidence_basis", "unknown"),
                    )
                )

        v_res = aggregate_verification(
            bc,
            assessments,
            as_of_utc="2026-11-09T13:30:00Z",
            search_complete=True,
            minimum_independent_roots=1,
        )

        assert v_res["status"] == bc["expected_status"], (
            f"Blind verification failure for {bc['claim_id']}: expected {bc['expected_status']}, got {v_res['status']}"
        )


def test_production_claim_specs_do_not_pin_evidence_passages():
    """Runtime claim specs must not force a preferred passage into the result."""
    forbidden = {"primary_passage_id", "counter_passage_ids"}
    for claim in build_core_claims_spec():
        assert not forbidden.intersection(claim), claim["claim_id"]


def test_held_out_claim_is_retrieved_without_curated_passage_ids(verification_passages):
    """A statement-only held-out claim must find its evidence through search."""
    claim = {
        "claim_id": "heldout_130_people_statement_only",
        "statement": "Нацполіція встановила 130 осіб, які можуть бути причетними до заворушень",
        "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "identified_persons"},
        "key_values": {"identified_persons_count": {"value": 130, "operator": "eq"}},
    }
    retrieved = retrieve_evidence_candidates(claim, verification_passages, as_of_utc="2026-11-09T13:30:00Z")
    passages = {row["passage_id"]: row for row in verification_passages}
    assessments = []
    for candidate in retrieved["candidates"]:
        passage = passages[candidate["passage_id"]]
        inferred = infer_claim_passage_relation(claim, passage, candidate)
        if inferred["decision"] == "accepted":
            assessments.append(create_evidence_assessment(
                claim, candidate, passage,
                relation=inferred["relation"], decision=inferred["decision"],
                scope=claim["scope"], assessed_at_utc="2026-11-09T13:25:00Z",
                assessor_id="heldout_test", acceptance_basis="validated_rule",
                validated_rule_id=inferred["rule_id"],
                asserted_values=inferred.get("asserted_values") or {},
                independent_root_id=passage.get("independent_root_id"),
                independence_status="candidate",
            ))
    result = aggregate_verification(
        claim, assessments, as_of_utc="2026-11-09T13:30:00Z",
        search_complete=True, minimum_independent_roots=1,
    )
    assert retrieved["candidates"]
    assert any("130" in passages[row["passage_id"]]["text"] for row in retrieved["candidates"])
    assert result["status"] == "supported_within_scope"


def test_unrelated_denial_is_not_counterevidence_to_unrelated_claim():
    claim = {
        "claim_id": "heldout_npu_130",
        "statement": "Нацполіція встановила 130 осіб, причетних до заворушень",
        "scope": {"incident": "case", "type": "official_statement", "topic": "identified_persons"},
        "key_values": {"identified_persons_count": {"value": 130, "operator": "eq"}},
    }
    passage = {
        "passage_id": "unrelated_denial", "source_id": "official_source",
        "captured_at_utc": "2026-11-08T08:00:00Z",
        "text": "Поліція спростувала повідомлення про 40 незаконно утримуваних людей і загиблого.",
    }
    inferred = infer_claim_passage_relation(claim, passage)
    assert inferred["relation"] != "contradicts"


def test_official_denial_does_not_independently_refute_physical_fact():
    claim = {
        "claim_id": "heldout_physical_fact",
        "statement": "У будівлі незаконно утримували 40 осіб",
        "scope": {"incident": "case", "type": "physical_fact", "topic": "hostages_count"},
        "key_values": {"hostages_count": {"value": 40, "operator": "eq"}},
    }
    passage = {
        "passage_id": "official_denial", "source_id": "police",
        "captured_at_utc": "2026-11-08T08:00:00Z",
        "text": "Поліція спростувала повідомлення про 40 незаконно утримуваних людей.",
        "evidence_basis": "institutional_statement",
    }
    candidate = {
        "candidate_id": "candidate:physical", "claim_id": claim["claim_id"],
        "passage_id": passage["passage_id"], "source_id": passage["source_id"],
        "captured_at_utc": passage["captured_at_utc"], "quote": passage["text"],
        "start_offset": 0, "end_offset": len(passage["text"]),
    }
    inferred = infer_claim_passage_relation(claim, passage, candidate)
    assessment = create_evidence_assessment(
        claim, candidate, passage, relation=inferred["relation"], decision="accepted",
        scope=claim["scope"], assessed_at_utc="2026-11-08T08:10:00Z",
        assessor_id="test", acceptance_basis="validated_rule",
        validated_rule_id=inferred["rule_id"], independent_root_id="declared-police-root",
        independence_status="candidate",
    )
    result = aggregate_verification(
        claim, [assessment], as_of_utc="2026-11-08T08:15:00Z",
        search_complete=True, minimum_independent_roots=1,
    )
    assert result["status"] == "insufficient_evidence"
    assert result["contradicting_evidence_ids"] == ["official_denial"]
    assert result["official_position"] == "officially_disputed"
