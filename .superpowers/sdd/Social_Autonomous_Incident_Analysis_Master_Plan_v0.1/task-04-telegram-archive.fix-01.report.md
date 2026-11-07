# Task 04 — Telegram archive fix round 1 report

Implementation commit: `fde6fe4` (`fix: harden resumable Telegram archive statuses`).

- Cached channel IDs now resolve to a current entity that must match the expected public username and broadcast-channel identity before messages can be fetched. Marked negative Telegram channel IDs are checked against the entity's positive ID.
- Per-post `source_status` (and legacy `status`) is separate from `asset_status`. Asset success and failure preserve each row's source status/error. Verified file metadata is linked across all rows sharing a Telegram file ID, and unresolved duplicate source observations are retried on resume.
- Each run writes a JSON receipt under `collection_receipts/` with run ID, collector/version/method, parameters, UTC start/completion, access policy, channel snapshot source/hash, orphan-part count, and per-post attempts/status/error types. Exception messages and session values are not recorded.
- Startup quarantines collector-owned `.tg_*.part` staging files without overwriting prior quarantine files. Summary counts keep source-post counts/statuses separate from unique file-ID and verified-asset counts.
- Added focused tests for entity identity checks, legacy status migration, duplicate asset linking, source/asset status independence, receipt provenance and error sanitization, startup quarantine, and post/file count semantics.

Verification completed:

- `PYTHONPATH=. uv run --with pytest -- python -m pytest tests/test_telegram_video_archive.py -q` — 14 passed.
- `python3 -m py_compile src/telegram_video_archive.py` — passed.
- `git diff --check -- src/telegram_video_archive.py tests/test_telegram_video_archive.py docs/specs/telegram-video-archive.md` — passed.

No network collection was run, and the already-running collector process and its live outputs were left untouched.
