# ACL survey manuscript

**Hallucination in Large Language Models: A Survey of Detection, Evaluation, and Mitigation**
Xincheng Li — University of Auckland

- Main paper: **pages 1–7**.
- References: **pages 8–13**, 86 research studies and two credited design sources.
- Appendices: **pages 14–18**, selection/provenance, benchmark caveats, complementary evidence, and reporting protocol.
- Four user-edited PDFs are included unchanged at full two-column text width (Figures 1–4). The nine-benchmark table is native LaTeX.
- Actual ACL BibTeX output matches all 55 distinct studies cited inside the diagrams, including the six disambiguation groups.

This is a coursework survey and repository release, not an accepted ACL conference paper. It reports no new experiments. The library and paper have different counts: one of the 87 screened studies is retained in the library but not cited in the paper.

## Build

The supplied official `acl.sty` and `acl_natbib.bst` are unchanged. `main.tex` uses `preprint` mode to display the author's name and page numbers. No font or margin compression is applied. Appendices use one-column tables for readability; the main paper and references use ACL's two-column format.

From this directory, using a TeX installation with `latexmk` and BibTeX:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

From the repository root, with Python and `pypdf` available:

```sh
python3 scripts/validate_manuscript.py
```

The validator checks seven main pages, the bibliography start, 88 entries, imported-figure hashes, figure citation labels, unresolved references, and overfull boxes. Visual review is recorded in `../docs/manuscript_validation.md`. The checked release PDF is `LLM_Hallucination_Survey.pdf`.

For Overleaf, import `../release/LLM_Hallucination_Survey_Overleaf.zip`, set `main.tex` as the main document, and use pdfLaTeX. All style, bibliography, section, and figure files are bundled. The release ZIP excludes build intermediates and historical artwork.

## Artwork and sources

`figures/manifest.json` records SHA-256 digests for the author's supplied final PDFs. PNGs are only README previews. Prior native draw.io working files are outside this package in `../figures/drawio/`; the later PDF edits are not claimed to be reflected in those native files.

Original academic sources are linked in the bibliography; their PDFs are not bundled. The two visual-design surveys are credited in figure/table captions. Figure 1 is a constructed example, and Figure 4 is a qualitative synthesis, not measured causal evidence.
