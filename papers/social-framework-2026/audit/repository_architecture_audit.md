# Repository architecture audit — completed before manuscript drafting

## Frozen system identity

Audited baseline `f0e9d0d67422b0c286a2cb9e7d4e935a833a9533`, branch `codex/social-master-plan-audit-remediation`, commit2026-11-09T17:35:56+02:00. Initial worktree clean. Main checkout remains at older `e1f66f9b0c57cc5f4c6f44527923e1fa5a11840b`; using main alone would omit remediations. `git fetch origin --prune` found no newer remote baseline. Publication files are new and are not part of the frozen system snapshot. Audit date2026-11-10.

## Audit evidence and coverage

Direct code inspection is divided into [ingestion](ingestion_audit.md), [evidence/events/autonomy/audience](evidence_autonomy_audit.md), [evaluation/statistics](evaluation_audit.md), and [multimodal](media_audit.md). Those linked files contain the detailed Component/Path/Purpose/Inputs/Outputs/Dependencies/Implementation/Validation tables and concrete functions/line references. [Document inventory](document_inventory.md) distinguishes specifications and Deep Research from execution evidence. `data/directory_inventory.json` records actual directories and tracked counts. `data/environment.json` records measured audit dependencies; no unified lockfile exists. Full suite:783passed+16subtests; evidence and ingestion focused suites are subsets and must not be added to783.

## Actual architectural composition

This is a modular Python research repository, not a packaged universal investigator. Separate platform collectors feed JSON/JSONL snapshots. Legacy analysis has case-specific preprocessing/relevance/narrative rules, full-text shingling, graph analysis and conditional nulls. New typed contracts support Source/Artifact/Passage evidence accounting, retrieval, source dependency, temporal organization, uncertainty scenarios and report gates. A fixed orchestrator integrates SourceWatch and optional pretyped offline analysis. Video processing is a separate local pipeline. Audience contracts/aggregation accept supplied semantic labels; trained multilingual target-aware classifiers are not evaluated production inference.

Implementation readiness is component-specific: contracts, local ledger and deterministic processors are implemented/tested; platform access remains permission/network dependent; one-off claim/timeline/ASR builders are curated research scripts; dossier generators are report-only; perceptual and semantic heuristics are experimental. No release engineering/SLA/security audit establishes repository-wide production readiness. Planned end-to-end fact verification and general physical-event discovery are not established by current orchestration.

## Critical audit outcomes

1. Correct missingness denominator:459raw missing texts/23350allposts, not1408relevant;0missing inrelevant;1384>=80chars excludes24short.
2. Exact369-pair graph derives from historical1408/1384corpus, despite contrary merged-corpus lineage label.
3. Current25claim matrix is19supported/0refuted/6insufficient/36acceptedruleassessments; version history is explicit. These are outputs, not measured accuracy.
4. Numeric-predicate and negation counterexamples demonstrate semantic rule failure; persisted in data/evidence_counterexamples.json.
5. General offline retrieval creates no accepted assessments. Fresh smoke run remains partial with unverifiedclaim, no report; dangling eventref correctly fails structuralgate.
6. Physical timeline is analyst-supplied; quote flags lack independently demonstrated human acoustic review.607decodes are technical checks.
7. SourceWatch receipts with different timestamps cannot be substituted. TLS errors establish failed access, not publicationabsence or a diagnosed permanent CAcause.

## Audit boundary

No Social core or prior case-paper files were modified. No fresh platform collection, paid inference, full607video decode/ASR, or independent human annotation was performed. ExactJaccard/metric/null-summary and25-drawprefix replays were executed; full9999draws were read/recomputed rather than all regenerated. Subsequent manuscript claims must inherit these bounds.
