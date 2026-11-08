# Audience Response Intelligence Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve privacy-safe Telegram comment reaction breakdowns and build W14 audience analysis on top of the existing comment, claim, entity, and evidence records.

**Architecture:** Additive raw collection keeps the current `reactions` integer stable while writing a typed, timestamped aggregate and an explicit completeness state. Later analysis is a separate deterministic/ML layer that links comment interpretations to existing Social targets and reports frame-conditional estimates with uncertainty.

**Tech Stack:** Python, Telethon/MTProto, JSONL, pytest, existing Social claim/evidence and report contracts.

**Spec:** `docs/specs/audience-response-v1.md`.

## Global Constraints

- Collect aggregate reaction counts only; never call `messages.getMessageReactionsList` or persist reactor identities.
- Preserve the legacy `reactions` numeric field for existing comment-signal consumers.
- Distinguish message reaction states (`not_reported`, `empty`, `available`, `current_user_excluded`) from request outcomes (`no_update`, `wrong_peer_update`, `request_failed`) and absent legacy fields; do not convert unavailable data into analytical zero.
- Record an observation timestamp for every new reaction vector; do not claim historical reaction dynamics from one snapshot.
- Do not equate reactions, replies, or classifier scores with support by the population.
- Use only the linked discussion peer and the comment message ID for per-comment reaction operations.
- Do not run a full live collection during implementation tests; live sampling, if run, is bounded and emits only aggregate, content-free receipts.
- Keep all outputs in the existing isolated worktree; do not stage, commit, or publish shared changes.

---

### Task 1: Add a pure typed reaction serializer to the comment collector

**Files:**
- Modify: `src/tg_comments_collect.py`
- Create: `tests/test_tg_comments_collect.py`

**Interfaces:**
- Add `serialize_reaction_snapshot(reactions, observed_at_utc: str) -> dict[str, object]`.
- Return keys: `legacy_total`, `reaction_breakdown`, `reaction_state`, `reaction_observed_at`.
- Each breakdown row has `kind`, `key`, and `count`; standard emoji, custom emoji, paid, and unknown constructors have separate representations described in `docs/specs/audience-response-v1.md`.
- `MessageReactions.min` takes precedence and yields `current_user_excluded`.

- [x] **Step 1: Write focused tests first** for: no reaction object; present-but-empty results; ordinary emoji counts; custom emoji document ID string preservation; paid reaction preservation; unknown constructor; `min=True`; deterministic legacy sum; malformed fractional/string counts.
- [x] **Step 2: Verify RED** with `../../.venv/bin/python -m pytest -q tests/test_tg_comments_collect.py`; all five behaviors failed on the missing serializer as expected.
- [x] **Step 3: Implement the pure serializer** in `src/tg_comments_collect.py`. It uses constructor-aware handling with an unknown-type fallback and does not change network behavior.
- [x] **Step 4: Attach the serializer output to each comment record.** One UTC `fetched_at` value is shared with `reaction_observed_at`; the legacy `reactions` field is preserved as `legacy_total`.
- [x] **Step 5: Verify GREEN and compatibility** with the focused tests plus `../../.venv/bin/python -m pytest -q tests/test_continuation_merge.py tests/test_e2e_evidence_pipeline.py`. Original cases passed (5); the two malformed-count cases separately failed before strict validation and passed afterward (7 total focused cases).

### Task 2: Add a bounded MTProto refresh adapter for min-marked reactions

**Files:**
- Create: `src/analysis/telegram_reaction_snapshots.py`
- Create: `tests/test_telegram_reaction_snapshots.py`
- Modify: `docs/specs/audience-response-v1.md`

