# Evaluation Harness & Release Gates v1

## Purpose and boundary

`src/analysis/evaluation_harness.py` provides repeatable structural release gates for Social run artifacts and a frozen synthetic/adversarial regression suite. A passing hard-gate result means the submitted contracts, IDs, timestamps, paths, hashes, provenance references, and selected invariants are internally consistent. It does **not** mean a claim is true, a source is authentic, or a citation semantically entails the finding.

The API deliberately reports `semantic_evaluation.status=not_evaluated` and a null unsupported-assertion rate. An LLM judge or agreement among several models is not accepted as a ground-truth substitute by this harness.

## Run bundle API

```python
from src.analysis.evaluation_harness import evaluate_run_bundle

result = evaluate_run_bundle(
    run_manifest=run_manifest,
    incident_spec=incident_spec,             # optional but recommended
    artifact_root="runs/run-123",            # optional; enables output byte/hash checks
    report_context=report_context,             # provide the report inputs together
    findings=findings,
    evidence_records=evidence_records,
    verification_results=verification_results,
    event_reconstruction=event_reconstruction,
    source_dependency_edges=dependency_edges,
    report_bundle_dir="runs/run-123/report", # optional; verifies generated receipt/hashes
)
```

The result is JSON-serializable and includes `status`, `hard_gate_status`, `hard_gate_failures`, `warnings`, object counts, optional report-bundle verification, and explicit semantic non-evaluation. `status=passed_with_warnings` means no deterministic hard gate failed, but one or more optional byte/lineage checks could not be completed. It is not a softer semantic confidence level.

When report inputs are supplied, the harness sends them through the existing deterministic `build_report_bundle()` validator in a temporary directory. No report is written to the requested output location. This checks finding/evidence/result references, exact locators, timestamp cutoff, scope and status consistency using the same production contract. It does not check semantic entailment.

When `artifact_root` is supplied, every `run_manifest.outputs[*]` path and every source snapshot's `snapshot_artifact_path` must resolve to a regular file within that root and match its declared SHA-256. Without it, manifest output and snapshot bytes are explicitly marked unverified.

The event reconstruction path validates `schemas/event_reconstruction.schema.json`, requires an explicit UTC `as_of_utc`, checks that it matches the IncidentSpec when supplied, and rejects any referenced evidence captured after the reconstruction cutoff. It also checks uniqueness and referential integrity for event IDs, mention IDs, evidence references, time anchors, candidate links, timelines, and temporal relations. The harness does not merge events or infer causal relations.

Every verification evidence reference is checked even without a rendered report context. A `supported_within_scope` or `refuted_within_scope` result must cite explicit evidence with nonblank `independent_root_id` values; its unique root count is recomputed and checked against the positive integer `minimum_independent_roots`. Other unresolved statuses may retain unknown lineage as a warning. The W05 lineage candidate graph alone does not establish independent sources.

## Frozen synthetic and adversarial suite

Run with:

```bash
python -m src.analysis.evaluation_harness --frozen-suite
```

The suite emits deterministic JSON to stdout and exits nonzero if any invariant fails. Fixtures are under `tests/fixtures/evaluation_harness/`.

| Fixture | Invariant exercised | What it does not establish |
|---|---|---|
| `known_microcase.json` | Event reconstruction retains separate physical events and orders bounded intervals correctly | Real-case extraction accuracy or ground truth |
| `mass_copy_fanout.json` | 1,000 copies from one known root remain one source root and cannot satisfy a two-root threshold | Whether unknown sources are actually independent |
| `contradictory_testimony.json` | Conflicting status preserves both support and contradiction references | Which side is true |
| `corrected_statement_as_of.json` | A post-cutoff correction cannot leak into an earlier as-of projection | Whether either statement is accurate |
| `missing_corpus.json` | Partial, blocked, or unavailable sources plus no evidence require an unresolved status | Completeness of collection |
| `reused_video_mismatch.json` | Verified pre-incident footage reuse cannot alone support a later incident claim | Video geolocation or event identity from pixels |

These are synthetic logic controls, not an empirical benchmark for Ukrainian/Russian language understanding, model calibration, or real-world event accuracy. Phase 9 remains partially complete until a held-out incident benchmark with independently adjudicated semantic labels exists; the harness deliberately reports `not_evaluated` rather than inventing an accuracy estimate.

## Gate families

1. **Run contracts:** IncidentSpec and RunManifest schemas, `completed_bounded` release state, incident/run identity, unique snapshot/task/output keys, task timestamps within the run interval and snapshot capture no later than `as_of`.
2. **Byte integrity:** output exists, remains under `artifact_root`, is not a symlink, and matches SHA-256.
3. **Report structure:** production report validator; report receipt output hashes.
4. **Event graph references:** schema validity, unique IDs, no dangling evidence, time-anchor, timeline, or relation IDs.
5. **Lineage consistency:** check every evidence reference, require auditable roots for affirmative support/refutation, recompute root counts, and reject malformed thresholds; preserve unknown lineage for non-affirmative statuses as warning.
6. **Frozen invariants:** deterministic tests for duplicates, contradictory evidence, corrections/as-of, incomplete corpora, old reused video, and a known synthetic timeline.

Each issue has a stable `gate_id`; downstream CI may fail a release on `hard_gate_status=failed` and retain warnings for analyst visibility. Do not collapse these distinct gates into a weighted “truth score”.

## Integration and failure handling

- Run the frozen suite in CI and before a report release.
- Run `evaluate_run_bundle()` after the report bundle has been generated, passing the archived manifest, evidence projection and event result. Use `artifact_root` so hashes are checked against actual bytes.
- Persist the returned JSON next to run outputs and include its hash in a later RunManifest revision; do not mutate the source manifest in place.
- A failed gate means the projection or report package is internally inconsistent and must not be marked released. Preserve diagnostic JSON; do not silently repair IDs or timestamps in the evaluator.
- A passed gate is not semantic validation. Keep citation entailment, source authenticity, video identity/location/time, completeness, and causal claims explicitly unverified unless a separate validated component supplies evidence for those dimensions.

## Verification

```bash
PYTHONPATH=. pytest -q tests/test_evaluation_harness.py
PYTHONPATH=. python -m src.analysis.evaluation_harness --frozen-suite
python -m py_compile src/analysis/evaluation_harness.py
git diff --check
```
