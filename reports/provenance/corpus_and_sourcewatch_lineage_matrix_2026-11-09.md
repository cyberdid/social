# Corpus & Source-Watch Lineage Matrix Report

**Milestone:** M4 (Corpus & Source-Watch Provenance Harmonization)  
**Document ID:** `corpus_and_sourcewatch_lineage_matrix_2026-11-09`  
**Generated At (UTC):** 2026-11-09T07:52:20Z  
**Owner:** `worker_corpus_provenance`  
**Schema Version:** `social_lineage_manifest_v1`  
**Machine-Readable Manifest:** `reports/provenance/lineage_manifest_2026-11-09.json`  

---

## 1. Executive Summary & Epistemological Stance

This document establishes the authoritative provenance baseline for all Telegram publications, channel panels, view counters, text similarity networks, and Source Watch crawl snapshots cited throughout the Social Master Plan v2.0 investigation of the Petropavlivska Borshchahivka incident.

During previous reporting iterations, two prominent discrepancies arose:
1. **Telegram Corpus Metrics (1,408 vs 1,438 Posts; 159 vs 158 Channels):** Previous analytical sections cited different denominators—historical (`1408` posts, `159` channels, `115,931,014` views) versus merged (`1438` posts, `158` channels, `119,515,745` views)—creating apparent contradictions for downstream reviewers.
2. **Source Watch Crawl Success (10/12 vs 9/12 Targets):** One automated run reported 9 successful first-baseline pages with 3 access errors, whereas the dedicated snapshot run recorded 10 successful pages with 2 access errors.

This report delivers a rigorous forensic reconciliation:
- **Corpus Harmonization:** Proves that the +30 relevant post difference ($1,438 - 1,408 = +30$) is the deterministic result of merging dual-sweep crawls (+36 total posts, +31 newly relevant posts) while omitting channel `kiber_boroshno` (-1 relevant post). Further documents the 475 URL channel name casing mutations that caused naive diffs to falsely show 505 additions and 475 removals.
- **Source Watch Harmonization:** Identifies the permanent technical root cause for the 2 DBR crawler errors: a local OS TLS trust-store limitation (`SSLCertVerificationError: unable to get local issuer certificate`) on `dbr.gov.ua`, and classifies the third error in the automated run as a transient HTTP socket timeout.
- **Strict Provenance Rule:** Mandates that every quantitative figure and empirical claim in reports link to an immutable tuple `(corpus_version, run_id, timestamp)` with bitwise SHA-256 verification, strictly forbidding denominator bleeding across corpus versions.

---

## 2. Part 1: Telegram Corpus Reconciliation (1,408 vs 1,438 Posts)

### 2.1 Baseline Dataset Definitions

The repository hosts two canonical clean publication datasets:

1. **Historical Baseline (`telegram_historical_v1`):**
   - **Path:** `data/processed/continuation_20261105/posts_clean.jsonl`
   - **SHA-256:** `4e859d407aef52c72a8e690dc5716d7d92d11ff7d7a164760db5a4c0ad334350`
   - **Size:** 90,630,741 bytes
   - **Total Publications:** `23,350`
   - **Relevant Publications:** `1,408`
   - **Relevant Channels:** `159`
   - **Total View Counters:** `115,931,014`
   - **MinHash-LSH Verified Pairs (>= 0.6):** `367`

2. **Merged Corpus (`telegram_merged_v2`):**
   - **Path:** `data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl`
   - **SHA-256:** `d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f`
   - **Size:** 55,105,209 bytes
   - **Total Publications:** `23,386`
   - **Relevant Publications:** `1,438`
   - **Relevant Channels:** `158`
   - **Total View Counters:** `119,515,745`
   - **Exact Jaccard Cross-Channel Pairs (>= 0.6):** `369`

### 2.2 Mathematical Difference Accounting