**Interfaces:**
- `async refresh_min_reactions(client, discussion_peer, message_ids: list[int]) -> list[dict]` returns one row per requested comment ID with that local `comment_id` for internal correlation, `request_status`, `reaction_state`, `reaction_breakdown`, `reaction_observed_at`, and optional sanitized `error_code`.
- Build only `messages.getMessagesReactions(peer=discussion_peer, id=message_ids)` calls. Never call the per-reactor list method.
- `request_status` is `ok` or `request_failed`; `reaction_state` is `available`, `empty`, `current_user_excluded`, or `not_reported`. `request_failed` is not a reaction-state value. Include `observed_at_utc` and a sanitized error code; never include source text, peer IDs, or user IDs. Internal correlation uses comment IDs already present in the local collected corpus; receipts redact them.

- [x] **Step 1: Write request-shape tests** that assert exact discussion peer and comment IDs are passed and no reaction-list method is referenced.
- [x] **Step 2: Verify RED** with the focused test path; expected failure is missing module/API.
- [x] **Step 3: Implement one bounded request adapter** using Telethon's generated `GetMessagesReactionsRequest`; do not add automatic unbounded retry or polling.
- [x] **Step 4: Test response mapping** for aggregate updates, empty/no-update results, `MessageReactions.min`, private-channel and invalid-message errors, and flood-wait reporting without sleeping.
- [x] **Step 5: Run focused tests and inspect the returned receipt** to confirm that it contains no user/reaction identities or raw text. The adapter now exposes request status independently from reaction state; renderer text clarifies that failure is not a zero.

### Task 3: Define stable comment and reaction snapshot contracts

**Files:**
- Create: `schemas/comment_reaction_snapshot.schema.json`
- Create: `src/analysis/audience_response_contracts.py`
- Create: `tests/test_audience_response_contracts.py`
- Modify: `docs/specs/audience-response-v1.md`

**Interfaces:**
- Validate a reaction snapshot with `snapshot_id`, `platform`, `comment_id`, `source_post_id`, `thread_id`, `parent_comment_id`, `author_pseudonym`, platform timestamps, `reaction_state`, optional `reaction_breakdown`, and a source snapshot reference.
- Keep model interpretation provenance in Task 4's separate interpretation records; reaction snapshots have no model fields.
- Preserve the difference among absent legacy field, explicit `null`, empty list, and integer zero.

- [x] **Step 1: Write JSON Schema tests** for each reaction state and malformed counts/IDs.
- [x] **Step 2: Verify RED** on missing schema/validator.
- [x] **Step 3: Implement Draft 2020-12 schema and a small validation wrapper** without data coercion.
- [x] **Step 4: Verify that legacy records validate as `not_collected` only when the new field is absent**, and that an explicit `not_reported` never becomes `empty`.
- [x] **Step 5: Run contract and existing comment-analysis tests.**

### Task 4: Build target-linked comment interpretation adapters

**Files:**
- Create: `src/analysis/audience_response.py`
- Create: `tests/test_audience_response.py`
- Modify: `docs/specs/audience-response-v1.md`

**Interfaces:**
- Normalize model/rule output into records containing `interpretation_id`, `comment_id`, `target_id`, `dimension`, `label`, `language`, `model_id`, `model_version`, `context_ids`, `evidence_span`, optional validated `context_evidence_span`, `score_kind`, and `abstention_reason`.
- `dimension` is one of `topic`, `claim`, `stance`, `sentiment`, `emotion`, or `hostility`; scores are not probabilities unless independently calibrated.
- `target_id` must resolve to an existing `Claim`, `Entity`, `Event`, or versioned registered target.

- [x] **Step 1: Write tests** for multi-target comments, context-only replies, sarcasm/unclear stance abstention, no-text emoji comments, mixed Ukrainian/Russian text, and invalid target IDs.
- [x] **Step 2: Verify RED** on missing adapter.
- [x] **Step 3: Implement only validation, provenance, and abstention contracts**; keep each classifier behind a versioned adapter so providers can be swapped. **No semantic classifier is implemented by this task.**
- [x] **Step 4: Add deterministic eligibility checks** for empty/emoji-only text; emoji-only comments abstain for sentiment and emotion regardless of parent context, while context-linked topic/claim/stance/hostility labels require a validated text-bearing context span.
- [x] **Step 5: Verify all interpretations retain parent/post context references and exact source spans.**

