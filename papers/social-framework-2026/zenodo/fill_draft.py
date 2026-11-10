#!/usr/bin/env python3
"""Fill the remaining fields of the reviewed Zenodo draft through the InvenioRDM API. Never publishes.

Reads ZENODO_TOKEN from ~/.config/social/zenodo.env. Usage: fill_draft.py <draft id>
"""
import json
import re
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
env = dict(l.split("=", 1) for l in (Path.home() / ".config/social/zenodo.env").read_text().splitlines() if "=" in l)
MIME = "application/vnd.inveniordm.v1+json"
HEADERS = {"Authorization": f"Bearer {env['ZENODO_TOKEN'].strip()}", "Accept": MIME}
URL = f"https://zenodo.org/api/records/{sys.argv[1]}/draft"
CODE = "https://github.com/cyberdid/social-framework"


def only_ids(value):
    """Vocabulary references are sent as ids; the server fills in their titles."""
    if isinstance(value, dict):
        return {"id": value["id"]} if "id" in value and "title" in value else {k: only_ids(v) for k, v in value.items()}
    return [only_ids(v) for v in value] if isinstance(value, list) else value


tex = (HERE.parent / "manuscript/social_framework_uk.tex").read_text(encoding="utf-8")
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1).strip()
abstract = re.sub(r"\s+", " ", abstract.replace("---", "—").replace("\\%", "%"))
assert "\\" not in abstract
keywords = re.search(r"Ключові слова:\} (.*?)\.\s*$", tex, re.M).group(1).split("; ")
title_uk = "Social: доказово обґрунтований фреймворк для автоматизованого аналізу соціальних конфліктів та інформаційних інцидентів"

record = requests.get(URL, headers=HEADERS, timeout=60).json()
meta = only_ids(record["metadata"])
meta["languages"] = [{"id": "eng"}, {"id": "ukr"}]
meta["copyright"] = "Copyright (C) 2026 Oleksandr Pylypenko"
meta["creators"][0]["affiliations"] = [{"name": "State University of Trade and Economics"}]
meta["additional_titles"] = [{"title": title_uk, "type": {"id": "translated-title"}, "lang": {"id": "ukr"}}]
notes = [d for d in meta.get("additional_descriptions", []) if d["type"]["id"] == "notes"]
for note in notes:
    note["lang"] = {"id": "eng"}
meta["additional_descriptions"] = [{"description": f"<p>{abstract}</p>", "type": {"id": "abstract"}, "lang": {"id": "ukr"}}] + notes
existing = [s["subject"] for s in meta["subjects"]]
meta["subjects"] = meta["subjects"] + [{"subject": k} for k in keywords if k not in existing]
meta["dates"] = [{"date": "2026-11-05/2026-11-09", "type": {"id": "collected"},
                  "description": "Digital-trace collection used in the real-world application"}]
meta["references"] = [{"reference": r} for r in json.loads((HERE / "references.json").read_text(encoding="utf-8"))]
payload = {
    "access": record["access"], "metadata": meta, "pids": record.get("pids", {}),
    "files": {"enabled": True, "default_preview": "social_framework_en_2026-11-10.pdf"},
    "custom_fields": {"code:codeRepository": CODE, "code:programmingLanguage": [{"id": "python"}],
                      "code:developmentStatus": {"id": "active"}},
}
response = requests.put(URL, headers=HEADERS, json=payload, timeout=120)
result = response.json()
print("status", response.status_code, "errors", json.dumps(result.get("errors", []), ensure_ascii=False)[:1200])
m = result.get("metadata", {})
print("languages", [x["id"] for x in m.get("languages", [])], "| copyright:", m.get("copyright"))
print("dates", m.get("dates"), "| references", len(m.get("references", [])), "| subjects", len(m.get("subjects", [])))
print("titles", len(m.get("additional_titles", [])), "| descriptions", [d["type"]["id"] for d in m.get("additional_descriptions", [])])
print("affiliation", m.get("creators", [{}])[0].get("affiliations"))
print("custom", json.dumps(result.get("custom_fields"), ensure_ascii=False)[:300], "| preview", result.get("files", {}).get("default_preview"))
print("published", result.get("is_published"), "status", result.get("status"))
