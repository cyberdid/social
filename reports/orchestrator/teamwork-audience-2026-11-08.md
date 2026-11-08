# W14 Audience Response Intelligence & MTProto Telemetry Closeout Report

**Date:** 8 November 2026  
**Author:** Worker M4 (Audience and W14 Analyst), Social Master Plan Closeout  
**Component:** W14 — Audience Response Intelligence Engine  
**Working Directory:** `/home/cyberdid/Projects/Social/.worktrees/social-master-plan`  
**Reference Specs & Reviews:**
- Specification: `docs/specs/audience-response-v1.md`
- Core Modules: `src/analysis/audience_aggregation.py`, `src/analysis/audience_response_contracts.py`, `src/analysis/audience_response_reporting.py`, `src/analysis/telegram_reaction_snapshots.py`
- Test Suites: `tests/test_audience_aggregation.py`, `tests/test_audience_response_contracts.py`, `tests/test_audience_response.py`, `tests/test_audience_response_reporting.py`, `tests/test_telegram_reaction_snapshots.py`
- Deep Research Foundation: `docs/research/DR4-audience-response-2026-11-08.md`
- External Peer Review: `docs/research/DR4-review-received-2026-11-08.md` (Reviewer score: 89/100)
- Technical Telegram Notes: `docs/research/telegram-reaction-units-and-privacy-2026-11-08.md`, `reports/audience-response/telegram-reaction-parity-2026-11-08.md`, `reports/audience-response/telegram-reaction-pilot-2026-11-08.md`

---

## 1. Executive Summary & Gate Status

This report delivers the comprehensive technical and methodological audit for **Milestone M4 (Audience and W14 Analysis)** under the Social Master Plan v1.1 closeout. It documents the resolution of the code-backed unit mixing defect in reaction aggregation, verifies MTProto reaction state-machine telemetry, evaluates repeat-snapshot feasibility, audits multi-estimand denominators and exposure bias, assesses target-linking boundaries to the Evidence Graph, and establishes sensitivity controls for commenter dynamics.

### Acceptance Gate Status Summary

| Workstream Gate | Target Requirement | Evaluation Status | Empirical Receipt / Evidence Locator |
|---|---|---|---|
| **P0.8 Reaction Capture Architecture** | MTProto typed reactions schema 1.1 with backward compatibility | **CLOSED (Architecture & Contracts)** | `schemas/comment_reaction_snapshot.schema.json`, `src/analysis/audience_response_contracts.py` (92/92 audience tests pass) |
| **P0.8 Reaction Currency Decoupling** | Decouple paid Telegram Stars from emoji counts in rankings | **CLOSED (Defect Resolved & Verified)** | `src/analysis/audience_aggregation.py` lines 135–236, `tests/test_audience_aggregation.py` |
| **P0.8 Live MTProto Parity** | 10/10 live API parity check on discussion comments | **CLOSED (Bounded Sample 10/10)** | `reports/audience-response/telegram-reaction-parity-2026-11-08.md` (SHA-256 `aca8d40e9e6fc306ee7f9830ac937b0d81916b3acf157cf0a5051b14e42945df`) |
| **P0.8 Corpus Backfill Boundary** | Historical 39,598-comment corpus backfill | **CLOSED (Definitive Boundary: Irrecoverable)** | 6 Nov 2026 snapshot contains scalar legacy sums only; cannot be backfilled with emoji types |
| **P1.0 Local Semantic Classifiers** | Benchmark sentiment/stance/emotion on Ukrainian/Russian/mixed text | **OPEN (Methodological Spec Complete; Models Unevaluated)** | `semantic_quality_status: not_evaluated` preserved in all aggregates; zero unvalidated claims |
| **P1.0 Longitudinal Reaction Series** | Time-series repeat snapshots across 533 threads | **OPEN (Requires Bounded Scheduler & Quota)** | Single snapshot verified; longitudinal series requires rate-limited multi-pass scheduler |
| **Privacy & Anti-Generalization** | Zero reactor identity collection, lexical population check | **ENFORCED (Strict Invariant)** | `getMessageReactionsList` prohibited; `_UNQUALIFIED_POPULATION` validator active |

---

## 2. Code Defect Resolution: Telegram Star Currency Decoupling

