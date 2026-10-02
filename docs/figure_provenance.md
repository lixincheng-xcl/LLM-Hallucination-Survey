# Figure provenance and use

All three diagrams are original conceptual syntheses drawn for this project. They are not screenshots or tracings of another paper. The supplied LVLM hallucination and logical reasoning surveys informed the organization and readability goals, not copied text or art.

| Figure | Purpose | Evidence / basis | Intended placement |
|---|---|---|---|
| 1 — Structure | Map the proposed seven sections | Course rubric and project outline in the Chinese preparation document | Main text |
| 2 — Taxonomy | Separate reference frame, detection evidence and intervention point | [Hallucinated but Factual](https://aclanthology.org/2022.acl-long.236/), [Factuality survey](https://aclanthology.org/2024.emnlp-main.1088/), and the individually linked methods in `method_matrix.md` | Main text |
| 3 — Evidence loop | Explain detection as part of a generation-and-control process | [CoVe](https://aclanthology.org/2024.findings-acl.212/), [CRITIC](https://proceedings.iclr.cc/paper_files/paper/2024/hash/fef126561bbf9d4467dbb8d27334b8fe-Abstract-Conference.html), [Self-RAG](https://openreview.net/forum?id=hSyW5go0v8) | Optional / appendix |

The taxonomy's reference axis is not an exhaustive universal definition of hallucination. Hybrid methods may occupy several intervention categories. The diagram is an organizing synthesis, not a learned causal graph or experimental result.

SVG files remain editable; PDF files are vector exports sized to 160 mm width; PNG files are previews. The smallest labels are approximately 7.8 pt at that width. Regenerate with `python scripts/draw_figures.py` after installing `reportlab` and `pypdfium2`. Final captions and in-text academic citations should be adapted when the manuscript is drafted.
