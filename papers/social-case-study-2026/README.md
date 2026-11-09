# Social case study, bilingual Scribe project

This project contains English and Ukrainian versions of a detailed computational case study of the 2–5 November 2026 information wave concerning Petropavlivska Borshchahivka, Ukraine.

## Manuscript format

The layout follows the conventions shared by the author's five recent Zenodo papers: single-column A4 with 25 mm margins; CMU Serif body text at 11 pt; a regular 17.28 pt title; default LaTeX section (14.4 pt bold) and subsection (12 pt bold) headings; centered title, author/affiliation/ORCID/contact block and date; an unstructured abstract and keywords on page one; numbered, plain black section headings; numeric citations; restrained tables and figures with captions in `Figure 1:` / `Table 1:` form; and a centered page number without a branded running header. The article uses an introduction, case and research questions, data and methods, results, discussion, limitations, conclusion, data statements and references. Figures retain only a restrained blue/orange data palette. No journal-specific submission template was supplied, so this is a journal-neutral preprint in the author's established article style.

## Open in Scribe

Open this folder as a project in [Scribe](https://github.com/Scribe-IDE/Scribe), then open `main.tex` (English) or `main_uk.tex` (Ukrainian). The article text is in `sections/article_en.tex` and `sections/article_uk.tex`; both use `references.bib`. This is a standard LaTeX/BibTeX project using `natbib` and `polyglossia`, rather than a Scribe-specific document format.

## Build

From this directory:

```sh
./build.sh
```

The script regenerates the bilingual vector figures from the repository's reviewed CSV/JSON artifacts, compiles both documents with Tectonic, stores temporary build files under the repository's ignored `tmp/` directory, and copies the final PDFs to the repository root. It requires Python 3, Matplotlib, and Tectonic. The exact Computer Modern Unicode OTF faces are bundled under `fonts/` with their SIL Open Font License; the document does not rely on a system font substitution. Figures use Matplotlib’s bundled DejaVu Sans. Run `tectonic -X compile --help` for engine details. This keeps build artifacts out of version control while making the release PDFs immediately visible at the top level.

## Scope and release status

Draft for analytical review; not peer reviewed and not a court or investigative finding. Internal counts are tied to the Social repository's case report, edition 3.1 (9 November 2026), the 8 November automated-case-run snapshot, and individually named supporting artifacts. The private repository contains some data that cannot be republished here; platform data are incomplete and collected under a purposive design. Before public release, confirm the data-sharing/ethics statement, and independently re-check every cited case source and final figure.

No raw usernames, private-channel content, or personal profile data are reproduced. Numerical totals are descriptive of the observed corpora and snapshots, not population estimates or unique reach.