### 2.1. Nature of the Defect
In Telegram MTProto, message reactions can be of multiple distinct types:
1. `reactionEmoji`: Standard Unicode emoji reactions (e.g. 👍, 🔥, ❤️).
2. `reactionCustomEmoji`: Premium custom document emoji.
3. `reactionPaid`: Telegram Stars paid reactions, introduced in Telegram Bot/Client API 2024. Sending a paid reaction with an amount $N$ increments the reaction counter by $N$ Stars in a single interaction.

Prior to this fix, `src/analysis/audience_aggregation.py` lines 208–217 computed the `largest_available_reaction_comments` ranking by iterating over the `reaction_breakdown` list and indiscriminately summing all `item["count"]` values into `total += count`. Because paid Telegram Star quantities represent financial currency amounts (where 1 user can spend 100 or 1,000 Stars on a single message), this composite sum mixed non-comparable units (currency Stars vs emoji reactions). A comment with 1,000 paid Stars and zero emoji reactions would be ranked #1 above comments with substantial organic emoji engagement, distorting descriptive comment rankings.

### 2.2. Mathematical Formulation & Implementation
We decoupled the reaction vector into orthogonal measurement units:
$$\text{Vector}(c) = \big(\text{emoji}, \text{custom\_emoji}, \text{paid}, \text{unknown}\big)$$

1. **Non-Paid Emoji Reaction Count ($R_{\text{non-paid}}$):**
   $$R_{\text{non-paid}}(c) = \sum_{r \in \text{breakdown}(c),\, \text{kind}(r) \in \{\text{emoji}, \text{custom\_emoji}\}} \text{count}(r)$$
2. **Paid Telegram Star Amount ($S_{\text{paid}}$):**
   $$S_{\text{paid}}(c) = \sum_{r \in \text{breakdown}(c),\, \text{kind}(r) = \text{paid}} \text{count}(r)$$
3. **Unknown Constructor Count ($U_{\text{unknown}}$):**
   $$U_{\text{unknown}}(c) = \sum_{r \in \text{breakdown}(c),\, \text{kind}(r) = \text{unknown}} \text{count}(r)$$

The implementation introduces two explicit functions in `src/analysis/audience_aggregation.py`:
- `separate_reaction_breakdown(breakdown: list[Mapping[str, Any]]) -> dict[str, int]`:
  Strictly segregates `non_paid_reaction_count`, `paid_star_amount`, and `unknown_reaction_count`, supporting both `kind` and `reaction_type` keys.
- `largest_available_reaction_comments(comments, top_k=10, snapshots_by_comment=None, *, include_paid=False)`:
  Ranks comments strictly descending by $R_{\text{non-paid}}$ (tie-broken by `comment_id` ascending). The emitted dictionaries preserve exact set equality with `_REACTION_RANK_FIELDS` (`{"platform", "rank", "unit", "reaction_count", "denominator", "denominator_basis"}`), ensuring 100% compliance with `validate_audience_aggregate` and `render_audience_response_markdown`.

### 2.3. Verification & Regression Coverage
Regression tests added to `tests/test_audience_aggregation.py`:
- `test_separate_reaction_breakdown_decouples_stars_and_unknowns`: Verifies vector separation across emoji, custom emoji, paid Stars, and unknown reaction constructors.
- `test_separate_reaction_breakdown_validates_counts`: Validates error handling for negative, non-integer, or empty inputs.
- `test_paid_star_reactions_do_not_distort_comment_rankings`: Verifies that a comment with 500 paid Stars and 2 emojis ranks at Rank 3, while a comment with 10 emojis and 0 Stars ranks at Rank 1, and a comment with 1,000 Stars and 0 emojis ranks at Rank 4.
- `test_largest_available_reaction_comments_direct_call_and_include_paid`: Verifies direct invocation, schema compatibility, and the optional `include_paid=True` parameter.

All 92 tests in the audience test suite (`tests/test_audience*.py` and `tests/test_telegram_reaction_snapshots.py`) pass in 0.16 seconds, and all 687 tests across the repository pass without regression.

---

## 3. MTProto Aggregate Telemetry and Live Parity Analysis

### 3.1. Telemetry State Machine
Telegram MTProto exposes comment reactions through discussion supergroups. W14 implements an explicit 5-state reaction state machine:
1. `not_collected`: Legacy record where reaction collection was not attempted or fields are absent.
2. `not_reported`: The MTProto `Message` object lacked a `MessageReactions` structure (meaning no reaction object returned).
3. `empty`: A `MessageReactions` object was returned with `results = []` and `min = False`.
4. `available`: A complete, non-empty reaction breakdown vector was observed with `min = False`.
5. `current_user_excluded`: `MessageReactions.min = True`. The aggregate may omit the authorized account's own reaction; it is stored as partial and excluded from descriptive non-paid rankings.