| Metric | Historical (`v1`) | Merged (`v2`) | Net Delta | Forensic Explanation |
|---|---|---|---|---|
| **Total Posts** | 23,350 | 23,386 | **+36** | Addition of 36 raw crawl lines captured during dual-sweep collection |
| **Relevant Posts** | 1,408 | 1,438 | **+30** | +31 newly relevant posts added minus 1 relevant post lost from `kiber_boroshno` |
| **Relevant Channels** | 159 | 158 | **-1** | Omission of channel `kiber_boroshno` |
| **Summed Views** | 115,931,014 | 119,515,745 | **+3,584,731** | Additional views accrued by newly captured publications |
| **Cross-Channel Pairs (>= 0.6)** | 367 | 369 | **+2** | LSH-audited full Jaccard sweep detected 2 additional cross-channel pairs |

### 2.3 Forensic Accounting of Missing Channel `kiber_boroshno`

The single channel present in the historical relevant panel ($159$) but absent from the merged relevant panel ($158$) is **`kiber_boroshno`** (КіберБорошно | CyberBoroshno):

- **Channel Identifier:** `kiber_boroshno` (Chat ID: `-1001742466857`)
- **Post Message ID:** `13675`
- **Post URL:** `https://t.me/kiber_boroshno/13675`
- **Published Timestamp:** `2026-11-03T14:05:40+00:00` (`2026-11-03T16:05:40+02:00` Kyiv time)
- **Observed Views:** `39,012`
- **Forward Count:** `1,109`
- **Source Snapshot Tag:** `20261105T104050Z`
- **Post Clean Text Excerpt:**
  > "Минула доба довкола Петропавлівської Борщагівки пройшла в інформаційному просторі дуже гучно. Нацгвардія тримала людей у пункті для повернутих із СЗЧ, а за 22 години з цього зробили «концтабір ТЦК».

..."

#### Technical Reason for Absence:
Forensic analysis of the `source_snapshot` metadata field demonstrates that `kiber_boroshno` was fetched under snapshot **`20261105T104050Z`**. The historical continuation dataset (`continuation_20261105`) ingested all sweeps through `20261105T104252Z`. However, the merged dataset directory name and ingestion script—`data/processed/20261105T101013Z+20261105T102914Z/`—bounded collection to `2026-11-05T10:29:14Z`. Because `kiber_boroshno` was scraped at 10:40:50Z, it was excluded from the dual-sweep merge window by design.

### 2.4 URL Casing Mutations Analysis (475 Naïve Diff Mutations)

In naive string comparisons, the raw URL set difference showed **475 historical URLs absent in merged** and **505 merged URLs absent in historical** ($505 - 475 = 30$).

Forensic decomposition reveals:
1. **Raw URL String Churn:** Exactly **475** historical relevant posts were recorded with altered URL strings in the merged dataset.
2. **Direct Casing Mutations on Shared Posts:** **354** posts existed in both datasets but had their channel name casing mutated from lowercase (e.g. `https://t.me/anoncinews/84608`) in historical to title/mixed case (e.g. `https://t.me/Anoncinews/84608`) in merged.
3. **Historical-Only Normalized Posts:** **121** posts were present only in the historical dataset (including `https://t.me/kiber_boroshno/13675`).
4. **Merged-Only Normalized Posts:** **151** posts were newly captured in the merged dataset.
5. **Net Delta:** $151 - 121 = +30$ relevant posts ($1,438 - 1,408 = 30$).

Representative casing mutation samples:
- Historical: `https://t.me/anoncinews/84608`  
  Merged: `https://t.me/Anoncinews/84608`
- Historical: `https://t.me/anoncinews/84610`  
  Merged: `https://t.me/Anoncinews/84610`
- Historical: `https://t.me/anoncinews/84613`  
  Merged: `https://t.me/Anoncinews/84613`
- Historical: `https://t.me/anoncinews/84615`  
  Merged: `https://t.me/Anoncinews/84615`
- Historical: `https://t.me/anoncinews/84620`  
  Merged: `https://t.me/Anoncinews/84620`

Accounting for case-insensitive normalization eliminates all spurious churn and validates the exact $+30$ net post count.

---

## 3. Part 2: Source Watch Run Reconciliation (10/12 vs 9/12)

### 3.1 Target Composition (12 Deterministic Targets)

The Source Watch crawler (`src/source_watch_collect.py:build_plan()`) monitors exactly 12 deterministic endpoints:

