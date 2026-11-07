# Task 07 — Social conflict analysis aggregation

## Scope

Implemented a conservative, deterministic aggregator for already extracted event and position records. It does not extract from raw posts, decide truth, infer motives, or establish causation.

## Files

- `src/analysis/conflict_analysis.py`
- `tests/test_conflict_analysis.py`
- `docs/specs/conflict-analysis-v1.md`

## Implemented behavior

- Physical event records and information-attention aggregates are stored separately. The physical action vector is calculated only from evidence-referenced physical records.
- Position statements remain attributed to their stated speaker and source. Representation evidence is recorded when supplied, but this module never uses it to generalize a speaker's statement to a group and never independently validates that evidence.
- Unknown speaker roles remain `unknown`; structural hypotheses remain labeled as hypotheses.
- Records missing evidence references are listed as unresolved and excluded from the analytical groups.
- View counters are explicitly labeled as snapshot counters, not unique people.
- Non-finite (`NaN`, positive infinity, negative infinity) attention metrics are rejected to prevent non-standard JSON and invalid summaries.
- The action and physical-event lists are independent deep copies so downstream edits to one field cannot silently mutate the other.
- Physical event category counts are corpus record counts and do not estimate real-world event frequency or severity.

## Validation

```text
RED: `uv run --with pytest -- python -m pytest -q tests/test_conflict_analysis.py -k 'non_physical or source_receipt'`
    2 failed as expected (communication event admitted to physical input; attention record accepted without source refs).
RED follow-up: `uv run --with pytest -- python -m pytest -q tests/test_conflict_analysis.py -k 'non_finite or do_not_alias'`
    4 failed as expected (NaN/±inf admitted; output lists shared mutable objects).
GREEN: `uv run --with pytest -- python -m pytest -q tests/test_conflict_analysis.py`
    13 passed.
```

Earlier focused run before adding the final two checks: 7 passed. No external services or raw data were used.

## Deliberate limitations

- This does not constitute autonomous conflict-event extraction or an escalation classifier.
- It trusts the supplied event categories and verification statuses while preserving them; it does not independently validate them.
- It does not infer the beginning/end of an episode or claim a whole group holds one position.
- Source lineage and sampling coverage must be supplied by separate stages; unknown lineage remains unknown.

## Review status

Awaiting independent scoped code review.
