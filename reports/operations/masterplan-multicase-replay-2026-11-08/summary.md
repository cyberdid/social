# Multi-case replay and restore control — 8 November 2026

This is a synthetic software acceptance run. It contains no evidence about the real incident.

- Two isolated synthetic incident IDs each have two immutable as-of snapshots: four snapshots total.
- Replaying an identical case-B cutoff reused its immutable snapshot.
- A copied snapshot registry was restored; all four snapshot SHA-256 values matched and the registry listed four valid snapshots afterward.
- A synthetic correction seeded two changed nodes and the explicit dependency graph identified `b-c-demo` and `b-finding-demo` as downstream candidates.
- Downstream analytical recomputation remains `not executed`; the snapshot module records an invalidation plan and does not dispatch analysis jobs.

The machine-readable aggregate is `acceptance-summary.json`. Full synthetic fixtures and snapshot bytes remain outside Git at `$SOCIAL_ANALYSIS_ROOT/multicase-replay-control-2026-11-08/`.
