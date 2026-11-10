# Bibliography consolidation and source-verification audit

Checked 2026-11-10. Deliverable: `manuscript/references.bib`, consolidated from the four unchanged source fragments in root → systems → evidence → statistics order. This file distinguishes structural validation, direct primary-source checking, inherited team verification, and local manuscript identity. It does not claim every URL was fetched successfully or every DOI was freshly resolved through Crossref.

## Consolidation result

| Fragment | Entries | SHA-256 at consolidation |
|---|---:|---|
| `manuscript/references_root.bib` | 12 | `7e8a67649ca45c7a7c123051142a9ee81187d66b8558ade7c4191a7826cf5225` |
| `manuscript/references_systems.bib` | 8 | `86fa2880c610eb4d9a1495f47f89c7faab64660f22dc64314b64d1f9b6f9b458` |
| `manuscript/references_evidence.bib` | 8 | `d2c3bd054cab868c5af3c0e36d4075029750b9449bf9e9bb823a6aeea3bdf5f5` |
| `manuscript/references_statistics.bib` | 9 | `daf27b10b54b7b132f2b226038fad5611cd26c4610a6523160625fac75c72ef7` |

The consolidated file contains **37 records, 37 unique citation keys and 22 DOI fields**. Normalizing DOI case and optional resolver prefixes found **no duplicate DOIs**. The local structural scan found **no unmatched entry/field braces, malformed fields, repeated field names, empty titles, or missing author/editor identity**. Three official living webpages intentionally omit publication year: `acledCodebook`, `invidVerificationPlugin`, and `weverifyVerificationPlugin`. The local unpublished case manuscript intentionally has no invented public URL or DOI. The two W3C records preserve editorial roles rather than assigning personal authorship.

A scan of currently present manuscript `.tex` files found **all 37 keys cited and zero unknown citation keys** at consolidation time. This is a syntactic citation-coverage check, not a statement that every citation supports its surrounding assertion. Later manuscript changes can invalidate this check. The root build must still verify bibliography rendering and warning behavior in the selected LaTeX/BibTeX style.

## Aggregate-only corrections and retained exceptions