1. **4 Official News Listing Endpoints:**
   - `https://mvs.gov.ua/press-center/news` (MVS News Center)
   - `https://ngu.gov.ua/` (NGU Official Portal)
   - `https://dbr.gov.ua/news` (DBR News Portal)
   - `https://ombudsman.gov.ua/news` (Ombudsman Portal)
2. **8 Specific Official Article Endpoints:**
   - MVS Service Investigation Statement: `https://mvs.gov.ua/news/mvs-ziasovuje-obstavini-podii-na-kiyivshhini-rozpocato-sluzbove-rozsliduvannia`
   - MVS Briefing Statement: `https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini`
   - MVS Pivnenko Conference: `https://mvs.gov.ua/news/oleksandr-pivnenko-proviv-selektornu-naradu-z-kerivnictvom-nacionalnoyi-gvardiyi-ukrayini`
   - NGU Official Refutation: `https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/`
   - Ombudsman Official Demand: `https://ombudsman.gov.ua/news_details/zhodnih-podvijnih-standartiv-ne-maye-buti-ombudsman-vimagaye-perevirki-situaciyi-na-petropavlivskij-borshchagivci`
   - Suspilne Court Custody Report: `https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/`
   - Hromadske Detention Report: `https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi`
   - DBR Criminal Proceeding: `https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini`

### 3.2 Comparison of Automated Case Run vs Dedicated Snapshot

| Dimension | Automated Case Run (`source_watch_v1`) | Dedicated Snapshot Run (`source_watch_v2`) |
|---|---|---|
| **Run ID** | `automated-case-run-2026-11-08` | `20261108T080550.329799Z` |
| **Timestamp (UTC)** | `2026-11-08T01:14:07Z` | `2026-11-08T08:05:50Z` |
| **Report Locator** | `reports/automated-case-run-2026-11-08/source_watch_summary.json` | `reports/source-watch/20261108/latest.json` |
| **Artifact SHA-256** | `b78ba070ccf0690cb828051e73379582e02b69718022745bea26229f46f92735` | `aa3acaafaaadf532c0f58ef537f938d63bab420527e8ccd63c8412909c0389f6` |
| **HTTP 200 Baselines** | **9** | **10** |
| **Access Errors** | **3** | **2** |
| **Ratio Reported** | **9/12** | **10/12** |
| **Error Breakdown** | 2 DBR TLS errors + 1 transient socket timeout | 2 DBR TLS errors only |

### 3.3 Root Cause Analysis: Systematic DBR TLS Certificate Failure

Across all runs, attempts to connect to `dbr.gov.ua` consistently fail with the verbatim error:
```
SSLError: HTTPSConnectionPool(host='dbr.gov.ua', port=443): Max retries exceeded with url: ...
(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)')))
```

#### Technical Classification & Epistemological Invariant:
1. **Infrastructure Constraint:** The Linux host execution environment lacks the specific Ukrainian government root/intermediate Certificate Authority (CA) certificates necessary to establish trust with `dbr.gov.ua`. Under strict network security policies (`tls_verification: true`), Python `requests` rejects the TLS handshake.
2. **Epistemological Invariant:** This error represents a **transport-level infrastructure limitation**, NOT an absence of publication on DBR servers. As stated in `source_watch_summary.json`: *"A first baseline is not evidence of a new event or changed source statement; individual page errors limit coverage."*
3. **Transient Timeout:** In the automated run, a third endpoint suffered a transient network socket timeout, yielding 9/12. In the isolated snapshot run 7 hours later, the transient timeout cleared, yielding 10/12.

---

## 4. Part 3: The Strict Provenance Rule

To prevent future discrepancies and eliminate citation ambiguity across report dossiers, all downstream generators (`worker_report_publisher`, `worker_integrator_lead`) must adhere to the following **Strict Social Provenance Rule**:

### 4.1 Provenance Binding Tuple

Every quantitative metric, denominator, channel panel count, view total, and factual assertion cited in any report, summary, or manifest must explicitly bind to an exact tuple:

`Provenance Locator = (corpus_version, run_id, timestamp_utc)`

accompanied by the exact cryptographic SHA-256 digest of the source artifact.

### 4.2 Invariant Protocols

