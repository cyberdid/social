"""Resumable acquisition of public Telegram video posts already in a manifest.

The collector stores one manifest row per source post and one binary per Telegram
document ID. It never edits source posts or attempts to bypass access controls.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import mimetypes
import os
import re
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, Callable


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_matches(path: str | Path, expected_size: int | None,
                 expected_sha256: str | None = None) -> bool:
    candidate = Path(path)
    if not candidate.is_file() or expected_size is None or expected_size <= 0:
        return False
    if candidate.stat().st_size != expected_size:
        return False
    return not expected_sha256 or sha256_file(candidate).lower() == expected_sha256.lower()


async def download_atomic(
    writer: Callable[[Path], Awaitable[str | Path | None]],
    destination: str | Path,
    expected_size: int,
    expected_sha256: str | None = None,
) -> dict:
    """Download to a sibling temporary file and publish only a verified result.

    ``writer`` must write to the path it receives and return that path (or None).
    An existing destination is retained until the new file passes integrity
    checks, so interrupted downloads cannot replace a known good asset.
    """
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    if file_matches(target, expected_size, expected_sha256):
        return {"status": "existing_verified", "path": str(target),
                "size_bytes": target.stat().st_size, "sha256": sha256_file(target)}
    if expected_size <= 0:
        raise ValueError("expected media size must be positive")

    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".part",
                                     dir=target.parent)
    os.close(fd)
    temporary = Path(temp_name)
    temporary.unlink()
    try:
        result = await writer(temporary)
        written = Path(result) if result else temporary
        if written.resolve() != temporary.resolve():
            raise ValueError("downloader wrote outside the designated temporary path")
        if not written.is_file():
            raise ValueError("downloader returned without creating the temporary file")
        actual_size = written.stat().st_size
        if actual_size != expected_size:
            raise ValueError(f"download size mismatch: expected {expected_size}, got {actual_size}")
        digest = sha256_file(written)
        if expected_sha256 and digest.lower() != expected_sha256.lower():
            raise ValueError("download sha256 mismatch")
        os.replace(written, target)
        return {"status": "downloaded", "path": str(target),
                "size_bytes": actual_size, "sha256": digest}
    finally:
        temporary.unlink(missing_ok=True)


def group_manifest_by_file_id(rows: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        file_id = row.get("telegram_file_id")
        if file_id is not None and str(file_id).strip():
            groups[str(file_id)].append(row)
    return dict(groups)


def read_manifest(path: str | Path) -> list[dict]:
    records = []
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"manifest row {line_number} must be an object")
            records.append(record)
    return records


def write_manifest_atomic(path: str | Path, rows: list[dict]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp",
                                     dir=target.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, target)
    finally:
        Path(temp_name).unlink(missing_ok=True)


def write_json_atomic(path: str | Path, payload: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp",
                                     dir=target.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, target)
    finally:
        Path(temp_name).unlink(missing_ok=True)


def load_channel_ids(path: str | Path | None) -> dict[str, int]:
    if not path or not Path(path).is_file():
        return {}
    result = {}
    with Path(path).open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            record = json.loads(line)
            username, chat_id = record.get("username"), record.get("chat_id")
            if username and chat_id:
                try:
                    result[str(username).lower().lstrip("@")] = int(chat_id)
                except (TypeError, ValueError):
                    continue
    return result


def _safe_error_type(exc: Exception) -> str:
    """Do not persist exception strings, which can contain user/session data."""
    return type(exc).__name__


def _video_document(message):
    from telethon.tl import types

    document = getattr(message, "document", None)
    if document is None:
        return None, None
    attrs = list(getattr(document, "attributes", []) or [])
    video_attr = next((a for a in attrs if isinstance(a, types.DocumentAttributeVideo)), None)
    mime = (getattr(document, "mime_type", None) or "").lower()
    return (document, video_attr) if mime.startswith("video/") or video_attr else (None, None)


def _media_suffix(document) -> str:
    mime = getattr(document, "mime_type", None) or "video/mp4"
    suffix = mimetypes.guess_extension(mime.split(";")[0].strip()) or ".mp4"
    if suffix == ".jpe":
        return ".jpg"
    if not re.fullmatch(r"\.[a-zA-Z0-9]{1,8}", suffix):
        return ".mp4"
    return suffix


def _canonical_path(media_dir: Path, document) -> Path:
    return media_dir / f"tg_{int(document.id)}{_media_suffix(document)}"


def _apply_metadata(row: dict, message, media_dir: Path) -> bool:
    document, video_attr = _video_document(message)
    if document is None:
        old_id = row.pop("telegram_file_id", None)
        old_asset = {key: row[key] for key in ("local_file", "sha256", "file_size_bytes") if row.get(key)}
        if old_id or old_asset:
            row["previous_media_observation"] = {"telegram_file_id": str(old_id) if old_id else None,
                                                 **old_asset}
        for key in ("local_file", "sha256", "file_size_bytes", "duration_seconds", "width",
                    "height", "is_round_video"):
            row.pop(key, None)
        row.update(status="not_video", actual_mime_type=getattr(
            getattr(message, "document", None), "mime_type", None))
        return False
    previous_id = row.get("telegram_file_id")
    file_id = str(document.id)
    if previous_id and str(previous_id) != file_id:
        row["previous_telegram_file_id"] = str(previous_id)
    row.update(
        status="metadata_ok", telegram_file_id=file_id,
        actual_mime_type=getattr(document, "mime_type", None),
        file_size_bytes=int(getattr(document, "size", 0) or 0),
        duration_seconds=getattr(video_attr, "duration", None),
        width=getattr(video_attr, "w", None), height=getattr(video_attr, "h", None),
        is_round_video=bool(getattr(video_attr, "round_message", False)),
        local_file=str(_canonical_path(media_dir, document)),
    )
    row.pop("error_type", None)
    return True


def build_summary(rows: list[dict], manifest_path: Path, media_dir: Path) -> dict:
    status_counts = Counter(row.get("status", "unknown") for row in rows)
    groups = group_manifest_by_file_id(rows)
    verified = set()
    total_verified_bytes = 0
    for file_id, copies in groups.items():
        row = next((r for r in copies if r.get("sha256") and r.get("local_file")), None)
        if row and file_matches(row["local_file"], row.get("file_size_bytes"), row.get("sha256")):
            verified.add(file_id)
            total_verified_bytes += Path(row["local_file"]).stat().st_size
    return {
        "schema_version": "1.0", "updated_at_utc": utc_now(),
        "manifest": str(manifest_path), "media_dir": str(media_dir),
        "source_posts": len(rows), "unique_telegram_file_ids": len(groups),
        "verified_unique_media": len(verified), "verified_unique_bytes": total_verified_bytes,
        "status_counts_by_post": dict(sorted(status_counts.items())),
        "policy": "Public Telegram posts only; authenticated existing session; no access-control bypass.",
    }


async def collect(manifest_path: Path, media_dir: Path, channel_snapshot: Path | None,
                  concurrency: int = 3, checkpoint_every: int = 10) -> dict:
    """Resume downloads for a previously collected public-post manifest."""
    from tg_collect import load_env, make_client

    rows = read_manifest(manifest_path)
    channel_ids = load_channel_ids(channel_snapshot)
    media_dir.mkdir(parents=True, exist_ok=True)
    quarantine = media_dir.parent / "partial_downloads"
    quarantine.mkdir(parents=True, exist_ok=True)

    # Re-verify all recorded binaries before trusting a checkpoint.
    for row in rows:
        path = row.get("local_file")
        if not path:
            continue
        expected_size = row.get("file_size_bytes")
        expected_sha = row.get("sha256")
        if file_matches(path, expected_size, expected_sha):
            row["status"] = "downloaded_verified"
            if not expected_sha:
                row["sha256"] = sha256_file(path)
            continue
        candidate = Path(path)
        had_file = candidate.is_file()
        if had_file:
            quarantined = quarantine / candidate.name
            if quarantined.exists():
                quarantined = quarantine / f"{candidate.stem}.{int(datetime.now().timestamp())}{candidate.suffix}"
            os.replace(candidate, quarantined)
        if had_file:
            row.update(status="download_interrupted", local_file=None)
            row.pop("sha256", None)
        elif row.get("sha256") or row.get("status") in ("downloaded", "downloaded_recovered",
                                                          "downloaded_verified"):
            row.update(status="download_interrupted", local_file=None)
            row.pop("sha256", None)
        else:
            row["local_file"] = None

    write_manifest_atomic(manifest_path, rows)
    post_groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        channel = str(row.get("channel") or "").lower().lstrip("@")
        message_id = row.get("message_id")
        if channel and message_id:
            post_groups[channel].append(row)

    # One source post per missing document, plus rows whose media metadata is unknown.
    missing_file_ids = {
        file_id for file_id, copies in group_manifest_by_file_id(rows).items()
        if not any(r.get("status") == "downloaded_verified" for r in copies)
    }
    fetch_by_channel: dict[str, dict[int, dict]] = defaultdict(dict)
    for channel, posts in post_groups.items():
        for row in posts:
            fid = str(row.get("telegram_file_id") or "")
            if (not fid) or (fid in missing_file_ids and row.get("status") != "downloaded_verified"):
                fetch_by_channel[channel][int(row["message_id"])] = row

    client = make_client(load_env())
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram session is not authorized; no download attempted")

        semaphore = asyncio.Semaphore(max(1, concurrency))
        messages: dict[tuple[str, int], object] = {}
        async def fetch_channel(channel: str, by_id: dict[int, dict]):
            try:
                input_entity = None
                cached_id = channel_ids.get(channel)
                if cached_id is not None:
                    try:
                        input_entity = await client.get_input_entity(cached_id)
                    except Exception:
                        input_entity = None
                if input_entity is None:
                    input_entity = await client.get_input_entity("@" + channel)
                message_ids = list(by_id)
                for offset in range(0, len(message_ids), 100):
                    batch_ids = message_ids[offset:offset + 100]
                    async with semaphore:
                        received = await client.get_messages(input_entity, ids=batch_ids)
                    received = received if isinstance(received, (list, tuple)) else [received]
                    by_message_id = {message.id: message for message in received if message is not None}
                    for message_id in batch_ids:
                        row = by_id[message_id]
                        message = by_message_id.get(message_id)
                        if message is None:
                            row.update(status="message_unavailable")
                            continue
                        messages[(channel, message_id)] = message
                        _apply_metadata(row, message, media_dir)
            except Exception as exc:
                for row in by_id.values():
                    row.update(status="channel_or_metadata_error", error_type=_safe_error_type(exc))

        await asyncio.gather(*(fetch_channel(channel, posts)
                               for channel, posts in fetch_by_channel.items()))
        write_manifest_atomic(manifest_path, rows)

        groups = group_manifest_by_file_id(rows)
        work = []
        for file_id, copies in groups.items():
            if any(r.get("status") == "downloaded_verified" for r in copies):
                continue
            source_row = next((r for r in copies if (str(r.get("channel", "")).lower().lstrip("@"),
                                                     int(r.get("message_id") or -1)) in messages), None)
            if source_row:
                message = messages[(str(source_row["channel"]).lower().lstrip("@"),
                                    int(source_row["message_id"]))]
                work.append((file_id, copies, source_row, message))

        completed = 0
        download_semaphore = asyncio.Semaphore(max(1, concurrency))
        async def download_one(file_id, copies, source_row, message):
            nonlocal completed
            document, _ = _video_document(message)
            if document is None or str(document.id) != file_id:
                for row in copies:
                    row.update(status="metadata_changed", error_type="DocumentIdMismatch")
                return
            expected_size = int(getattr(document, "size", 0) or 0)
            target = _canonical_path(media_dir, document)
            if expected_size <= 0:
                for row in copies:
                    row.update(status="invalid_metadata", error_type="MissingExpectedSize")
                return
            try:
                async with download_semaphore:
                    result = await download_atomic(
                        lambda temporary: client.download_media(message, file=str(temporary)),
                        target, expected_size,
                    )
                for row in copies:
                    row.update(status="downloaded_verified", local_file=result["path"],
                               file_size_bytes=result["size_bytes"], sha256=result["sha256"],
                               downloaded_at_utc=utc_now())
                    row.pop("error_type", None)
            except Exception as exc:
                for row in copies:
                    row.update(status="download_error", error_type=_safe_error_type(exc))
            finally:
                completed += 1
                if completed % checkpoint_every == 0 or completed == len(work):
                    write_manifest_atomic(manifest_path, rows)
                    summary = build_summary(rows, manifest_path, media_dir)
                    write_json_atomic(manifest_path.with_name("collection_summary.json"), summary)
                    print(f"verified {summary['verified_unique_media']}/{summary['unique_telegram_file_ids']} unique media; "
                          f"download step {completed}/{len(work)}", flush=True)

        await asyncio.gather(*(download_one(*item) for item in work))
    finally:
        await client.disconnect()

    summary = build_summary(rows, manifest_path, media_dir)
    summary["completed_at_utc"] = utc_now()
    write_json_atomic(manifest_path.with_name("collection_summary.json"), summary)
    write_manifest_atomic(manifest_path, rows)
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True,
                        help="Existing per-post JSONL manifest to resume")
    parser.add_argument("--media-dir", type=Path, required=True,
                        help="Destination for immutable downloaded binaries")
    parser.add_argument("--channel-snapshot", type=Path,
                        help="Optional local Telegram channels.jsonl ID cache")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--checkpoint-every", type=int, default=10)
    args = parser.parse_args(argv)
    summary = asyncio.run(collect(args.manifest, args.media_dir, args.channel_snapshot,
                                  args.concurrency, args.checkpoint_every))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
