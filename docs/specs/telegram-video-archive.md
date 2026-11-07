# Resumable Telegram Video Archive

`src/telegram_video_archive.py` resumes downloads from a per-post JSONL manifest created from public Telegram channel posts. It stores one binary per Telegram document ID while retaining one row per source post.

## Integrity and access policy

- Downloaded bytes are written to a unique sibling `.part` file. The temporary file is published to the media directory only if its byte count matches Telegram's declared document size; SHA-256 is then recorded.
- Existing files are reused only after size and, when present, SHA-256 match. Invalid partial files are moved to `partial_downloads/` before retry.
- Manifest and summary checkpoints are atomically replaced. Progress is recorded by post-level status; unique document counts are reported separately.
- A cached public channel ID is preferred. If absent, the collector resolves the public username normally. It does not access private channels, bypass restrictions, or store exception text that could expose session information.
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

The manifest is the checkpoint. Re-running verifies existing media and attempts only unresolved or missing file IDs. `download_verified` means byte integrity passed; it does not verify recording time, location, scene identity, caption accuracy, or claim truth.