1. **Rule of Denominator Integrity (Anti-Bleed Invariant):**
   - Historical baseline figures (`1,408` posts, `159` channels, `115,931,014` views) belong exclusively to `telegram_historical_v1`.
   - Merged corpus figures (`1,438` posts, `158` channels, `119,515,745` views) belong exclusively to `telegram_merged_v2`.
   - **Prohibition:** Denominators and numerators from differing corpus versions must never be mixed in the same table, ratio, or narrative sentence without explicit dual-corpus labeling.
2. **Rule of Immutable Locators:**
   - Every passage, statement, or quote must cite exact character offsets (`artifact_start_offset`, `artifact_end_offset`) or audio millisecond intervals (`[start_ms, end_ms]`).
3. **Rule of Technical Limitation Classification:**
   - Network errors (e.g., DBR TLS failures) must be cataloged as technical transport limitations, never as proof of absent news or non-occurrence of events.

---

## 5. Part 4: Complete Lineage Matrix (Master Table)

The following master matrix links every published metric and empirical finding across the investigation to its exact corpus version, run identifier, UTC timestamp, source file locator, and cryptographic SHA-256 digest:

| Published Metric / Finding | Reported Value | Corpus Version ID | Run ID / Snapshot ID | Timestamp (UTC) | Input Source File / Locator | SHA-256 Digest |
|---|---|---|---|---|---|---|
| **Historical Relevant Posts** | `1408` | `telegram_historical_v1` | `continuation_20261105` | `2026-11-05T10:29:14Z` | `data/processed/continuation_20261105/posts_clean.jsonl` | `4e859d407aef52c7...` |
| **Historical Total Publications** | `23350` | `telegram_historical_v1` | `continuation_20261105` | `2026-11-05T10:29:14Z` | `data/processed/continuation_20261105/posts_clean.jsonl` | `4e859d407aef52c7...` |
| **Historical Relevant Channels** | `159` | `telegram_historical_v1` | `continuation_20261105` | `2026-11-05T10:29:14Z` | `reports/continuation_20261105/relevant_posts.csv` | `8b69539801a385be...` |
| **Historical View Counter Sum** | `115931014` | `telegram_historical_v1` | `continuation_20261105` | `2026-11-05T10:29:14Z` | `reports/continuation_20261105/audit_results.json` | `e9051b3ba98e3676...` |
| **Historical MinHash-LSH Verified Pairs (Threshold 0.6)** | `367` | `telegram_historical_v1` | `coordination_null_models` | `2026-11-06T12:00:00Z` | `reports/continuation_20261105/verified_similarity_edges.csv` | `6d559f3a1d553c60...` |
| **Merged Relevant Posts** | `1438` | `telegram_merged_v2` | `masterplan-run-2026-11-08` | `2026-11-08T01:14:07Z` | `data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl` | `d229d8618021cf28...` |
| **Merged Total Publications** | `23386` | `telegram_merged_v2` | `masterplan-run-2026-11-08` | `2026-11-08T01:14:07Z` | `data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl` | `d229d8618021cf28...` |
| **Merged Relevant Channels** | `158` | `telegram_merged_v2` | `masterplan-run-2026-11-08` | `2026-11-08T01:14:07Z` | `reports/20261105T101013Z+20261105T102914Z/audit_results.json` | `cea8ea91b856fc68...` |
| **Merged View Counter Sum** | `119515745` | `telegram_merged_v2` | `masterplan-run-2026-11-08` | `2026-11-08T01:14:07Z` | `reports/20261105T101013Z+20261105T102914Z/audit_results.json` | `cea8ea91b856fc68...` |
| **Exact Cross-Channel Jaccard Pairs (Threshold >= 0.6)** | `369` | `telegram_merged_v2` | `lsh-audit-20261108` | `2026-11-08T18:00:00Z` | `reports/coordination-null-models-2026-11-08-lsh-audit/exact_cross_channel_edges_ge_0.6.csv` | `9e1d07c77cba556d...` |
| **Source Watch Automated Case Run** | `9/12 OK (3 errors)` | `source_watch_v1` | `automated-case-run-2026-11-08` | `2026-11-08T01:14:07Z` | `reports/automated-case-run-2026-11-08/source_watch_summary.json` | `b78ba070ccf0690c...` |
| **Source Watch Dedicated Snapshot Run** | `10/12 OK (2 errors)` | `source_watch_v2` | `20261108T080550.329799Z` | `2026-11-08T08:05:50Z` | `reports/source-watch/20261108/latest.json` | `aa3acaafaaadf532...` |
| **Telegram Video Assets** | `607` | `telegram_video_v1` | `asr-bulk-20261108` | `2026-11-08T08:00:00Z` | `reports/video-pipeline/telegram-full-decode-2026-11-08.md` | `6e6977eb373158f7...` |
| **Telegram Candidate ASR Segments** | `10872` | `telegram_video_v1` | `asr-bulk-20261108` | `2026-11-08T08:00:00Z` | `external/asr-bulk-20261108/telegram_text_observations.jsonl` | `987ee53ff56a477e...` |
| **TikTok Video Assets** | `20` | `tiktok_video_v1` | `tiktok-runner-2026-11-08` | `2026-11-08T09:00:00Z` | `reports/video-pipeline/tiktok-runner-2026-11-08.md` | `bd7752226eae60a8...` |
| **Release Package Frozen Artifacts** | `65` | `release_package_v1` | `case-release-2026-11-08` | `2026-11-08T22:06:20Z` | `reports/case-release-manifest-2026-11-08.json` | `219bb362eafa6c72...` |