### 3.2. Bounded Refresh Adapter Outcomes
When refreshing reaction telemetry via `messages.getMessagesReactions(peer, ids)`, four explicit request statuses are recorded:
- `ok`: A matching `updateMessageReactions` was received for the target message ID.
- `no_update`: The API responded with updates, but none matched the requested message ID.
- `wrong_peer_update`: An update was received for the requested message ID, but belonging to a different peer.
- `request_failed`: Network error, authorization failure, or `FLOOD_WAIT`.

Crucially, `no_update` and `wrong_peer_update` carry `reaction_state = None` and `reaction_breakdown = None`. They do NOT overwrite prior successful observations or synthesize artificial zeroes.

### 3.3. 10/10 Live Parity Verification Receipt
The live parity check conducted on 8 November 2026 through the authorized user session (`reports/audience-response/telegram-reaction-parity-2026-11-08.md`) established:
- **Sample:** 10 public comments across 3 linked discussion threads.
- **Collector vs API:** 10/10 collector-serialized rows matched the live `messages.getMessagesReactions` vector byte-for-byte in canonical ordering.
- **State Observed:** 10/10 observed in `available` state.
- **Private Receipt:** Maintained at `/home/cyberdid/Downloads/SocialIncidentAnalysis/audience-response/telegram-reaction-parity-10-2026-11-08/private_snapshots.jsonl` (file mode `0600`, dir mode `0700`, SHA-256 `aca8d40e9e6fc306ee7f9830ac937b0d81916b3acf157cf0a5051b14e42945df`).
- **Scope Limit:** This convenience sample verified live parity for `available` states in 3 threads. It does NOT establish empirical parity for `empty`, `current_user_excluded`, or rate-limited states across the remaining 530 threads.

### 3.4. Repeat-Snapshot Feasibility & Quota Analysis
Telegram MTProto does not provide a historical reaction log or timeseries API. Each query returns the instantaneous snapshot. To evaluate the feasibility of repeat-snapshot collection across the 533-thread panel (comprising 39,598 comments):
- **Rate Limit Constraints:** MTProto user sessions enforce strict flood-wait controls. Calling `messages.getMessagesReactions` in tight loops results in `FLOOD_WAIT_X` penalties ranging from seconds to hours.
- **Cadence Feasibility:** Client UI behavior (short polling every 15–30 seconds) is technically impossible and methodologically unjustified for research panels.
- **Recommended Cadence:** A bounded batch runner requesting up to 100 message IDs per call (`messages.getMessagesReactions(peer, ids=[...])`) with randomized exponential backoff (inter-batch delays of 2–5 seconds) could snapshot active threads at 6-hour or 24-hour intervals. However, historical data from 6 November cannot be retrieved retroactively.

---

## 4. Denominators, Estimands, and Exposure Bias Audit

### 4.1. The Denominator Taxonomy
As underscored in Deep Research №4 and the peer review (`docs/research/DR4-review-received-2026-11-08.md`), every audience statistic must declare its estimand and exact denominator. Audience aggregation supports four distinct units:

| Unit Estimand | Numerator Definition | Denominator Definition | Substantive Meaning |
|---|---|---|---|
| `comment` | Comments with label for target | All comments with any interpretation for target | Proportion of expressed comment volume |
| `author` | Authors with at least 1 comment with label | Authors with at least 1 comment evaluated for target | Proportion of participating comment authors |
| `thread` | Threads containing at least 1 label | Threads with at least 1 comment evaluated for target | Pervasiveness of stance across discussions |
| `channel` | Channels containing at least 1 label | Channels with at least 1 comment evaluated for target | Distribution of stance across source channels |

### 4.2. Multilabel Overlap & Proportion Basis
Because a single comment (or author) can address multiple aspects of a target, express mixed sentiments, or evolve over time:
- Stance, topic, and emotion labels are explicitly flagged with `labels_may_overlap: true`.
- Numerators for a given target do not necessarily sum to the denominator; proportions represent marginal coverage, not mutually exclusive shares of a 100% pie.
- Abstentions remain in the denominator (`proportion_basis = "units with label divided by units with any output for this target and dimension; abstentions remain in the denominator"`), preventing artificial inflation of stance proportions.

