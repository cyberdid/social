#!/usr/bin/env python3
"""Deterministic challenge evaluation of the claim-passage relation rule.

Compares two versions of infer_claim_passage_relation on the 25 curated claims and passages of
reports/evidence-verification/core_claims_verification_2026-11-09.json.  No human labels, models or
network.  This is an authored stress test: templates were written by the same (AI) author who revised
the rule and the rule was revised after seeing two hand-made failures, so results are NOT a blind
accuracy benchmark and do not estimate prevalence in real text.

Case families (expected outcome by construction):
  control          baseline-accepted (claim, passage) support pairs, unmodified -> measures retention only
  negated_predicate passage with "не" inserted before the first verb-like word sharing a claim stem -> not supports
  wrong_predicate  numeric claims against unrelated sentences carrying the same numbers -> not supports
  altered_number   digits of every claimed value replaced with value+7 -> not supports
  cross_claim      claim i against support passages of claim j (j != i, not accepted for i) -> not supports

Usage: evaluate_verifier_challenges.py --out data/verifier_challenge_evaluation.json [--baseline-rev f0e9d0d]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = "reports/evidence-verification/core_claims_verification_2026-11-09.json"
TEMPLATES = ("{v} дерев ростуть у саду.", "У місті відкрили {v} нових кав'ярень.", "Книга має {v} сторінок із ілюстраціями.")
VERBISH = re.compile(r"(ав|ив|ув|ла|ло|ли|лась|лись|ть|ють|ать|ять|ить|ено|ано|ито)$")
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def baseline_source(rev: str, target: Path) -> str:
    src = subprocess.run(["git", "show", f"{rev}:src/analysis/claim_verification.py"], cwd=ROOT, check=True,
                         capture_output=True).stdout
    target.write_bytes(src)
    return hashlib.sha256(src).hexdigest()


def is_support(res: dict) -> bool:
    return res.get("relation") == "supports" and res.get("decision") == "accepted"


def negate(claim_stmt: str, text: str, stem) -> str | None:
    stems = {stem(t.lower()) for t in WORD.findall(claim_stmt) if len(t) >= 4}
    for m in WORD.finditer(text):
        w = m.group(0).lower()
        if len(w) >= 4 and m.group(0)[0].islower() and stem(w) in stems and VERBISH.search(w):
            return text[: m.start()] + "не " + text[m.start():]
    return None


def build_cases(matrix: dict, baseline) -> list[dict]:
    passages = {p["passage_id"]: p for p in matrix["passages"]}
    claims, support, accepted_any = [], {}, {}
    for row in matrix["verification_bundle"]:
        claim = row["claim"]
        claims.append(claim)
        for a in row["assessments"]:
            accepted_any.setdefault(claim["claim_id"], set()).add(a.get("evidence_id"))
            if a.get("relation") == "supports":
                pid = a.get("evidence_id")
                if pid in passages:
                    support.setdefault(claim["claim_id"], []).append(pid)
    cases: list[dict] = []
    for claim in claims:
        cid = claim["claim_id"]
        kv = claim.get("key_values") or {}
        for pid in support.get(cid, []):
            text = passages[pid]["text"]
            cases.append({"family": "control", "claim": claim, "passage": text, "source": pid})
            n = negate(claim["statement"], text, baseline._stem_uk)
            if n:
                cases.append({"family": "negated_predicate", "claim": claim, "passage": n, "source": pid})
            changed, altered = 0, text
            for spec in kv.values():
                v = str(spec.get("value"))
                new, k = re.subn(rf"(?<!\d){re.escape(v)}(?!\d)", str(spec["value"] + 7), altered)
                altered, changed = new, changed + k
            if kv and changed:
                cases.append({"family": "altered_number", "claim": claim, "passage": altered, "source": pid})
        if kv and support.get(cid):
            nums = " і ".join(str(s.get("value")) for s in kv.values())
            for i, tpl in enumerate(TEMPLATES):
                cases.append({"family": "wrong_predicate", "claim": claim, "passage": tpl.format(v=nums), "source": f"template_{i}"})
        for other, pids in support.items():
            if other != cid:
                for pid in pids:
                    if pid not in support.get(cid, []) and pid not in accepted_any.get(cid, set()):
                        cases.append({"family": "cross_claim", "claim": claim, "passage": passages[pid]["text"], "source": pid})
    seen, uniq = set(), []
    for c in cases:
        key = (c["family"], c["claim"]["claim_id"], c["passage"])
        if key not in seen:
            seen.add(key)
            uniq.append(c)
    return uniq


def run(mod, cases) -> list[bool]:
    return [is_support(mod.infer_claim_passage_relation(c["claim"], {"text": c["passage"]})) for c in cases]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--baseline-rev", default="f0e9d0d")
    a = ap.parse_args()
    matrix_bytes = (ROOT / MATRIX).read_bytes()
    matrix = json.loads(matrix_bytes)
    current_path = ROOT / "src/analysis/claim_verification.py"
    with tempfile.TemporaryDirectory() as td:
        bpath = Path(td) / "cv_baseline.py"
        bsha = baseline_source(a.baseline_rev, bpath)
        base = load_module(bpath, "cv_baseline")
    cur = load_module(current_path, "cv_current")
    cases = build_cases(matrix, base)
    rb, rc = run(base, cases), run(cur, cases)
    fam = Counter(c["family"] for c in cases)
    summary = {}
    for f in fam:
        idx = [i for i, c in enumerate(cases) if c["family"] == f]
        summary[f] = {"n": len(idx), "baseline_accepted_support": sum(rb[i] for i in idx),
                      "current_accepted_support": sum(rc[i] for i in idx)}
    residual = [{"family": c["family"], "claim_id": c["claim"]["claim_id"], "source": c["source"],
                 "passage": c["passage"][:400]} for c, r in zip(cases, rc) if r and c["family"] != "control"]
    lost = [{"claim_id": c["claim"]["claim_id"], "source": c["source"],
             "current": cur.infer_claim_passage_relation(c["claim"], {"text": c["passage"]})["rationale"][:200]}
            for c, r, b in zip(cases, rc, rb) if c["family"] == "control" and b and not r]
    out = {"schema_version": "1.0", "evaluation_kind": "authored deterministic stress test; not a blind accuracy benchmark",
           "baseline_rev": a.baseline_rev, "baseline_sha256": bsha,
           "current_sha256": hashlib.sha256(current_path.read_bytes()).hexdigest(),
           "matrix": MATRIX, "matrix_sha256": hashlib.sha256(matrix_bytes).hexdigest(),
           "templates": TEMPLATES, "summary": summary, "residual_false_accepts": residual, "lost_controls": lost}
    a.out.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("residual", Counter(r["family"] for r in residual), "lost controls", len(lost))


if __name__ == "__main__":
    main()
