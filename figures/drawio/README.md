> **Final manuscript update (2026-10-02):** The completed paper is in `manuscript/`. Its author-supplied revised PDFs are authoritative. This document describes an earlier preparation/design stage; see `docs/manuscript_validation.md` for final counts and checks.

# Editable draw.io figures

Four separate native diagrams, saved and visually checked in draw.io desktop on 2026-10-02. PNG previews were exported from that application at 200% with a diagram copy included.

| Figure | Editable source | Preview |
|---|---|---|
| 1: hallucination examples | [Fig1](Fig1_hallucination_examples.drawio) | [PNG](Fig1_hallucination_examples.png) |
| 2: survey structure | [Fig2](Fig2_survey_structure.drawio) | [PNG](Fig2_survey_structure.png) |
| 3: evaluation taxonomy | [Fig3](Fig3_evaluation_taxonomy.drawio) | [PNG](Fig3_evaluation_taxonomy.png) |
| 4: causes and mitigation | [Fig4](Fig4_causes_mitigation.drawio) | [PNG](Fig4_causes_mitigation.png) |

The diagrams were assembled as native mxGraph rectangles, ellipses, text and connectors, then opened, saved and exported through the draw.io interface. They contain no flattened screenshot or embedded SVG/image. Most labelled nodes are grouped so their frames and text move together; double-click into a group or ungroup it to edit individual components. Some connecting branches use fixed editable waypoints; moving a node may require adjusting the adjacent branch.

The content, numbering and colours follow the reviewed diagrams. Fig1 remains a constructed text-source example, not measured model output. Fig2 has 12 green nodes with 4–5 citations each. Fig3 and Table 1 share the nine benchmarks. Fig4 retains the evaluation feedback path.

Citation suffixes come from [actual ACL BibTeX output](../../bibliography/acl_label_proof/README.md). The six collisions include the five content-study pairs and the Liu 2024 design-source pair. [Validation](validation.json) records native-object and citation checks. Layout/design attribution remains in the [LaTeX captions](../reference_style/figure_includes.tex).

Run `python3 scripts/validate_drawio_citations.py` from the repository root to audit the current native sources and vector PDFs against the ACL label map. PNGs and source PDFs are caption-free; the ACL float controls the final figure caption. The full seven-page paper has not yet been typeset.
