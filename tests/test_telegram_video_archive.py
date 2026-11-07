import asyncio
import hashlib

from src.telegram_video_archive import download_atomic, file_matches, group_manifest_by_file_id


def test_file_matches_requires_exact_size_and_optional_hash(tmp_path):
    path = tmp_path / "clip.mp4"
    path.write_bytes(b"video bytes")
    digest = hashlib.sha256(b"video bytes").hexdigest()

    assert file_matches(path, 11, digest)
    assert not file_matches(path, 10, digest)
    assert not file_matches(path, 11, "0" * 64)
    assert not file_matches(tmp_path / "missing.mp4", 11)


def test_download_atomic_keeps_only_verified_complete_file(tmp_path):
    destination = tmp_path / "media.mp4"

    async def writer(path):
        path.write_bytes(b"complete-media")
        return str(path)

    result = asyncio.run(download_atomic(writer, destination, expected_size=14))
    assert result["status"] == "downloaded"
    assert destination.read_bytes() == b"complete-media"
    assert result["size_bytes"] == 14
    assert not list(tmp_path.glob("*.part"))


def test_download_atomic_rejects_truncated_media_and_preserves_destination(tmp_path):
    destination = tmp_path / "media.mp4"
    destination.write_bytes(b"previous")

    async def writer(path):
        path.write_bytes(b"short")
        return str(path)

    try:
        asyncio.run(download_atomic(writer, destination, expected_size=10))
    except ValueError as exc:
        assert "size" in str(exc).lower()
    else:
        raise AssertionError("truncated download should fail integrity check")

    assert destination.read_bytes() == b"previous"
    assert not list(tmp_path.glob("*.part"))


def test_download_atomic_reuses_existing_verified_file(tmp_path):
    destination = tmp_path / "media.mp4"
    destination.write_bytes(b"already complete")

    async def should_not_run(path):
        raise AssertionError("verified asset should not be downloaded again")

    result = asyncio.run(download_atomic(should_not_run, destination, expected_size=16))
    assert result["status"] == "existing_verified"


def test_group_manifest_by_file_id_preserves_rows_and_skips_missing_ids():
    rows = [
        {"telegram_file_id": "10", "message_id": 1},
        {"telegram_file_id": "10", "message_id": 2},
        {"message_id": 3},
    ]
    grouped = group_manifest_by_file_id(rows)
    assert list(grouped) == ["10"]
    assert grouped["10"] == rows[:2]
