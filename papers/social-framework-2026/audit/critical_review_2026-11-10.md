# Critical review of the Social system paper

Date: 10 November 2026. Reviewer: one AI system (Claude) working in one session, using the four review roles from the task. This is not independent or human peer review. The three Codex reviewers started on 10 November stopped at a usage limit and returned no findings.

| Role | Severity | Finding | Resolution |
|---|---|---|---|
| A Methodology | Major | Semantic failure was shown only by two examples, with no measured rate | Added an authored 534-case stress test comparing rule v1 and v2 (Section 11.1), labeled as not a blind benchmark |
| A Methodology | Major | Text said no core code changed, which became false after rule v2 | Reworded; baseline results stay separate from the disclosed post-audit revision |
| A Methodology | Minor | Research questions were not answered explicitly | Added Section 13.2 |
| A Methodology | Open | One incident, no matched organic controls, no independent gold set | Stated as limitations; not resolvable with current data |
| B Architecture | Checked | File names cited in tables exist in the repository; autonomy levels agree with the audited runners | No change |
| B Architecture | Minor | Claim that a clean environment was not evaluated was out of date | Replaced with clean-clone result: 788 of 794 tests pass, six need ignored local data |
| C Evidence | Major | Bail, injury and walking passages were accepted by rule v1 | v2 withholds them; matrix written to a new file, 9 November artifact unchanged |
| C Evidence | Major | Case preprint assigned 49 and 459 to the relevant subset | Corrected in both language editions |
| C Evidence | Minor | Two remaining support pairs are weak (60 days from "two months"; police called versus arrived) | Disclosed in Section 11.1 |
| C Evidence | Major | AI disclosure described review critiques that had not completed | Rewritten to state what happened |
| D Editorial | Minor | Figure text used DejaVu and overflowed boxes | CMU Serif embedded through TrueType conversion; box text resized; all figure pages inspected |
| D Editorial | Minor | Five BibTeX warnings, one overfull table cell, malformed case-study reference | Fixed |

Not done: independent human review, new DOI verification beyond `bibliography_audit.md`, public code release, and Zenodo publication.
