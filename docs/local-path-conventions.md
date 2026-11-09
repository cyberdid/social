# Local path conventions

Tracked reports and manifests must not depend on one workstation's `/home/<user>` path.

## Repository-relative paths

Files inside the checkout are recorded from the repository root, for example `reports/source-watch/latest.json` or `data/raw/...`. Set `SOCIAL_REPO_ROOT` only when a command needs an absolute checkout path, such as the source-watch cron job.

## Private data roots

Private media and analysis files remain outside Git. Historical receipts use symbolic roots where needed:

| Placeholder | Meaning |
|---|---|
| `$SOCIAL_REPO_ROOT` | Local clone of this repository |
| `$SOCIAL_MEDIA_ROOT` | Private incident media directory, commonly `Downloads/SocialIncidentVideos` |
| `$SOCIAL_ANALYSIS_ROOT` | Private analysis outputs, commonly `Downloads/SocialIncidentAnalysis` |
| `$DOWNLOADS_ROOT` | User's Downloads directory |
| `$DOCUMENTS_ROOT` | User's Documents directory |
| `$USER_HOME` | User's home directory |

In archived JSON and Markdown, these are provenance placeholders; they are not necessarily expanded by a shell. Active ASR tooling accepts `SOCIAL_ASR_RAW_PATH` and `SOCIAL_ASR_SECOND_PASS_PATH`. The transcript integrity tests also accept `SOCIAL_MEDIA_ROOT` and default to `~/Downloads/SocialIncidentVideos` when it is unset. Missing private inputs remain missing; a path placeholder does not imply that the file is present or verified.
