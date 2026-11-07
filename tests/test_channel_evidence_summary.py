from src.analysis.channel_evidence_summary import summarize


def test_summary_counts_records_and_distinct_channels_separately():
    snapshots = {
        "one.jsonl": [
            {"channel": "a", "infrastructure_candidate": True,
             "origin": {"value": "unknown"}, "content_orientation": {"value": "unknown"},
             "legacy_group": "C"},
            {"channel": "b", "infrastructure_candidate": False,
             "origin": {"value": "unknown"}, "content_orientation": {"value": "unknown"},
             "legacy_group": "U"},
        ],
        "two.jsonl": [
            {"channel": "a", "infrastructure_candidate": True,
             "origin": {"value": "unknown"}, "content_orientation": {"value": "unknown"},
             "legacy_group": "C"},
        ],
    }
    result = summarize(snapshots)
    assert result["snapshot_records"] == 3
    assert result["unique_channels"] == 2
    assert result["infrastructure_candidate_records"] == 2
    assert result["origin_unknown_records"] == 3
    assert result["content_orientation_unknown_records"] == 3
