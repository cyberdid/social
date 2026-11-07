# Narrative / Claim / Stance v3 codebook

## Purpose and limits

`src.analysis.narrative_v3.classify(text)` is a deterministic, rules-only
baseline for producing candidate annotations for analyst review. It does not
decide whether a claim is true, verified, misleading, or representative of a
whole narrative. Every returned annotation has `truth_state="unverified"` and
`classifier_status="candidate_only"`.

This version has a small Ukrainian/Russian topic vocabulary (TCC/NGU, medics,
doctors, basements, people, custody-related groups, police, and ambulance
terms) and a small predicate vocabulary (holding, restricting access,
torture/assault, death, and concealment forms). The vocabulary is intentionally
incomplete. It is not a general Ukrainian/Russian parser, classifier, or
translation layer. Unknown subjects, paraphrases, inflections, languages, and
compound posts may be missed or abstained on. No independent gold-set
validation has been performed; do not report precision, recall, or agreement.
The Russian torture predicate is constrained to forms such as `пытать`,
`пытают`, and `пытки`; `пытаются` (“they try”) is not a torture cue.

The legacy `src/analysis/narratives.py` codebook is a separate module and is
not imported or changed by v3.

## Output fields

| Field | Meaning |
| --- | --- |
| `source_text` | Exact text passed to `classify`, including leading and trailing whitespace. |
| `evidence_text` | Exact raw evidence span in `source_text`; v3 currently uses the full supplied text so wrappers and stance cues remain visible. |
| `evidence_start`, `evidence_end` | Zero-based, half-open Python string offsets into `source_text`. These delimit `evidence_text` and count Unicode code points. |
| `limitations` | Tuple of stable machine-readable limitation codes, listed below. |
| `mentions` | Ordered tuple of literal topic/issue spans matched by the fixed vocabulary. A mention alone is not a claim. |
| `claim` | Candidate proposition span when at least one recognized mention and one recognized claim predicate occur. Simple quote, reporting, attribution, denial, and debunk wrappers are peeled where the rule can identify the span. Denial normalization or wrapper removal may change it; `source_text` and `evidence_text` preserve the exact input. |
| `speaker` | Text captured after `за словами`, `по словам`, `зі слів`, `со слов`, `за даними`, or `по данным`; otherwise `None`. This is string capture, not identity resolution. |
| `commitment` | Surface relation to the candidate: `direct_assertion`, `attributed`, `reports`, `quoted`, `denial`, `debunk`, `unclear`, or `none`. |
| `stance_to_claim` | `support` only for an unquoted, unhedged, non-attributed direct assertion; `oppose` for a recognized explicit denial or debunk; `reports_no_stance` for a reporting wrapper; otherwise `unclear` or `not_applicable`. |
| `truth_state` | Always `unverified`. This module never verifies a proposition. |
| `classifier_status` | Always `candidate_only`. This is a review aid, not a validated classifier. |

`limitations` currently contains these codes on every annotation:
`deterministic_rules_only`, `narrow_uk_ru_vocabulary`, `candidate_only`,
`no_independent_gold_set_validation`, and `truth_unverified`.

Stance is relative to the candidate proposition, not to the author's general
political position. A reported or quoted claim is not treated as endorsed.
Reporting verbs get the explicit `reports` / `reports_no_stance` labels.
Negation and debunk cues are never assigned `support`. Cases where a rule cannot
reliably tell what is being negated or debunked abstain as `unclear`.
Quoted-span extraction occurs only when the quoted text itself contains both a
recognized topic and claim predicate; quote marks around an isolated term keep
the full candidate span and still force `unclear` stance.

## Positive examples

These are rule demonstrations, not verified facts.

| Text | Candidate output |
| --- | --- |
| `ТЦК утримує людей у підвалі.` | Mentions: `ТЦК`, `людей`, `підвалі`; claim: `ТЦК утримує людей у підвалі.`; commitment: `direct_assertion`; stance: `support`; truth: `unverified`. |
| `В подвале держат людей.` | Mentions: `подвале`, `людей`; claim: `В подвале держат людей.`; commitment: `direct_assertion`; stance: `support`; truth: `unverified`. |

