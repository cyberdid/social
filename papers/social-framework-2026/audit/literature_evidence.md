# Verified literature: evidence verification, event extraction/coreference, provenance

Verified on 2026-11-10 against primary publisher/proceedings pages, published PDFs and versioned W3C Recommendations. Scope: eight records in `manuscript/references_evidence.bib`. This file is a source audit, not manuscript prose. Numbers below are the cited authors' benchmark results; none measures Social. Local implications are explicitly separated from findings in the literature. Author lists, publication years, venues, pages and DOIs were checked when included; the NeurIPS page range is omitted because it was not verified in the accessible primary metadata.

## 1. FEVER dataset (2018)

**Key:** `thorne2018fever`. James Thorne, Andreas Vlachos, Christos Christodoulopoulos and Arpit Mittal. *FEVER: a Large-scale Dataset for Fact Extraction and VERification*. NAACL-HLT 2018, Volume 1 (Long Papers), pp. 809–819. DOI: `10.18653/v1/N18-1074`.

**Verified method/result:** 185,445 claims were created by modifying Wikipedia sentences. Separate annotators assigned supported/refuted/not-enough-information labels without seeing the originating sentence; evidence sentences accompany the first two labels. Reported Fleiss' kappa is 0.6841. The paper's pipeline reaches 31.87% when correctness requires the label and correct evidence, compared with 50.91% label accuracy when evidence correctness is ignored. These are different evaluation conditions, not interchangeable accuracies. [Primary proceedings record and abstract](https://aclanthology.org/N18-1074/).

**Limit / local implication:** Wikipedia-derived claims differ from naturally occurring incident reports. FEVER motivates evaluating evidence selection and verdict jointly; a correct substring or declared assessment state is insufficient. It does not validate Social's curated Ukrainian incident judgments. The [official task definition](https://fever.ai/2018/task.html) additionally specifies that evidence-complete verification requires at least one complete annotated evidence set and considers only the first five predicted sentences.

## 2. AVeriTeC dataset (2023)

**Key:** `schlichtkrull2023averitec`. Michael Schlichtkrull, Zhijiang Guo and Andreas Vlachos. *AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web*. *Advances in Neural Information Processing Systems*, 36, Datasets and Benchmarks Track. DOI: `10.52202/075280-2842`, as listed by the proceedings.

**Verified method/result:** The dataset contains 4,568 real-world claims from fact-checks by 50 organizations. Claims have evidence-linked question-answer pairs and textual explanations connecting evidence to a verdict. Multi-round annotation addresses context dependence, evidence sufficiency and temporal leakage. Verdict agreement is reported as kappa 0.619; the work also introduces a QA-oriented open-web verification baseline and evaluation scheme. [Primary NeurIPS record](https://papers.neurips.cc/paper_files/paper/2023/hash/cd86a30526cd1aff61d6f89f107634e4-Abstract-Datasets_and_Benchmarks.html).

**Limit / local implication:** This is a selected fact-check corpus with human annotations, not a complete census of claims or an infallible truth oracle. The agreement statistic measures annotation agreement, not model accuracy. Social could adopt explicit evidence sufficiency and knowledge-time evaluation; citing this dataset does not supply the missing independent gold labels for Social. No unverified baseline score is copied here.

## 3. AVeriTeC shared task (2024)

**Key:** `schlichtkrull2024averitec`. Michael Schlichtkrull, Yulong Chen, Chenxi Whitehouse, Zhenyun Deng, Mubashara Akhtar, Rami Aly, Zhijiang Guo, Christos Christodoulopoulos, Oana Cocarascu, Arpit Mittal, James Thorne and Andreas Vlachos. *The Automated Verification of Textual Claims (AVeriTeC) Shared Task*. Seventh FEVER Workshop, pp. 1–26. DOI: `10.18653/v1/2024.fever-1.1`. [Primary metadata](https://aclanthology.org/2024.fever-1.1/).

**Verified method/result:** Teams retrieve evidence via web search or a provided knowledge store and predict verdicts. AVeriTeC@0.25 credits a correct verdict only when question-plus-answer Hungarian METEOR evidence score meets 0.25. Twenty-one submissions participated; eighteen beat the baseline. Table 2 reports winner TUDA_MAI at 0.63, versus baseline 0.11, over 2,214 hidden-test examples. The paper added 1,215 claims to the original 4,568; total dataset size and evaluated hidden-test size are distinct. [Published PDF, §§2–3 and Table 2](https://aclanthology.org/2024.fever-1.1.pdf).

**Limit / local implication:** Lexical evidence matching is a proxy; thresholded benchmark success is not direct truth measurement. The store guarantees gold-evidence inclusion and differs from unrestricted discovery. Do not call 0.63 plain verdict accuracy, or compare it to Social's accepted-assessment fraction.

## 4. InFact (2024)

**Key:** `rothermel2024infact`. Mark Rothermel, Tobias Braun, Marcus Rohrbach and Anna Rohrbach. *InFact: A Strong Baseline for Automated Fact-Checking*. Seventh FEVER Workshop, pp. 108–112. DOI: `10.18653/v1/2024.fever-1.12`. [Primary metadata](https://aclanthology.org/2024.fever-1.12/).

**Verified method/result:** Six stages interpret a claim, generate ten questions, retrieve evidence for each, answer, predict a verdict and generate a justification. The authors describe a static single-pass pipeline; per-question resource retrieval/answer selection occurs within that fixed structure. Dense retrieval searches the AVeriTeC knowledge store. With GPT-4o, the text reports 62.6% **test AVeriTeC score** (rounded to 63% in the abstract/table) and 72.4% **development verdict accuracy**. The generated final justification is not scored by those metrics. [Published PDF, §§2–3, Figure 1 and Tables 1–2](https://aclanthology.org/2024.fever-1.12.pdf).

**Limit / local implication:** Results depend on the task's evidence store and LLM backbone. The paper's qualitative disagreement analysis is not an independent proof that model verdicts supersede annotation. This is a concrete comparator for bounded staged automation; six stages do not by themselves imply adaptive investigation or validated source authenticity.

## 5. DyGIE++ (2019)

**Key:** `wadden2019dygiepp`. David Wadden, Ulme Wennberg, Yi Luan and Hannaneh Hajishirzi. *Entity, Relation, and Event Extraction with Contextualized Span Representations*. EMNLP-IJCNLP 2019, pp. 5784–5789. DOI: `10.18653/v1/D19-1585`. [Primary metadata](https://aclanthology.org/D19-1585/).

**Verified method/result:** The supervised multitask model enumerates spans, contextualizes them with BERT and dynamic graph propagation, then scores entities, relations, event triggers and arguments. Table 1 reports ACE05-Event test F1 of 73.6 for trigger classification and 52.5 for argument classification; the event configuration uses a four-model ensemble for trigger detection. Argument-identification F1 is 55.4 versus the prior comparator's 57.2, so “improved every subtask” is unsupported. [Published PDF, §§2–4 and Table 1](https://aclanthology.org/D19-1585.pdf).

**Limit / local implication:** These metrics evaluate annotated extraction, not whether reported events occurred. They do not establish cross-document physical-event identity, causal reconstruction, or performance on Ukrainian/Russian incident data. The work makes the distinction between raw-text learned extraction and Social's organization of pretyped mentions concrete.

## 6. ECB+ (2014)

**Key:** `cybulska2014ecbplus`. Agata Cybulska and Piek Vossen. *Using a sledgehammer to crack a nut? Lexical diversity and event coreference resolution*. LREC 2014, pp. 4545–4552, European Language Resources Association. No DOI is supplied by the primary record. [Primary metadata](https://aclanthology.org/L14-1646/).

**Verified method/result:** The authors diagnose how a corpus with largely one salient event instance per topic can make event coreference resemble topic classification. Their within-topic lemma baseline approaches 65% CoNLL F-score on the original ECB (§3.3). They add 502 texts covering different instances of event types already represented by ECB's 43 topics, creating ECB+. Annotation includes events, times, entities and coreference. [Published PDF, §§3.3–4](https://aclanthology.org/L14-1646.pdf).

**Limit / local implication:** A news corpus and lemma-baseline diagnostic do not constitute physical-event verification. Similar predicates/topics can refer to different events; entity, location and temporal distinctions matter. This directly motivates challenge cases for Social's event links and its separation of the incident from a later fire, without treating curator-supplied cannot-link constraints as automatically discovered identity judgments.

## 7. PROV-O final Recommendation (2013)

**Key:** `lebo2013provo`. Timothy Lebo, Satya Sahoo and Deborah McGuinness, editors. *PROV-O: The PROV Ontology*. W3C Recommendation, **30 April 2013**. Stable version: `REC-prov-o-20130430`.

**Verified specification:** PROV-O expresses the PROV data model using OWL 2 and supplies classes, properties and restrictions for representing and exchanging provenance. Core terms include entity, activity and agent, plus derivation, attribution, association, generation and usage relations. The header and document status explicitly identify this as a Recommendation; the December 2012 candidate and March 2013 proposed versions are different documents. [Final version, header, abstract and §3](https://www.w3.org/TR/2013/REC-prov-o-20130430/).

**Limit / local implication:** This is a normative representation standard, not an empirical fact-checking result. Recording provenance supports inspection but does not make the recorded claim true or the cited sources independent. Social's JSON/SQLite provenance fields are conceptually relatable to PROV terms; the audit found no basis to claim tested PROV-O conformance, RDF export or ontology-level interoperability.

## 8. PROV-DM final Recommendation (2013)

**Key:** `moreau2013provdm`. Luc Moreau and Paolo Missier, editors. *PROV-DM: The PROV Data Model*. W3C Recommendation, **30 April 2013**. Stable version: `REC-prov-dm-20130430`.

**Verified specification:** The domain-independent conceptual model covers entities/activities and their times, derivation, responsible agents, provenance bundles, links between entities referring to the same thing, and collections. PROV-DM supplies concepts; PROV-O supplies their OWL/RDF representation. [Final version, header and abstract](https://www.w3.org/TR/2013/REC-prov-dm-20130430/).

**Limit / local implication:** The specification provides no performance score or truth guarantee. A ledger can document who produced a claim/assessment and from which artifact without demonstrating evidential entailment. Cite PROV-DM for the conceptual provenance architecture and PROV-O only when discussing its ontology representation; do not conflate either with a cryptographic integrity or independent verification protocol.

## Use in the paper

- Literature-backed distinctions: retrieval versus verdict; joint evidence/verdict evaluation versus label-only accuracy; learned extraction versus supplied-mention organization; event coreference versus topic similarity; provenance representation versus evidential truth.
- Local interpretation: Social's implemented contracts/receipts can be situated against these methods, but no reviewed benchmark score establishes Social's performance. AVeriTeC and InFact are external comparators, not evaluated baselines in this repository.
- Bibliographic checks: all eight keys are unique; all records have verified primary URLs. ACL records preserve published page ranges and DOI fields. W3C records preserve editor roles and the dated final Recommendations. No arXiv preprint is substituted for a verified final publication, and no unverified page range or DOI is invented.