### 4.3. Exposure Bias in Social Media Comments
A critical finding of W14 is that comment reaction counts cannot be normalized into "percentage of viewers who agree":
1. **Unavailable Impression Data:** MTProto provides message view counts for channel posts, but does NOT provide per-comment impression counters in discussion supergroups.
2. **Algorithmic & Chronological Exposure:** Top-level comments posted early receive orders of magnitude more impressions than late replies buried deep in threads.
3. **Engagement vs Endorsement:** A reaction (such as 👍, 😢, or 😡) reflects a platform engagement action, not a verified vote on the substantive truth or legal merit of claims in the text.
4. **Ranking Disclaimer:** The `largest_available_reaction_comments` table is explicitly bounded:
   `"Rank is within this platform among comments whose latest selected reaction snapshot is available. Counts are not exposure-adjusted engagement or population support."`

---

## 5. Target Linking to Claims, Entities, and Events

### 5.1. Integration with the Evidence Graph
W14 requires that every interpretation row links to a canonical identifier from the Evidence Graph:
- `target_id`: Must resolve to a versioned `Claim` (e.g. `claim:action`), `Entity` (e.g. `entity:police`), or `Event` (e.g. `event:clash_1800`).
- **Prohibition of Broad Ambiguous Targets:** As emphasized by the DR4 reviewer, broad targets such as general "attitude to police" or "sentiment on authorities" are prohibited. Stance and sentiment must bind to specific actions, statements, or events.

### 5.2. Multi-Dimensional Orthogonality
W14 separates audience response into six independent dimensions:
1. `topic`: What substantive subject is discussed (e.g. `security`, `procedure`, `protest`).
2. `claim`: What factual assertion is made or evaluated.
3. `stance`: The author's position toward the target (`favor`, `against`, `neutral`, `no_stance`, `mixed`).
4. `sentiment`: The affective valence toward the target (`positive`, `negative`, `neutral`, `mixed`).
5. `emotion`: Expressed discrete emotions (`anger`, `fear`, `sadness`, `joy`, `solidarity`).
6. `hostility`: Incivility, toxicity, or abusive language (`hostile_language`, `threat`, `none`).

**Core Invariant:** Hostility is NOT stance disagreement; negative sentiment toward an event is NOT opposition to a claim; reactions are NOT endorsement.

### 5.3. Emoji-Only Comments & Affective Abstention Contract
Under `src/analysis/audience_aggregation.py` and `audience-response-v1.md`:
- Emoji-only comments (e.g. comments consisting solely of 👍, 🤮, or 🇺🇦) must abstain from sentiment and emotion (`label = "abstain"`).
- Sarcasm, irony, and contextual ambiguity mean that an emoji written in isolation cannot establish the commenter's internal emotional state.
- While a text-bearing context span from a parent comment may justify a topic or stance label under strict conditions, the emoji alone cannot support an affect finding.

---

## 6. Sensitivity Controls for Hyperactive & Coordinated Dynamics

Rather than permanently deleting suspicious comments (which risks selection bias and conceals platform manipulation dynamics), W14 provides three orthogonal sensitivity parameters:

```python
sensitivity = {
    "deduplicate_exact": True,
    "cap_author_contribution": True,
    "exclude_candidate_coordination": True,
}
```

### 6.1. Exact Text Deduplication (`deduplicate_exact`)
- **Mechanism:** Normalizes text (casefolded, whitespace-collapsed) for comments with length $\ge 20$ characters. Within a given `(platform, thread_id)` partition, only the earliest comment by timestamp is retained; subsequent duplicates are excluded.
- **Boundary Invariant:** Deduplication never crosses platform boundaries (`test_exact_deduplication_never_crosses_platform_boundaries`). A comment copied on YouTube and Telegram is retained in both platform frames.
- **Reporting:** Excluded counts are recorded under `frame.comments_excluded.exact_duplicate`.

### 6.2. Author Volume Capping (`cap_author_contribution`)
- **Mechanism:** Hyperactive commenters who flood discussions can skew comment-weighted aggregations. When enabled, this filter caps each author pseudonym to their chronologically earliest comment per `(period_start_utc, target_id, dimension)`.
- **Handling Unattributed Authors:** Comments lacking an author pseudonym (`author = None`) cannot be grouped by author; they are preserved without dropping, and tracked under `unit_missing_excluded_n` when running in `unit="author"` mode.
- **Reporting:** Dropped group memberships are recorded in `frame.author_cap_dropped_group_memberships`.

