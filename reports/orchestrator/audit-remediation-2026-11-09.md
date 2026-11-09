# Audit remediation: current evidence and publication artifacts

**Date:** 9 November 2026  
**Scope:** Corrective response to the independent audit of the Social case report and its supporting repository artifacts.  
**Status:** Local remediation branch; not published to GitHub.

## Current findings

| Audit finding | Remediation | Evidence and remaining boundary |
|---|---|---|
| Reaction chart contained hard-coded, unsupported counts | Replaced it with the documented live parity check: 10 comments in 3 threads; 10/10 reaction vectors matched. | This is a bounded API parity sample. It does not estimate reactions across 533 discussion threads; no historical reaction series exists. |
| Pseudo-map used arbitrary coordinates and reported an incorrect 4.2 km distance | Removed coordinates, distance, scale, and geographic-map framing. Figure 4 is a non-scale comparison of separately reported events. | The specific TikTok video has not been independently geolocated. |
| Official denial was presented as physical refutation | Recomputed the 25-claim matrix using evidence scope. | Current matrix: 19 supported within declared scope, 6 insufficient evidence, 0 physically refuted. The claims about 40 hostages and a death remain `insufficient_evidence` with the police position recorded as `officially_disputed`. This does not establish either side of those physical claims. |
| Evidence verification was described as autonomous end-to-end discovery | Removed forced primary/counter passage IDs. The verifier now assesses retrieved candidates from the supplied, curated passage corpus and records retrieval receipts. | It does not discover sources on the open web. It is a deterministic retrieval and relation-inference pipeline over its input corpus. |
| Fire source was mislabeled as a raw official bulletin | Quarantined the manually composed legacy text and replaced the verification passage with a source-attributed Interfax report. | Interfax reported the OVA-head statement and explicitly said the local Sofia location was not officially confirmed at that time. A later village-council post named Sofiaivska. Neither source independently geolocates the supplied TikTok video. See [fire source review](../source-watch/fire-source-review-2026-11-09.md). |
| Physical timeline had hand-entered decimal confidence scores | Timeline source and report identify it as analyst-curated reconstruction; confidence is expressed as qualitative evidence tiers. | These tiers are not calibrated probabilities and do not make the episode sequence automatically discovered. See [timeline JSON](../event-reconstruction/physical_event_timeline_2026-11-09.json) and its builder. |
| Master-plan closeout repeated stale results | Marked the original closeout as historical and linked this remediation report. | Old counts and integrity digests describe the earlier snapshot only; use the regenerated matrix and PDF manifest for current outputs. |
| Absolute local paths reduced portability | Replaced machine-specific ASR and lineage inputs with repository-relative defaults plus `SOCIAL_ASR_RAW_PATH` / `SOCIAL_ASR_SECOND_PASS_PATH`. | Private input files remain outside the repository; builders report when a local checksum comparison cannot be performed. |

## Fire-source provenance

The former `data/raw/official_bulletins/kyiv_ova_fire_20261105.txt` was not a captured official bulletin. It was moved to `data/processed/source_notes/kyiv_ova_fire_legacy_unverified.md`, whose content explicitly quarantines it and prevents use as evidence. The assessed passage now attributes the quoted text to Interfax-Ukraine’s 00:05 report of the OVA-head Telegram post. The Telegram original is linked by Interfax but is not archived in this repository. The passage therefore remains secondary reporting of an official statement, not a captured primary artifact.

## Scope of the regenerated case report

The 9 November report is generated from `scripts/reports/build_report.py` and JSON/CSV/PNG inputs. Its manifest records the builder and hashes of key inputs; it does not misidentify the separate `reports/borshchahivka-report.md` as the source of the PDF. The generated manifest starts with visual review marked pending; that status is changed only after pages are actually rendered and inspected.

The 6 and 8 November PDFs are preserved as dated historical editions. They are not silently rewritten. The 9 November edition is the corrected current artifact. Its page count, SHA-256, text-extraction result, and visual-review status are recorded in `output/pdf/manifest-2026-11-09.json`.

## Current verification boundary

The remediation improves traceability and removes unsupported claims. It does not independently determine the physical facts for which the only counterevidence is an institutional statement, establish the TikTok video’s location, recover historical platform reactions, or establish the independence of declared source-lineage roots. Those limits remain visible in the report.
