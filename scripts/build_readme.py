from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];ps=json.loads((R/'data/papers.json').read_text())
intro='''# Hallucination in Large Language Models

### A Survey of Detection, Evaluation, and Mitigation

**7 main pages · 4 figures · 9 main-table benchmarks · 88 references · ACL format**

[Read the survey (PDF)](manuscript/LLM_Hallucination_Survey.pdf) · [Overleaf source ZIP](release/LLM_Hallucination_Survey_Overleaf.zip) · [LaTeX source](manuscript/main.tex) · [Build and validation](manuscript/README.md)

Completed coursework survey by **Xincheng Li, University of Auckland**. The paper compares text-LLM hallucination detection, evaluation, and mitigation by reference frame, available evidence, and intervention location. It covers QA, long-form generation, summarization, grounded dialogue, and retrieval-augmented generation. It is a narrative literature synthesis, not a new empirical model or an accepted conference paper.

**Release:** 2 October 2026. **Literature snapshot:** 1 October 2026. The main paper occupies pages 1–7; references and appendices follow separately. The paper cites **86 research studies + 2 visual-design sources**. The discovery library retains **87 studies**, so library inclusion and manuscript citation counts differ. This is a dated curated collection, not an exhaustive systematic review or a continuously updating service.

## Figures and logical structure

The manuscript uses the author's four revised PDFs without alteration, each at full two-column text width. The PNGs below are previews of those exact PDFs. Original figure files and SHA-256 digests are in [manuscript/figures](manuscript/figures/manifest.json).

1. **Fig. 1 — Examples:** defines unsupported versus contradicted source claims.
2. **Fig. 2 — Survey structure:** navigates concepts, detection, evaluation, mitigation, and analysis.
3. **Fig. 3 — Evaluation taxonomy:** separates generated-answer quality from detector performance.
4. **Fig. 4 — Causes and mitigation:** maps potential failure points to interventions, whose outcomes return to Fig. 3 and Table 1 for independent evaluation.

![Fig. 1: constructed hallucination examples](manuscript/figures/Fig1_hallucination_examples.png)
![Fig. 2: structure of the survey](manuscript/figures/Fig2_survey_structure.png)
![Fig. 3: evaluation taxonomy](manuscript/figures/Fig3_evaluation_taxonomy.png)
![Fig. 4: potential causes and mitigation](manuscript/figures/Fig4_causes_mitigation.png)

[Main-text benchmark table source](manuscript/sections/table1.tex) · [Earlier editable draw.io sources](figures/drawio/README.md) · [ACL citation-label proof](bibliography/acl_label_proof/README.md)

The native draw.io files predate the author's final PDF edits and are retained as editable working sources; they are not claimed to reproduce the revised PDFs byte-for-byte. Earlier SVG/PDF assets under `figures/reference_style/` are archived design-stage artifacts, not the submitted artwork.

World factuality and source faithfulness are distinct. Unsupported content is not necessarily false in the world; faithful use of false evidence can still produce false answers. Fig. 1 is constructed, not measured output. Fig. 4 is a mechanism synthesis, not a causal experiment. Visual-design sources are acknowledged in captions.

## Evidence and reproducibility

- [Final build and citation audit](docs/manuscript_validation.md)
- [Detection/evaluation evidence ledger](data/manuscript_detection_evidence.csv)
- [Mitigation/analysis evidence ledger](data/manuscript_mitigation_evidence.csv)
- [Manuscript citation status](data/manuscript_citations.csv)
- [Search and screening protocol](docs/screening_protocol.md)
- [15-benchmark matrix](docs/benchmark_matrix.md) and [21-method matrix](docs/method_matrix.md)
- [Seven evidence tensions](docs/evidence_tensions.md)
- [CSV](data/papers.csv), [JSON](data/papers.json), [BibTeX](bibliography/references.bib), [RIS / Zotero mapping](bibliography/zotero_collections.csv)

The comparison tables are qualitative, not cross-paper leaderboards. Appendix material records benchmark counting caveats, complementary studies, access requirements, and a common reporting protocol. All selected studies received title/abstract screening; detailed arguments use targeted primary-source checks recorded in the ledgers. This does not claim every paper was fully read or independently reproduced. Original research-paper PDFs are not redistributed.

## Collection snapshot

| Year | 2022 | 2023 | 2024 | 2025 | 2026 | Total |
|---|---:|---:|---:|---:|---:|---:|
| Studies | 6 | 20 | 29 | 22 | 10 | **87** |

The discovery library contains 60 main-conference, 21 Findings, and 6 journal papers, including 80 ACL Anthology records. The two preprint-version design references are kept separately and are not counted among these 87 studies. Formal publication year is used for the research library.

## Reading map

[Foundations](#foundations) · [Detection](#detection) · [Evaluation](#evaluation) · [Mitigation](#mitigation) · [Analysis](#analysis)

Primary categories support navigation; subcategories and inclusion reasons are in the data files. Curator questions are proposed checks, not claims of demonstrated defects.

'''
text=intro
for cat in ['Foundations','Detection','Evaluation','Mitigation','Analysis']:
 text+='## '+cat+'\n\n| Study | Paper | Venue | Subcategory |\n|---|---|---|---|\n'
 for p in sorted((p for p in ps if p['category']==cat),key=lambda p:(-p['year'],p['short_name'])):
  text+=f"| {p['record_id']} · {p['short_name']} | [{p['title']}]({p['url']}) | {p['venue']} | {p['subcategory']} |\n"
 text+='\n'
text+='''## Use and maintain this collection

- Import `bibliography/references.bib` into an ACL project or `references.ris` into a reference manager. The final manuscript uses the citation set recorded in `data/manuscript_citations.csv`.
- For Zotero, use the collection mapping and category-specific RIS files. A flat RIS import does not automatically recreate nested collections.
- Check [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a correction. Changes should preserve the primary source, publication type, inclusion rationale and verification date.
- `python scripts/validate_resources.py` checks local metadata, bibliography counts and linked artifacts. `scripts/build_reference_style_assets.py` and `scripts/write_figure_integration.py` regenerate historical design-stage assets and fragments; they do not overwrite the author-supplied final PDFs. The earlier `scripts/draw_figures.py` regenerates only the three legacy diagrams.
- Raw metadata can be re-fetched using `scripts/fetch_acl.py`. Its cache is local and excluded from version control. The log and SHA-256 manifest describe the original snapshot; re-fetching later may produce different files.

## Acknowledgments and scope

Repository organization was informed by [Liu et al.'s LVLM Hallucinations Survey](https://github.com/lhanchao777/LVLM-Hallucinations-Survey). Our scope is text generation. The new diagrams were redrawn with project-specific text, examples and methods. Their layouts explicitly adapt the supplied LVLM and logical-reasoning surveys; see the design attribution notes. Two design references are recorded separately from the 87 content studies. Source-paper photographs and manuscript prose are not reused.

This repository release is a completed coursework manuscript, not a claim of peer-reviewed publication. No DOI, acceptance badge, or new experimental result is claimed. Paper rights remain with their respective authors and publishers. See [RIGHTS.md](RIGHTS.md).
'''
(R/'README.md').write_text(text)
print('README contains',len(ps),'linked paper entries')
