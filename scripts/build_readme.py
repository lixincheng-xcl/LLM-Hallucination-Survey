from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];ps=json.loads((R/'data/papers.json').read_text())
intro='''# Hallucination in Large Language Models

### A Survey of Detection, Evaluation, and Mitigation

**87 curated studies · 2022–2026 · text generation · 80 ACL Anthology papers**

This repository supports an in-preparation, seven-page ACL-format survey. It organizes text hallucination research by the reference used to judge an error, the evidence used to detect it, and the location of a mitigation intervention. It covers open-ended QA, long-form generation, summarization, grounded dialogue and retrieval-augmented generation.

**Status:** literature screening, outline, diagrams and comparison tables are available. The survey manuscript has **not** been written or published. This is a dated curated snapshot, not a continuously running update service or an exhaustive systematic review.

Search snapshot: **1 October 2026** · Preparation release: **2 October 2026**.

[中文研究准备与七页规划](docs/研究准备与七页规划.md) · [Screening protocol](docs/screening_protocol.md) · [CSV](data/papers.csv) · [JSON](data/papers.json) · [BibTeX](bibliography/references.bib) · [RIS / Zotero](bibliography/references.ris)

## Survey structure

![The structure of this survey](figures/figure_1_survey_structure.svg)

[Editable SVG](figures/figure_1_survey_structure.svg) · [Vector PDF](figures/figure_1_survey_structure.pdf)

## Taxonomy

![Three-axis taxonomy](figures/figure_2_taxonomy.svg)

[Editable SVG](figures/figure_2_taxonomy.svg) · [Vector PDF](figures/figure_2_taxonomy.pdf) · [Figure provenance](docs/figure_provenance.md)

World factuality and source faithfulness are separate criteria: unsupported content is not necessarily false, and a response faithful to an incorrect source can still be false. The detection and intervention axes are non-exclusive; hybrid methods can occupy several leaves. This is an original organizing synthesis, not a claim of a universally accepted taxonomy.

## Comparison resources

| Resource | What it compares |
|---|---|
| [15-benchmark matrix](docs/benchmark_matrix.md) | Task, reference, annotation granularity, evaluation target and comparability limits |
| [21-method matrix](docs/method_matrix.md) | Mechanism, model access, supervision, dominant cost and limitations |
| [Seven evidence tensions](docs/evidence_tensions.md) | Conflicting findings, likely confounds and testable research questions |
| [Evidence-to-response diagram](figures/figure_3_evidence_loop.svg) | How detection connects to retrieval, revision and abstention |
| [Screening ledger](data/screening_log.csv) | Included, automatically triaged and unreviewed reserve records |
| [Zotero collection mapping](bibliography/zotero_collections.csv) | Hierarchical categories and import files |

The matrices are qualitative syntheses, not a cross-paper leaderboard. Scores obtained under different model versions, prompts, source corpora, label definitions or evaluation protocols are not directly ranked.

## Collection snapshot

| Year | 2022 | 2023 | 2024 | 2025 | 2026 | Total |
|---|---:|---:|---:|---:|---:|---:|
| Studies | 6 | 20 | 29 | 22 | 10 | **87** |

Publication types: **60 main-conference papers, 21 Findings papers, 6 journal papers**. The collection contains no preprint-only entries. Findings is explicitly distinguished from main conferences. Formal publication year is used rather than an earlier arXiv submission year.

All included papers were screened at title/abstract level; selected full-text passages of 15 representative Anthology papers were inspected. This is not a claim to have fully read or reproduced all 87 studies. Every record links to a primary publication source and records its screening/read status. The public repository does not redistribute paper PDFs or full source abstracts.

## Reading map

- [Foundations](#foundations)
- [Detection](#detection)
- [Mitigation](#mitigation)
- [Evaluation](#evaluation)
- [Analysis](#analysis)

The following primary category is for navigation. See the CSV/JSON for subcategories, inclusion rationale and curator questions. These questions are proposed review checks, not claims of demonstrated defects.

'''
text=intro
for cat in ['Foundations','Detection','Mitigation','Evaluation','Analysis']:
 text+='## '+cat+'\n\n| Study | Paper | Venue | Subcategory |\n|---|---|---|---|\n'
 for p in sorted((p for p in ps if p['category']==cat),key=lambda p:(-p['year'],p['short_name'])):
  text+=f"| {p['record_id']} · {p['short_name']} | [{p['title']}]({p['url']}) | {p['venue']} | {p['subcategory']} |\n"
 text+='\n'
text+='''## Use and maintain this collection

- Import `bibliography/references.bib` into an ACL project or `references.ris` into a reference manager. Include only studies actually discussed in the eventual manuscript.
- For Zotero, use the collection mapping and category-specific RIS files. A flat RIS import does not automatically recreate nested collections.
- Check [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a correction. Changes should preserve the primary source, publication type, inclusion rationale and verification date.
- `python scripts/validate_resources.py` checks local metadata, bibliography counts and linked artifacts. `python scripts/draw_figures.py` regenerates the vector diagrams with `reportlab` and `pypdfium2`.
- Raw metadata can be re-fetched using `scripts/fetch_acl.py`. Its cache is local and excluded from version control. The log and SHA-256 manifest describe the original snapshot; re-fetching later may produce different files.

## Acknowledgments and scope

Repository organization was informed by [Liu et al.'s LVLM Hallucinations Survey](https://github.com/lhanchao777/LVLM-Hallucinations-Survey). Our scope is text generation. The diagrams, curation notes and comparison matrices here are original; the source repository's survey prose and figures have not been copied.

The title is a working title, not a published paper. No manuscript BibTeX citation, DOI, acceptance badge or experimental result is claimed. Paper rights remain with their respective authors and publishers. See [RIGHTS.md](RIGHTS.md).
'''
(R/'README.md').write_text(text)
print('README contains',len(ps),'linked paper entries')
