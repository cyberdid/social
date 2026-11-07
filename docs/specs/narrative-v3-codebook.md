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

The legacy `src/analysis/narratives.py` codebook is a separate module and is
not imported or changed by v3.

## Output fields

| Field | Meaning |
| --- | --- |
| `mentions` | Ordered tuple of literal topic/issue spans matched by the fixed vocabulary. A mention alone is not a claim. |
| `claim` | Candidate proposition span when at least one recognized mention and one recognized claim predicate occur. Simple quote, attribution, denial, and debunk wrappers are peeled where the rule can identify the span. |
| `speaker` | Text captured after `за словами`, `по словам`, `зі слів`, `со слов`, `за даними`, or `по данным`; otherwise `None`. This is string capture, not identity resolution. |
| `commitment` | Surface relation to the candidate: `direct_assertion`, `attributed`, `quoted`, `denial`, `debunk`, `unclear`, or `none`. |
| `stance_to_claim` | `support` only for an unquoted, unhedged, non-attributed direct assertion; `oppose` for a recognized explicit denial or debunk; otherwise `unclear` or `not_applicable`. |
| `truth_state` | Always `unverified`. This module never verifies a proposition. |
| `classifier_status` | Always `candidate_only`. This is a review aid, not a validated classifier. |

Stance is relative to the candidate proposition, not to the author's general
political position. A reported or quoted claim is not treated as endorsed.
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
| `По словам Ивановой, в подвале держат людей.` | Claim: `в подвале держат людей.`; speaker: `Ивановой`; commitment: `attributed`; stance: `unclear`. |
| `«В подвале держат людей», — пишут в сети.` | Claim: `В подвале держат людей`; commitment: `quoted`; stance: `unclear`. |
| `Возможно, людей удерживают в подвале.` | Claim candidate found; commitment: `unclear`; stance: `unclear`. |
| `Это не фейк: в подвале держат людей.` | Claim candidate found; negated debunk cue makes commitment and stance `unclear`; it is not labeled `support`. |
| `ТЦК утримує людей у підвалі?` | Question; commitment and stance: `unclear`. |
| `ТЦК утримує людей у підвалі. Це неправда.` | Multiple sentences; commitment and stance: `unclear`. |
| `Завтра матч начнётся в восемь.` | No recognized topic/claim; no classification; stance: `not_applicable`. |

Abstention is expected for mixed or compound statements, sarcasm, indirect
endorsement, nested quotation, negation scope the rules do not recognize,
multiple claims with different stances, and terms outside the fixed lists.

## Rule precedence

For a recognized claim candidate, the classifier applies these safety rules
before assigning direct support:

1. Questions and multi-sentence text are `unclear`.
2. Any quote mark makes the candidate `quoted` with `unclear` stance.
3. Attribution markers make it `attributed` with `unclear` stance; an extractable
   speaker is preserved as text.
4. Hedges make it `unclear`.
5. A negated debunk cue makes it `unclear`.
6. A recognized debunk cue makes it `debunk` / `oppose`.
7. A recognized `не + predicate` form makes it `denial` / `oppose`.
8. Other recognized negation makes it `unclear`.
9. Only a recognized direct assertion with none of the preceding cues gets
   `direct_assertion` / `support`.

This precedence is deliberately conservative. It may abstain when a human
reader can infer the author's intent, and it can misread out-of-scope language.
Use these annotations to select or organize material for human review, not as
standalone evidence or a population-level measure.
