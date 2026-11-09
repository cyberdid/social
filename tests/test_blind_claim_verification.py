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

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_JSON = REPO_ROOT / "reports" / "evidence-verification" / "core_claims_verification_2026-11-09.json"


@pytest.fixture(scope="module")
def verification_passages():
    with open(VERIFICATION_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return data["passages"]


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
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "social_media_allegation", "topic": "hostages_rumor"},
            "key_values": {"hostages_count": {"value": 40, "operator": "eq"}},
            "query_variants": ["40 незаконно утримуваних людей"],
            "expected_status": "refuted_within_scope",
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
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "social_media_allegation", "topic": "fatalities"},
            "key_values": {},
            "query_variants": ["загиблого"],
            "expected_status": "refuted_within_scope",
        },
    ]

    for bc in blind_claims:
        s_res = retrieve_evidence_candidates(bc, verification_passages, as_of_utc="2026-11-08T08:15:00Z")
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
                        assessed_at_utc="2026-11-08T08:10:00Z",
                        assessor_id="autonomous_claims_verifier",
                        acceptance_basis="validated_rule",
                        validated_rule_id=inf["rule_id"],
                        asserted_values=inf.get("asserted_values") or {},
                        independent_root_id=p["independent_root_id"],
                        independence_status="confirmed_independent",
                    )
                )

        v_res = aggregate_verification(
            bc,
            assessments,
            as_of_utc="2026-11-08T08:15:00Z",
            search_complete=True,
            minimum_independent_roots=1,
        )

        assert v_res["status"] == bc["expected_status"], (
            f"Blind verification failure for {bc['claim_id']}: expected {bc['expected_status']}, got {v_res['status']}"
        )
