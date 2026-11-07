# Resumable Telegram Video Archive

`src/telegram_video_archive.py` resumes downloads from a per-post JSONL manifest created from public Telegram channel posts. It stores one binary per Telegram document ID while retaining one row per source post.

Each manifest row keeps source observation state in `source_status` (also mirrored to the legacy `status` field) and binary integrity state in `asset_status`. Asset failures and successful deduplicated downloads never replace a post's source status or source error. Legacy rows with an overloaded `status` value are normalized when the collector resumes them.

## Integrity and access policy

- Downloaded bytes are written to a unique sibling `.part` file. The temporary file is published to the media directory only if its byte count matches Telegram's declared document size; SHA-256 is then recorded.
- At startup, collector-owned `.tg_*.part` files left in the media staging directory are moved to `partial_downloads/`. Existing files are reused only after size and, when present, SHA-256 match. Invalid completed files are also quarantined before retry.
- One verified file ID links its asset path, byte count, hash, and download time to every manifest row with that ID. The collector still retries unresolved source observations for those rows and keeps their individual source status.
- Manifest and summary checkpoints are atomically replaced. `source_posts` and source-status counts describe post rows; unique file-ID and verified-media counts describe assets.
- A cached channel ID is resolved to its current entity before use. The entity must still have the exact expected public username and be a broadcast channel. A rejected cache entry may fall back to resolving the expected public username, which receives the same validation. Private channels and groups are rejected; the collector does not bypass restrictions.
- Every run writes `collection_receipts/<run-id>.json` beside the manifest. The receipt records the collector version and method, parameters, run timestamps, access policy, channel snapshot source and SHA-256, orphan partial-file count, and per-post attempt/status/error-type records. It stores exception class names only, never exception messages or credentials.
- The receipt's top-level `status` is run-level: `complete` means the collector finished its run, even if individual posts have source or asset errors. Per-post outcomes are recorded separately in each `posts[]` entry's `source_status` and `asset_status`.
- Telegram credentials are loaded through the existing `~/.config/social/telegram.env` configuration and are never copied into the repository or output manifest.
- Downloaded binaries are stored outside the Git repository; the repository contains code, tests, and procedures only.

## Resume command

```bash
uv run --with telethon python src/telegram_video_archive.py \
  --manifest /path/to/SocialIncidentVideos/telegram/manifest.jsonl \
  --media-dir /path/to/SocialIncidentVideos/telegram/media \
  --channel-snapshot /path/to/data/raw/telegram_api/SNAPSHOT/channels.jsonl \
  --concurrency 2 --checkpoint-every 10
```

The manifest is the checkpoint. Re-running verifies existing media and attempts unresolved source observations and missing file IDs. `asset_status: "downloaded_verified"` means byte integrity passed; it does not verify recording time, location, scene identity, caption accuracy, or claim truth.