1. **FAIR author-name defect corrected.** In `wilkinson2016fair`, `Aalbersberg, I. Jsbrand Jan` was corrected to `Aalbersberg, IJsbrand Jan`. The author’s [ORCID identity](https://orcid.org/0000-0002-0209-4480) and [Elsevier author biography](https://researcheracademy.elsevier.com/node/3012) confirm the name. This aggregation pass could not retrieve Nature's publisher article/PDF because both redirected to an inaccessible identity-provider endpoint; PMC returned a browser challenge. The root worker had already checked publisher metadata manually. The correction is explicit; neither original fragment nor `root_doi_metadata.json` was rewritten.
2. **Empty optional fields removed.** Empty `number`/`volume` fields in the root fragment were omitted in the aggregate. No nonempty volume, issue, page range, year or DOI was silently changed.
3. **Capitalization protection added.** Aggregate-only braces preserve `FAIR`, `Tesseract OCR`, and `Ukrainian` under bibliography styles that downcase titles. These are typesetting changes, not changes to work identity.
4. **BM25 publisher/depositor discrepancy retained.** `RobertsonZaragoza2009BM25` follows the publisher PDF's preferred citation, 3(4):333–389 (2009), despite a conflicting Crossref volume/page deposit. The source fragment already records this exception; see `audit/literature_statistics.md`. A DOI match alone is not a metadata validation.
5. **Other deliberate exceptions retained.** Broder uses the conference year; Holm uses a stable JSTOR locator without an invented DOI; Phipson cites the 2010 article while noting the author copy's 2011 correction; Magelinski follows the publisher title with initial “A”; Vicente has one author whose surname is Vicente. W3C records cite dated final Recommendations rather than draft versions. Berkeley cites the final 2022 edition, not the earlier advance edition.
6. **Living documentation dates.** `systran2026faster` and `telegram2026reactions` use 2026 as the inspected documentation snapshot year, as their notes state; it is not a claim that the software/protocol originated in 2026. The faster-whisper source is current official documentation, while Social's historical dependency is version 1.1.0. No software benchmark was rerun.
7. **Style warnings remain possible.** The two editor-only `@techreport` W3C records are semantically intentional, but some BibTeX styles require `author` for that entry type. The three undated `@manual`/`@misc` pages may also generate style warnings. Such warnings should be resolved through appropriate bibliography styling, not by inventing author roles or publication years.

## Per-key verification categories

**D** = primary publisher/proceedings/author/tool source directly inspected by this audit worker during the systems or aggregation task. **T** = detailed primary-source verification inherited from the responsible team audit; not falsely presented as a second independent full-text check. **R** = root worker's manually checked primary metadata, with Crossref access limitation explicitly recorded. **L** = local unpublished manuscript identity only. Multiple codes indicate complementary checks, not multiple independent confirmations of substantive claims.

| Citation key | Category | Primary source and metadata verification scope | Limits / decision |
|---|---|---|---|
| `imran2015crisis` | D+R | [Author PDF](https://mimran.me/papers/processing_social_media_messages_in_mass_emergency_survey.pdf): title, four authors, ACM CSUR 47(4), article 67, 2015, DOI; root manual record. | Root DOI retrieval returned 429; no successful fresh Crossref claim. Survey is not Social validation. |
| `wilkinson2016fair` | R+D identity | [Publisher article](https://www.nature.com/articles/sdata201618); root checked title/year/venue/DOI. Author identity spelling checked as above. | Publisher/PMC access blocked during this pass; abbreviated author list ends in `others`. Corrected the malformed third given name only. |
| `wilson2017practices` | D+R | [PLOS article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510): six authors, title, 2017, 13(6), e1005510, DOI. | No numerical software-quality result imported. |
| `sandve2013reproducible` | D+R | [PLOS article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285): four authors, title, 2013, 9(10), e1003285, DOI. | Distinguishes computational replay from truth of findings. |
| `smith2007tesseract` | D+R | [Author/employer publication page](https://research.google/pubs/an-overview-of-the-tesseract-ocr-engine/): Ray Smith, title, ICDAR/IEEE, 2007, 629–633; root checked DOI. | Direct page verifies publication identity; no fresh IEEE/DOI resolver success claimed. |
| `radford2023whisper` | D | [PMLR proceedings](https://proceedings.mlr.press/v202/radford23a.html): authors, title, ICML 2023, volume 202, 28492–28518. | No DOI fabricated; foundational model paper is distinct from faster-whisper implementation. |
| `lewis2020rag` | D | [NeurIPS record](https://proceedings.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html): title, author order, year and proceedings volume. | Page range omitted in source fragment; no unverified DOI added. |
| `gao2023alce` | D | [ACL record](https://aclanthology.org/2023.emnlp-main.398/): four authors, title, EMNLP 2023, 6465–6488, DOI. | Citation metrics in that paper are external benchmarks, not Social results. |
| `dementieva2025emobench` | D | [ACL record](https://aclanthology.org/2025.findings-emnlp.107/): Daryna Dementieva, Nikolay Babakov, Alexander Fraser; title, Findings EMNLP 2025, 2025–2048, DOI. | Potentially suspicious page/year repetition was checked and is correct. |
| `systran2026faster` | D | [Official repository](https://github.com/SYSTRAN/faster-whisper): software title, SYSTRAN/contributor attribution, CTranslate2 implementation documentation. | Living documentation; year denotes access snapshot, not original release; Social pins historical 1.1.0. |
| `telegram2026reactions` | D | [Official MTProto documentation](https://core.telegram.org/api/reactions): reaction constructors and aggregate/list APIs, corporate source/title. | Living protocol documentation; no journal/publication DOI claimed. |
| `pylypenko2026case` | L | `papers/social-case-study-2026/sections/article_en.tex:1`–`:2`: exact title and Oleksandr Pylypenko authorship checked against local source. | Private project draft; public publication status not established; not independent evidence. |
| `gdelt2015events` | D | [Official Event v2.0 codebook](https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf): title/version/date (2015-02-19). | Corporate manual; no DOI asserted. |
| `gdelt2015gkg` | D | [Official GKG v2.1 codebook](https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf): title/version/date (2015-02-19). | Kept separate from Event codebook and older GKG v2.0. |
| `acledCodebook` | D | [Official methodology](https://acleddata.com/methodology/acled-codebook): corporate identity, title, coding scope. | No stable publication year on inspected page; access date retained. |
| `leban2014eventregistry` | D | [Official WWW archive](https://archives.iw3c2.org/www2014/proceedings/companion/p107.pdf): four authors, title, 2014, four pages numbered 107–110, DOI. | ACM landing-page fetch returned 403; full proceedings PDF supplied primary text. |
| `shao2016hoaxy` | D | [Official WWW proceedings PDF](https://archives.iw3c2.org/www2016/WWW2016-Proceedings/companion/p745.pdf), [author preprint](https://arxiv.org/abs/1603.01511), publisher DOI record: authors/title/2016/745–750/DOI. | 2016 architecture and preliminary analysis; no current Twitter access inferred. |
| `invidVerificationPlugin` | D | [Official InVID page](https://www.invid-project.eu/tools-and-services/invid-verification-plugin/): corporate title/tool features and historical releases. | Undated official webpage; no invented date; service capability not locally executed. |
| `weverifyVerificationPlugin` | D | [Official WeVerify page](https://weverify.eu/verification-plugin/): corporate title and documented 2021 redesign. | Undated webpage; 2021 redesign date is not page publication date or current service guarantee. |
| `berkeleyProtocol2022` | D | [Official co-publisher PDF](https://humanrights.berkeley.edu/wp-content/uploads/archive/2024/02/Berkeley-Protocol.pdf), [UN catalog](https://digitallibrary.un.org/record/3973652?v=pdf): title, co-publishers, 2022 imprint, report number, ISBN/eISBN. | Guidance publication; not software certification or a performance benchmark. |
| `thorne2018fever` | D+T | [ACL proceedings](https://aclanthology.org/N18-1074/): authors/title/NAACL 2018/809–819/DOI; evidence audit checked paper/task. | Benchmark corpus and metrics not transferred to Social. |
| `schlichtkrull2023averitec` | D+T | [NeurIPS record](https://papers.neurips.cc/paper_files/paper/2023/hash/cd86a30526cd1aff61d6f89f107634e4-Abstract-Datasets_and_Benchmarks.html): three authors, title, 2023/volume 36/DOI. | Unverified page range intentionally omitted. |
| `schlichtkrull2024averitec` | T | [ACL proceedings](https://aclanthology.org/2024.fever-1.1/): full author list, 2024, workshop, 1–26, DOI; see `literature_evidence.md`. | Shared-task score is joint evidence/verdict criterion, not plain accuracy. |
| `rothermel2024infact` | D+T | [ACL proceedings](https://aclanthology.org/2024.fever-1.12/): authors including **Mark** Rothermel, title, 2024/108–112/DOI. | No correction needed; evidence audit distinguishes development accuracy and test AVeriTeC score. |
| `wadden2019dygiepp` | D+T | [ACL proceedings](https://aclanthology.org/D19-1585/): author order, title, 2019, EMNLP-IJCNLP, 5784–5789, DOI. | Learned extraction evaluation differs from event-occurrence verification. |
| `cybulska2014ecbplus` | T | [ACL LREC record](https://aclanthology.org/L14-1646/): two authors, title, 2014, 4545–4552, ELRA; evidence audit checked PDF. | No DOI supplied by primary record; none invented. |
| `lebo2013provo` | D+T | [Dated W3C Recommendation](https://www.w3.org/TR/2013/REC-prov-o-20130430/): title/status/date; team audit verified three editors and final version identity. | Editorial role retained; not mistaken for 2012/2013 draft. Style-specific author warning possible. |
| `moreau2013provdm` | D+T | [Dated W3C Recommendation](https://www.w3.org/TR/2013/REC-prov-dm-20130430/): title/status/date; team audit verified Moreau/Missier editor roles. | Conceptual model distinct from PROV-O ontology; no DOI invented. |
| `Broder1997` | T | [Primary paper copy](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/broder97resemblance.pdf), [IEEE identifier](https://ieeexplore.ieee.org/document/666900); team also inspected depositor metadata. | Direct paper access/IEEE restrictions recorded in `literature_statistics.md`; conference year used. |
| `RobertsonZaragoza2009BM25` | T | [Publisher PDF](https://www.nowpublishers.com/article/DownloadEBook/INR-019): preferred-citation fields supersede conflicting deposit. | Publisher 3(4):333–389 retained; direct fetch restriction disclosed by team. |
| `Pacheco2021` | T | [Author paper](https://btrantruong.github.io/assets/pdf/uncover.pdf), [official record](https://ojs.aaai.org/index.php/ICWSM/article/view/18075); team checked DOI deposit and methods. | Official landing page bot-blocked during team audit; no claim of second direct reading here. |
| `Nizzoli2021` | T | [Institutional paper](https://iris.cnr.it/retrieve/00ebd390-5f39-42f0-92d4-ed4d8bb49a10/2021_Coordinated%20behavior%20on%20social%20media%20in%202019%20UK%20general%20election.pdf), [official record](https://ojs.aaai.org/index.php/ICWSM/article/view/18074). | One historical platform/election analysis, not universal coordination truth labels. |
| `Magelinski2022` | T | [Publisher record](https://tsjournal.org/index.php/jots/article/view/30): title with initial “A”, author middle initial, year/volume/issue/DOI. | Publisher wording retained despite shorter deposited title; no invented page range. |
| `Phipson2010` | T | [Corrected author copy](https://gksmyth.github.io/pubs/PermPValuesPreprint.pdf): authors, article identity, original 2010 publication and 2011 correction; DOI. | Corrected-copy date does not replace original year. |
| `Holm1979` | T | [Primary scan](https://sci2s.ugr.es/keel/pdf/specific/articulo/0052_001.pdf), [stable JSTOR record](https://www.jstor.org/stable/4615733): title/author/journal/year/6(2):65–70. | No DOI inferred from JSTOR number. |
| `Olteanu2019` | T | [Publisher article](https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2019.00013/full): four authors, title/year/volume/article number/DOI. | Methodological review, not measured Social bias correction. |
| `VicentePaula2023` | T | [Publisher article](https://link.springer.com/article/10.1007/s11135-023-01615-w): sole author Paula Vicente, title/year/57(6):5449–5489/DOI. | Citation key is not an author-name parse; no metadata correction needed. |

## Structural checks and access limitations

The merge/check ran with local `python3` and standard-library `re`, `collections` and `hashlib`. A brace-aware entry/field scanner handled escaped braces, nested braces, quoted values and bare month tokens, rejected duplicate fields, asserted the expected 12+8+8+9 counts, and required unique citation keys, nonempty titles and author/editor identity. DOI values were stripped of resolver prefixes and compared case-insensitively; each matched the `10.<registrant>/<suffix>` pattern. This checks syntax/uniqueness, not DOI registration or semantic correctness. No BibTeX parser package or LaTeX executable was installed for this pass; a full bibliography build belongs to the root integration step.

Observed scanner output:

```text
source_counts {'references_root.bib': 12, 'references_systems.bib': 8,
               'references_evidence.bib': 8, 'references_statistics.bib': 9}
aggregate_records 37 unique_keys 37 doi_fields 22 duplicate_dois 0 brace_or_field_errors 0
missing_year ['acledCodebook', 'invidVerificationPlugin', 'weverifyVerificationPlugin']
no_url ['pylypenko2026case']
editor_only ['lebo2013provo', 'moreau2013provdm']
currently_uncited []
currently_unknown_citations []
```

The root metadata artifact `audit/root_doi_metadata.json` is **manually transcribed primary metadata**, not a successful machine-harvested Crossref response: its five entries explicitly say the retry returned 429. No repeated Crossref query loop was run in this consolidation task. Statistics-worker successful depositor checks and publisher/depositor conflicts are recorded separately in `audit/literature_statistics.md`; those checks are inherited team evidence, not new queries claimed here. Official documentation, standards and private manuscripts need not have DOIs; absence is not a defect to repair by guessing.

Companion audits contain the substantive source reading and permissible uses: `literature_root.md`, `literature_systems.md`, `literature_evidence.md`, and `literature_statistics.md`. Bibliographic identity, access success, claim support, external validity and the present system's empirical evaluation remain separate checks.