- One interpretation row represents one `(comment_id, target_id, dimension, label, model_id, model_version)` result; multiple targets or labels use multiple rows. `context_ids` reference the source post and parent/reply context used, `evidence_span` uses Unicode codepoint offsets into the comment text, and optional `context_evidence_span` uses offsets verified against caller-supplied context text. Context text cannot establish sentiment or emotion for an emoji-only comment.

### Task 5: Implement frame-conditional aggregation and temporal summaries

**Files:**
- Create: `src/analysis/audience_aggregation.py`
- Create: `tests/test_audience_aggregation.py`
- Modify: `docs/specs/audience-response-v1.md`

**Interfaces:**
- `aggregate_audience(comments, interpretations, reaction_snapshots, unit, time_bins, sensitivity) -> dict` supports `comment`, `author`, `thread`, and `channel` units. `unit` must be one of those literal strings; `time_bins` is a positive integer number of seconds or null; `sensitivity` contains explicit booleans for `deduplicate_exact`, `cap_author_contribution`, and `exclude_candidate_coordination`.
- Every reported proportion includes numerator, denominator, included/excluded record counts, reaction state coverage, and sampling-frame limitation.
- Return a stable JSON object with `schema_version`, `frame`, `unit`, `time_bins`, `groups[]`, `sensitivity`, and `limitations[]`. Each group contains `period_start_utc`, `target_id`, `dimension`, `label`, `numerator`, `denominator`, `proportion`, `comments_n`, `authors_n`, `threads_n`, `channels_n`, and `reaction_state_counts`.
- Reaction-based metrics are descriptive engagement measures; no reaction-weighted stance estimate is named public support.

- [x] **Step 1: Write tests** for 100 comments from one author, missing/hidden/zero reactions, multiple targets, duplicate text, threads with no replies, and reaction snapshots captured at different times.
- [x] **Step 2: Verify RED** for each aggregation contract.
- [x] **Step 3: Implement descriptive counts, proportions, concentration and within-platform time bins.**
- [x] **Step 4: Add sensitivity views** for comment/author/thread/channel weighting, duplicate removal, high-activity caps, and suspected-coordination inclusion/exclusion scenarios.
- [x] **Step 5: Add tests proving non-probability/selected comment frames do not emit population language or population confidence intervals.**

### Task 6: Add quality gates and report integration

**Files:**
- Modify: `src/analysis/report_generator.py`
- Modify: `src/analysis/evaluation_harness.py`
- Create: `tests/test_audience_response_reporting.py`
- Modify: `docs/specs/audience-response-v1.md`

- [x] **Step 1: Write report tests** that reject unsupported denominator-free percentages, targetless stance claims, cross-platform reaction comparisons with incompatible semantics, missing model provenance, and reaction language that claims population support.
- [x] **Step 2: Verify RED** for each guard.
- [x] **Step 3: Add the dedicated report views** for target×stance distribution, topic×emotion co-occurrence conditioned on both outputs for the same target, and within-platform ranking of comments with the largest complete available reaction counts. Each view states its unit and denominator; multilabel cells are marked as overlapping. Hostility remains separate from stance disagreement and no unvalidated scalar polarization score is emitted; platform sections and reaction ranks remain separate by platform. The views omit comment text and identifiers.
- [x] **Step 4: Test an end-to-end synthetic report** with model/version provenance and visible abstentions.
- [x] **Step 5: Run the full suite and obtain a scoped independent code review.** Review passed for the compact views and contract fixes. Keep semantic quality `not_evaluated` where no local gold annotations exist.

### Task 7: Bounded no-identity MTProto pilot

**Files:**
- Create: `reports/audience-response/telegram-reaction-pilot-2026-11-08.md`
- Inputs: existing public Telegram discussion comments; no raw text or identifiers in the receipt.

