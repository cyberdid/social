# Local media index

`src/media_pipeline.py` indexes already downloaded media. It performs no HTTP,
API, or credential operations and never writes to the media files. Its JSONL
input contains one object per local file:

```json
{"source_locator":"https://example.invalid/post/1","local_path":"media/clip.mp4","fetched_at":"2026-11-07T12:00:00Z","provenance":{"collector":"example"}}
```

`local_path` is resolved relative to the input manifest when it is not
absolute. URL and FFmpeg protocol paths are rejected. `source_locator`,
`fetched_at`, `provenance`, and any caller supplied `model_observations` are
preserved unchanged under output `source`. Verified facts are separate under
`media_index.verified_media_facts`: SHA-256, byte size, a deterministic
magic/suffix media type, and raw ffprobe JSON when available. Probe and decode
results have their own status objects.

Run `python src/media_pipeline.py INPUT.jsonl OUTPUT.jsonl`; add
`--strict-decode` to decode the entire file with FFmpeg's `-xerror` flag to a
null sink. Missing tools, invalid probe JSON, probe/decode failures, missing
files, changed files, and malformed input rows receive explicit statuses.
Successful unchanged rows are reused by record identity, content digest, and
decode mode. Each completed row is checkpointed; successful completion
compacts checkpoints to one output row per current input line in source order.

The SHA-256 identifies bytes only. ffprobe output records container and stream
metadata; neither it nor the media type establishes authenticity, date,
location, or the truth of any claim. Model observations remain caller supplied
and are not promoted to verified facts.
