#!/usr/bin/env python3
"""Create a Zenodo draft for the Social system paper; publish only with --publish <deposition id>.

Reads ZENODO_TOKEN from ~/.config/social/zenodo.env (scopes: deposit:write, deposit:actions).
Usage: upload_to_zenodo.py             create draft, upload both PDFs, set metadata, print the review link
       upload_to_zenodo.py --publish ID publish that reviewed draft (permanent: a DOI cannot be withdrawn)
"""
import json
import sys
from pathlib import Path

import requests

API = "https://zenodo.org/api/deposit/depositions"
HERE = Path(__file__).resolve().parent
PDFS = [HERE.parents[2] / name for name in ("social_framework_en_2026-11-10.pdf", "social_framework_uk_2026-11-10.pdf")]
env = dict(l.split("=", 1) for l in (Path.home() / ".config/social/zenodo.env").read_text().splitlines() if "=" in l)
HEADERS = {"Authorization": f"Bearer {env['ZENODO_TOKEN'].strip()}"}


def checked(r):
    if not r.ok:
        sys.exit(f"Zenodo error {r.status_code}: {r.text[:500]}")
    return r.json()


if len(sys.argv) == 3 and sys.argv[1] == "--publish":
    print(checked(requests.post(f"{API}/{sys.argv[2]}/actions/publish", headers=HEADERS, timeout=120))["doi_url"])
    sys.exit()
dep = checked(requests.post(API, headers=HEADERS, json={}, timeout=60))
for pdf in PDFS:
    with pdf.open("rb") as f:
        checked(requests.put(f"{dep['links']['bucket']}/{pdf.name}", headers=HEADERS, data=f, timeout=300))
checked(requests.put(f"{API}/{dep['id']}", headers=HEADERS, json=json.loads((HERE / "metadata.json").read_text()), timeout=60))
print(f"Draft {dep['id']}: https://zenodo.org/uploads/{dep['id']}")
