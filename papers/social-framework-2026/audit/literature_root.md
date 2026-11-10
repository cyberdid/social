# Primary literature audit: root scope

Inspected 2026-11-10. Manually verified metadata for five DOI records are stored in root_doi_metadata.json. Publisher/author pages were read; no citation counts or secondary summaries are treated as evidence. Per-source discussion in the manuscript is deliberately bounded, and no external benchmark score is transferred to Social.

| Key | Primary source | Relevant method/result | Boundary |
|---|---|---|---|
| imran2015crisis | https://mimran.me/papers/processing_social_media_messages_in_mass_emergency_survey.pdf | Survey of crisis social-media filtering, classification, extraction and summarization | Review/context, not an evaluation of Social |
| wilkinson2016fair | https://www.nature.com/articles/sdata201618 | Findability/accessibility/interoperability/reuse; provenance for data/software/workflows | Guiding principles, not certification or proof that private artifacts are reusable |
| wilson2017practices | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510 | Organized data, documented programs, version tracking and collaboration practices | Professional research-computing guidance, not quantitative accuracy |
| sandve2013reproducible | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285 | Retain inputs, programs, parameters, intermediate results and randomness for computational replay | Replay does not validate substantive truth |
| smith2007tesseract | https://research.google/pubs/an-overview-of-the-tesseract-ocr-engine/ | OCR architecture, line finding and adaptive character recognition | Historical algorithm paper; no Social OCR ground truth |
| radford2023whisper | https://proceedings.mlr.press/v202/radford23a.html | Large-scale weak multilingual supervision (680000traininghours), zero-shot benchmark generalization | FoundationalWhisperstudy, not measurement of convertedsmall/turbo models onSocial |
| lewis2020rag | https://proceedings.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html | Parametric+retrievedWikipedia memory; improvement on knowledge-intensiveQA | Social has lexical retrieval and deterministic processors, not trainedRAG architecture; retrieval alone no truth guarantee |
| gao2023alce | https://aclanthology.org/2023.emnlp-main.398/ | Separate correctness/fluency/citation metrics; bestsystems lack completecitation support50% onELI5 inthatstudy | External generationbenchmark, not Social score; useful design distinction |
| dementieva2025emobench | https://aclanthology.org/2025.findings-emnlp.107/ | Crowdsourced Ukrainian emotion data and lexical/translated/LLM comparisons | Relevant future local validation, no transfer quality claim |
| systran2026faster | https://github.com/SYSTRAN/faster-whisper | CTranslate2 local implementation, CPU/GPU operational and benchmarking instructions | Software documentation; speed claims are not rerun inSocialaudit |
| telegram2026reactions | https://core.telegram.org/api/reactions | MTProto reaction constructors/counters and access-dependent lists | Current snapshots do not recover historical timeseries or imply supportforpoliticalclaims |
| pylypenko2026case | Local previous case manuscript | Context and separate application study | Private draft, publicationstatus unestablished; not independent evidence; denominator corrections tracked innewaudit |
