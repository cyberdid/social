from src.analysis.channel_evidence import (
    build_channel_evidence,
    export_channel_evidence,
    extract_infrastructure_features,
)
import json


def test_russian_links_are_only_an_infrastructure_candidate():
    record = build_channel_evidence(
        "ua_osint",
        profile_text="Український OSINT-проєкт",
        links=[f"https://news{i}.ru/story" for i in range(6)],
        source_refs=["profile:1", "posts:1-6"],
        as_of="2026-11-07T12:00:00Z",
    )
    assert record["infrastructure_candidate"] is True
    assert record["origin"]["value"] == "unknown"
    assert record["content_orientation"]["value"] == "unknown"
    assert record["operational_attribution"]["status"] == "unverified"
    assert record["legacy_group"] is None


def test_profile_markers_are_recorded_as_features_not_operator_attribution():
    features = extract_infrastructure_features(
        "https://vk.com and https://max.ru links appear here", ["https://vk.com/example"]
    )
    assert {x["feature"] for x in features} >= {"profile_marker:vk.com", "profile_marker:max.ru", "link_domain:vk.com"}


def test_low_volume_russian_domain_links_do_not_trigger_candidate_flag():
    record = build_channel_evidence(
        "small_source", "Independent reporting", ["https://one.ru/a"], ["post:1"],
        "2026-11-07T12:00:00Z",
    )
    assert record["infrastructure_candidate"] is False
    assert record["origin"]["value"] == "unknown"


def test_record_requires_evidence_receipt_for_any_non_unknown_attribution():
    try:
        build_channel_evidence(
            "example", "", [], [], "2026-11-07T12:00:00Z",
            origin={"value": "Russia", "status": "confirmed", "evidence_ids": []},
        )
    except ValueError as exc:
        assert "evidence" in str(exc).lower()
    else:
        raise AssertionError("unsupported attribution must be rejected")


def test_exporter_preserves_legacy_group_as_separate_axis_and_hashes_inputs(tmp_path):
    channels = tmp_path / "channels.jsonl"
    posts = tmp_path / "posts.jsonl"
    groups = tmp_path / "groups.csv"
    automatic = tmp_path / "auto.csv"
    output = tmp_path / "channel_evidence.jsonl"
    channels.write_text(json.dumps({"channel": "@ua_osint", "title": "UA OSINT",
                                    "description": "Example"}) + "\n", encoding="utf-8")
    post_rows = [{"channel": "ua_osint", "links": [f"https://source{i}.ru/a"]}
                 for i in range(6)]
    posts.write_text("".join(json.dumps(row) + "\n" for row in post_rows), encoding="utf-8")
    groups.write_text("channel,group\nua_osint,B\n", encoding="utf-8")
    automatic.write_text("channel,group\nua_osint,C\n", encoding="utf-8")

    assert export_channel_evidence(channels, posts, output, [groups, automatic],
                                   "2026-11-07T12:00:00Z") == 1
    record = json.loads(output.read_text(encoding="utf-8"))
    assert record["legacy_group"] == "B"
    assert record["infrastructure_candidate"] is True
    assert record["origin"]["value"] == "unknown"
    assert all(ref.startswith(("channel_snapshot:sha256:", "posts_snapshot:sha256:", "channel:"))
               for ref in record["source_refs"])


def test_exporter_rejects_overwriting_an_input(tmp_path):
    channels = tmp_path / "channels.jsonl"
    posts = tmp_path / "posts.jsonl"
    channels.write_text("{}\n", encoding="utf-8")
    posts.write_text("{}\n", encoding="utf-8")
    try:
        export_channel_evidence(channels, posts, channels)
    except ValueError as exc:
        assert "overwrite" in str(exc)
    else:
        raise AssertionError("input file must not be overwritten")