### 6.3. Upstream Coordination Exclusion (`exclude_candidate_coordination`)
- **Mechanism:** Excludes comments where upstream coordination detection flagged `is_candidate_coordination: True` (from LSH/MinHash text reuse or timing synchronization in `src/analysis/coordination_null_models.py`).
- **Analytical Purpose:** Allows analysts to compare the baseline stance distribution against a "coordination-filtered" stance distribution. If a narrative disappears when coordination is excluded, the signal was driven by coordinated activity rather than diverse participation.
- **Reporting:** Excluded counts are tracked under `frame.comments_excluded.candidate_coordination`.

---

## 7. Review of Deep Research №4 & Peer Feedback Integration

In accordance with dispatch item 5, this report incorporates the findings and recommendations from the peer review of DR4 (`docs/research/DR4-review-received-2026-11-08.md`, reviewer rating **89/100**):

| Reviewer Recommendation | Addressed in Social Implementation | Status & Remaining Limitations |
|---|---|---|
| **1. Separate MTProto reactions breakdown & permissions** | Implemented typed representation (`emoji`, `custom_emoji`, `paid`, `unknown`) and 5 reaction states + 4 request outcomes. Currency decoupled in aggregation. | **Complete for Architecture & Bounded Pilot**. Live parity checked on 10 comments; full 533-thread panel not re-crawled. |
| **2. Local Ukrainian/Russian/mixed classifier benchmarks** | Architecture requires model provenance (`model_id`, `model_version`). Pooling across models is blocked. | **OPEN (Methodology set, models unevaluated)**. No production NLP model evaluated on local gold data; `semantic_quality_status: not_evaluated` enforced. |
| **3. Canonical Evidence Graph targets** | Target IDs validated against versioned Social Claim/Entity/Event schema. Broad targets prohibited. | **Enforced by Schema & Contracts**. |
| **4. Strict Estimands & Denominators** | 4 units (`comment`, `author`, `thread`, `channel`) implemented with explicit denominator basis. Multilabel overlap marked. | **Enforced in Aggregates and Reporting**. |
| **5. Anti-Generalization to Population** | Lexical filter rejects unqualified population claims in UK/RU/EN. Explicit limitations block confidence intervals. | **Enforced by Contract & Validation**. |

---

## 8. Strict Privacy, Security, and Methodological Guardrails

W14 enforces three unbreakable privacy and methodological invariants:

1. **Zero Reactor Identity Collection:**
   - The Telegram API method `messages.getMessageReactionsList` is explicitly prohibited in code and configuration.
   - When MTProto returns `top_reactors` or `recent_reactions` in `MessageReactions`, the serializer ignores them, storing only anonymous aggregate counts.
   - Author IDs are stored solely as one-way HMAC pseudonyms with secret salts residing outside version control in `0600`/`0700` protected paths.
2. **No Equating Reactions to Support Without Context:**
   - Reaction counters represent platform interaction instances, not individual endorsements.
   - Aggregations and markdown tables explicitly disclose that exposure is unmeasured and reactions do not establish factual truth.
3. **Anti-Generalization Population Constraints:**
   - `validate_audience_aggregate` executes a regex scan (`_UNQUALIFIED_POPULATION`) across all rendered labels and titles, blocking phrases like "громадська думка", "населення вважає", "суспільство підтримує", "public opinion", "the population supports".
   - Aggregates describe solely the observed, selected comment frame. No population confidence intervals or sample-to-population weights are permitted.

---

## 9. Conclusion & Handoff Summary

Milestone M4 is fully executed:
1. **Defect Fixed:** Paid Telegram Star currency reactions are decoupled from non-paid emoji reaction counts in `src/analysis/audience_aggregation.py`. Rankings strictly reflect emoji/custom emoji counts without currency distortion.
2. **Regression Tested:** 4 new test suites added in `tests/test_audience_aggregation.py`; full audience suite passes 92/92, full workspace passes 687/687.
3. **Specification Updated:** `docs/specs/audience-response-v1.md` updated with comprehensive unit independence documentation.
4. **Telemetries & Boundaries Documented:** MTProto telemetry, 10/10 parity check, repeat-snapshot constraints, denominators, sensitivity scenarios, and DR4 review feedback fully synthesized.
5. **No PII or Secret Leakage:** Zero reactor identities, tokens, salts, or unpseudonymized records collected or transmitted.