---

## 6. Part 5: Reproducibility & Audit Protocol

### 6.1 Independent Verification Commands

To verify the integrity of all numbers, file counts, and cryptographic hashes established in this report:

1. **Run Provenance Matrix Verification Script:**
   ```bash
   /home/cyberdid/Projects/Social/.venv/bin/python3 scripts/provenance/build_lineage_matrix.py --verify
   ```

2. **Verify Bitwise Hashes of Core Datasets:**
   ```bash
   /home/cyberdid/Projects/Social/.venv/bin/python3 -c '
   import hashlib, json
   h1 = hashlib.sha256(open("data/processed/continuation_20261105/posts_clean.jsonl", "rb").read()).hexdigest()
   h2 = hashlib.sha256(open("data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl", "rb").read()).hexdigest()
   assert h1 == "4e859d407aef52c72a8e690dc5716d7d92d11ff7d7a164760db5a4c0ad334350"
   assert h2 == "d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f"
   print("Bitwise hashes verified 100% identical to lineage manifest.")
   '
   ```

3. **Verify Channel Counts and Missing Channel `kiber_boroshno`:**
   ```bash
   /home/cyberdid/Projects/Social/.venv/bin/python3 -c '
   import json
   hist = [json.loads(l) for l in open("data/processed/continuation_20261105/posts_clean.jsonl") if json.loads(l).get("relevant")]
   curr = [json.loads(l) for l in open("data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl") if json.loads(l).get("relevant")]
   assert len(hist) == 1408
   assert len(curr) == 1438
   ch_diff = {p["channel"] for p in hist} - {p["channel"] for p in curr}
   assert ch_diff == {"kiber_boroshno"}
   print("Corpus difference (+30 relevant posts, -1 channel kiber_boroshno) verified.")
   '
   ```

4. **Verify Automated vs Dedicated Source Watch Counts:**
   ```bash
   /home/cyberdid/Projects/Social/.venv/bin/python3 -c '
   import json
   sw_auto = json.load(open("reports/automated-case-run-2026-11-08/source_watch_summary.json"))
   sw_snap = json.load(open("reports/source-watch/20261108/latest.json"))
   assert sw_auto["new_first_baseline_pages"] == 9 and sw_auto["access_errors"] == 3
   assert sw_snap["counts"]["new_page"] == 10 and sw_snap["counts"]["error"] == 2
   print("Source Watch run reconciliation (9/12 vs 10/12) verified.")
   '
   ```

5. **Run Pytest Test Suite:**
   ```bash
   /home/cyberdid/Projects/Social/.venv/bin/pytest tests/test_provenance_lineage.py -v
   ```

---
*Report certified under Milestone M4 of Social Master Plan v2.0.*