Here `support` means only that the text directly asserts a recognized candidate
proposition. It is not support from evidence and makes no statement about truth.

## Negative examples

| Text | Candidate output |
| --- | --- |
| `В подвале людей не держат.` | Candidate claim: `В подвале людей держат.`; commitment: `denial`; stance: `oppose`; truth: `unverified`. |
| `Сообщение, что людей держат в подвале, — фейк.` | Candidate claim: `людей держат в подвале`; commitment: `debunk`; stance: `oppose`; truth: `unverified`. |

The positive candidate form in the denial example is a simple normalization of
the recognized `не + predicate` pattern. Other forms of negation are not
normalized and fall through to `unclear`.

## Borderline and abstention examples

| Text | Candidate output |
| --- | --- |
| `ТЦК, підвал, медики.` | Topic mentions only; no claim; commitment: `none`; stance: `not_applicable`. |
| `Сообщают, что ТЦК удерживает людей в подвале.` | Claim: `ТЦК удерживает людей в подвале.`; commitment: `reports`; stance: `reports_no_stance`; speaker: `None`. |
| `Повідомили, що ТЦК утримує людей у підвалі.` | Claim: `ТЦК утримує людей у підвалі.`; commitment: `reports`; stance: `reports_no_stance`; speaker: `None`. |
| `По словам Ивановой, в подвале держат людей.` | Claim: `в подвале держат людей.`; speaker: `Ивановой`; commitment: `attributed`; stance: `unclear`. |
| `«В подвале держат людей», — пишут в сети.` | Claim: `В подвале держат людей`; commitment: `quoted`; stance: `unclear`. |
| `Возможно, людей удерживают в подвале.` | Claim candidate found; commitment: `unclear`; stance: `unclear`. |
| `Это не фейк: в подвале держат людей.` | Claim candidate found; negated debunk cue makes commitment and stance `unclear`; it is not labeled `support`. |
| `ТЦК утримує людей у підвалі?` | Question; commitment and stance: `unclear`. |
| `ТЦК утримує людей у підвалі. Це неправда.` | Multiple sentences; commitment and stance: `unclear`. |
| `Людей не держат в подвале, а пытают.` | Multiple candidate predicates; claim preserves the raw statement; commitment and stance: `unclear` rather than applying denial normalization to only the first predicate. |
| `Медики пытаются уйти из подвала.` | Topic mentions only; `пытаются` is not a torture predicate, so no claim is emitted. |
| `Завтра матч начнётся в восемь.` | No recognized topic/claim; no classification; stance: `not_applicable`. |

Abstention is expected for mixed or compound statements, sarcasm, indirect
endorsement, nested quotation, negation scope the rules do not recognize,
multiple claims with different stances, and terms outside the fixed lists.

## Rule precedence

For a recognized claim candidate, the classifier applies these safety rules
before assigning direct support:

1. Questions, multi-sentence text, and text with multiple recognized claim
   predicates are `unclear`; multiple predicates keep the raw candidate text
   rather than normalizing only one of them.
2. Any quote mark makes the candidate `quoted` with `unclear` stance.
3. Explicit reporting verbs such as `сообщают` and `повідомляють` make it
   `reports` / `reports_no_stance`.
4. Attribution markers make it `attributed` with `unclear` stance; an extractable
   speaker is preserved as text.
5. Hedges make it `unclear`.
6. A negated debunk cue makes it `unclear`.
7. A recognized debunk cue makes it `debunk` / `oppose`.
8. A recognized `не + predicate` form makes it `denial` / `oppose`.
9. Other recognized negation makes it `unclear`.
10. Only a recognized direct assertion with none of the preceding cues gets
   `direct_assertion` / `support`.

This precedence is deliberately conservative. It may abstain when a human
reader can infer the author's intent, and it can misread out-of-scope language.
Use these annotations to select or organize material for human review, not as
standalone evidence or a population-level measure.
