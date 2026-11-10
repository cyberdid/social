#!/usr/bin/env python3
"""Publish a new version of a Zenodo record with replacement PDFs. This action is permanent.

Reads ZENODO_TOKEN from ~/.config/social/zenodo.env. Usage: publish_new_version.py <previous record id>
"""
import json
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
env = dict(l.split("=", 1) for l in (Path.home() / ".config/social/zenodo.env").read_text().splitlines() if "=" in l)
HEADERS = {"Authorization": f"Bearer {env['ZENODO_TOKEN'].strip()}", "Accept": "application/vnd.inveniordm.v1+json"}
API = "https://zenodo.org/api/records"
FILES = ["social_framework_en_2026-11-10_v1.1.pdf", "social_framework_uk_2026-11-10_v1.1.pdf"]
NOTE = ("<p>Version 1.1 corrects the availability statement after the development repository was made public on "
        "10 November 2026, and adds the corresponding privacy limitation. The evaluation and results are unchanged.</p>")


def checked(response):
    if not response.ok:
        sys.exit(f"Zenodo error {response.status_code}: {response.text[:800]}")
    return response.json() if response.content else {}


def only_ids(value):
    if isinstance(value, dict):
        return {"id": value["id"]} if "id" in value and "title" in value else {k: only_ids(v) for k, v in value.items()}
    return [only_ids(v) for v in value] if isinstance(value, list) else value


draft = checked(requests.post(f"{API}/{sys.argv[1]}/versions", headers=HEADERS, timeout=120))
url = f"{API}/{draft['id']}/draft"
for entry in checked(requests.get(f"{url}/files", headers=HEADERS, timeout=60)).get("entries", []):
    checked(requests.delete(f"{url}/files/{entry['key']}", headers=HEADERS, timeout=60))
checked(requests.post(f"{url}/files", headers=HEADERS, json=[{"key": name} for name in FILES], timeout=60))
for name in FILES:
    data = (ROOT / name).read_bytes()
    checked(requests.put(f"{url}/files/{name}/content", data=data, timeout=300,
                         headers={**HEADERS, "Content-Type": "application/octet-stream"}))
    checked(requests.post(f"{url}/files/{name}/commit", headers=HEADERS, timeout=120))
reserved = checked(requests.post(f"{url}/pids/doi", headers=HEADERS, timeout=120))
meta = only_ids(reserved["metadata"])
meta["version"] = "1.1"
meta["publication_date"] = "2026-11-10"
for item in meta.get("additional_descriptions", []):
    if item["type"]["id"] == "notes" and "Version 1.1" not in item["description"]:
        item["description"] += NOTE
payload = {"access": reserved["access"], "metadata": meta, "pids": reserved["pids"], "custom_fields": only_ids(reserved.get("custom_fields", {})),
           "files": {"enabled": True, "default_preview": FILES[0]}}
updated = checked(requests.put(url, headers=HEADERS, json=payload, timeout=120))
if updated.get("errors"):
    sys.exit("Validation errors, not published: " + json.dumps(updated["errors"], ensure_ascii=False)[:1500])
published = checked(requests.post(f"{url}/actions/publish", headers=HEADERS, timeout=180))
print(published["id"], published["pids"]["doi"]["identifier"], published["links"]["self_html"])
