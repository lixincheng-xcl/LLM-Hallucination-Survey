# ACL survey manuscript

**Hallucination in Large Language Models: A Survey of Detection, Evaluation, and Mitigation**
Xincheng Li — School of Computer Science, University of Auckland
Email: xli798@aucklanduni.ac.nz

- Main paper: **pages 1–7**.
- References: **pages 8–13**, 86 research studies and two credited design sources.
- Appendices: **pages 14–18**, selection/provenance, benchmark caveats, complementary evidence, and reporting protocol.
- Figures 1–2 have readability refinements; Figure 3 is unchanged; Figure 4 has one corrected method label. Figures 1, 2, and 4 include editable draw.io sources. Figure 1 occupies the right column of page 1 at its natural aspect ratio; Figures 2–4 use full two-column text width. The benchmark and compact method-comparison tables are native LaTeX. All eight numbered tables place their captions below the table body, following the supplied ACL example.
- Actual ACL BibTeX output matches all 55 distinct studies cited inside the diagrams, including the six disambiguation groups.

This is a coursework survey and repository release, not an accepted ACL conference paper. It reports no new experiments. The library and paper have different counts: one of the 87 screened studies is retained in the library but not cited in the paper.

## Build

The supplied official `acl.sty` and `acl_natbib.bst` are unchanged. `main.tex` uses `preprint` mode to display the author's name and page numbers. No font or margin compression is applied. The main text, references, and appendix prose use ACL's two-column format; wide tables use spanning floats. A dedicated Limitations section fits within the seven main pages.

From this directory, using a TeX installation with `latexmk` and BibTeX:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

From the repository root, with Python and `pypdf` available:

```sh
python3 scripts/validate_manuscript.py
```

The validator checks seven main pages, the bibliography start, 88 entries, imported-figure hashes, figure citation labels, the two main tables, all eight table captions below their table bodies, Figure 1 placement and proportional scaling, the GitHub link in the abstract’s final sentence, affiliation/email, dedicated Limitations, removal of main-caption production commentary, two-column appendix prose, unresolved references, and overfull boxes. Visual review is recorded in `../docs/manuscript_validation.md`. The checked release PDF is `LLM_Hallucination_Survey.pdf`.

For Overleaf, import `../release/LLM_Hallucination_Survey_Overleaf.zip`, set `main.tex` as the main document, and use pdfLaTeX. All style, bibliography, section, and figure files are bundled. The release ZIP excludes build intermediates and historical artwork.

## Artwork and sources

`figures/manifest.json` records SHA-256 digests and the provenance of the supplied and revised PDFs. PNGs are only README previews. The authoritative revised sources for Figures 1, 2, and 4 are bundled in this package alongside their PDFs. Figure citation mappings are retained in `../data/figure_citation_map.json`; historical artwork is not included in the repository.

Original academic sources are linked in the bibliography; their PDFs are not bundled. The two visual-design surveys are credited in Appendix A. Figure 1 is a constructed example, and Figure 4 is a qualitative synthesis, not measured causal evidence.