- [x] Request aggregate reaction objects for at most 10 comments from at most 3 already-collected linked discussion threads. Do not fetch reactor lists. Use the already authorized Telethon user session, set no long flood-wait sleep, and stop on the first rate-limit response. Pilot used one thread, read 10 messages, and requested one comment ID.
- [x] Record only request counts, success/error codes, reaction-state category counts, whether `min` appeared, and whether reaction types included standard/custom/paid categories. Do not record emoji-to-comment mappings, account IDs, peer IDs, text, or session details.
- [x] Access succeeded, so the failure-only branch did not apply. No retry or scope expansion occurred.
- [x] Compare newly saved private typed current-message rows with live `messages.getMessagesReactions` responses. The state and canonical type/count vectors matched exactly for 10/10 comments across three linked discussion threads; content-free receipt: `reports/audience-response/telegram-reaction-parity-2026-11-08.md`. The historical 6 November rows have only scalar totals; later values are not comparable as same-time parity and cannot establish a reaction history.
- [x] Repeat the parity check on a bounded set of messages across multiple linked discussion groups; do not poll and do not collect reactor identities. The selected convenience sample covered only the `available` state; `empty`, `current_user_excluded`, and `not_reported` states remain to be checked in a later test.

---

## Self-review against the DR4 assessment

- Separates topic, claim, stance, sentiment, emotion, hostility, interaction, and engagement.
- Uses existing Social Claim/Entity/Event identifiers for targets.
- Preserves platform reaction semantics and never equates reaction count with support.
- Includes comment/author/thread/channel denominators, selected-frame limits, duplicate/coordination sensitivity, and temporal snapshots.
- Provides an autonomous per-incident path while retaining a frozen validation set and external audit as development-time quality controls.
- Current P0 preserves reaction types already present in MTProto `MessageReactions`; bounded refresh is separate and limited to completeness checks or explicit snapshot runs.

### Task 8: Close independent W14 review findings and add compact analytical views

**Files:**
- Modify: `schemas/comment_reaction_snapshot.schema.json`
- Modify: `src/analysis/audience_response_contracts.py`
- Modify: `src/analysis/audience_response.py`
- Modify: `src/analysis/audience_aggregation.py`
- Modify: `src/analysis/audience_response_reporting.py`
- Modify: `docs/specs/audience-response-v1.md`
- Modify: tests for the above contracts, aggregation, and reporting

**Acceptance requirements:**
- Allow a `current_user_excluded` snapshot with an explicitly empty observed vector; continue to reject an empty `available` vector.
- Emoji-only comments must abstain for sentiment and emotion even when separate parent/context text is supplied; context-linked topic/claim/stance/hostility labels require a validated text-bearing context span.
- Reject known lexical forms of unqualified Ukrainian and Russian population-level phrasing in report labels and document that this regex is not a semantic guarantee.
- Add compact per-platform report views for (a) target-by-stance distribution, (b) topic/emotion co-occurrence conditioned on comments with both outputs for the same target, and (c) comments with the largest available reaction counts. State the exact unit and denominator; overlapping multilabel cells must be marked as overlapping. Rank only within each platform; do not imply exposure-adjusted engagement or population support.
- Show observed hostility labels separately from stance disagreement. Do not add a scalar polarization score without a validated measure.
- Avoid emitting raw comment text, user identifiers, or unsupported classifier accuracy claims. Preserve `semantic_quality_status=not_evaluated`.

- [x] Write focused tests for all four independent review findings; verify each fails for the expected behavior before implementation.
- [x] Implement the smallest contract, aggregation, and renderer changes that pass those tests.
- [x] Update the W14 spec and mark Task 6 Step 3 complete only after the required views are present with correct limits.
- [x] Run W14 focused tests and full suite, pass `git diff --check`, and obtain a scoped independent re-review. Final run: 657 passed, 16 subtests; reviewer passed all four findings and Task 6 Step 3. Population-language matching remains a documented lexical heuristic, not semantic assurance.
