# ACL-oriented critical-survey draft

**When Do Hallucination Improvements Compose? A Survey of Detection, Evaluation, and Mitigation in LLMs**

Prepared 5 October 2026. This is a revised research draft, not a submitted or accepted paper. The original seven-page coursework release remains unchanged in `../manuscript/`.

## Destination-specific submission packages

Use the [separate arXiv and ACL/ARR packages](submission_packages/README.md) for uploading. Each source archive has exactly one explicit `main.tex` entry and a compiled bibliography; no anonymous/public switch is needed. The earlier dual-version Overleaf package below remains an editable master.

## Files

- [Anonymous review PDF](release/ACL_Review_Anonymous.pdf)
- [Author PDF](release/ACL_Author_Version.pdf)
- [Overleaf source ZIP](release/ACL_Overleaf_Source.zip): `main.tex` is anonymous; choose `author_version.tex` for the named version.
- [Anonymous source ZIP](release/ACL_Anonymous_Source.zip)
- [Anonymous evidence supplement](release/ACL_Anonymous_Supplement.zip)
- [Validation report](validation.json)
- [Author submission actions](review_materials/author_actions_CN.md)

## What changed

The revision centers on compatibility of evidence across detection and mitigation. It adds a fixed thirteen-study documentary audit, primary-source locators and hashes, comparison with five close surveys, four compatibility conditions, and a prospective combined-system protocol. No model experiment, independent human annotation, pooled effect, or field-wide prevalence is claimed. AI assistance and limitations are explicit.

Main content ends on page 8. The complete PDF has 23 pages including limitations/ethics, references, and appendices. There are 92 bibliography entries, four unchanged figure PDFs, and eleven tables (including appendix tables). All 55 figure citation labels match the actual ACL BibTeX output. Figure 1 remains on the right of page 1 at proportional single-column scale. Table captions remain below their tables.

## Reproduce

Use an existing TeX Live installation with `latexmk`, pdfLaTeX, and BibTeX. Run `bash scripts/build.sh`; validation and packaging require Python with `pypdf`. The source ZIP can compile on Overleaf without the Python audit scripts. This project is multipart; the build uses the existing TeX toolchain.

The build script uses `author_version.tex` explicitly because automatic root-file discovery may select `main.tex` and inadvertently build a second anonymous PDF. Check names and the repository hyperlink in the author PDF independently.

## Evidence and limits

`audit/evidence_cases.csv` is the canonical combined extraction table. `codebook.md` defines the fixed sample and coding rules. Detection/mitigation notes preserve detailed locators and uncertainty. The prior-survey record and update-search log delimit novelty and temporal coverage. Source-paper PDFs are not distributed. The supplied figure files remain byte-for-byte identical; style-file contents and ACL page geometry are unchanged.

The author still needs to verify the extraction against the cited papers, confirm identity/account/service information, and approve the final submission declarations. See the author action file. No submission, account registration, or external messages have been performed. A stronger draft is not a guarantee of ACL acceptance.
