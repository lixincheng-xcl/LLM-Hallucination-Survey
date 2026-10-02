# Final manuscript validation — 2 October 2026

## Delivered scope

The completed English survey is **Hallucination in Large Language Models: A Survey of Detection, Evaluation, and Mitigation**, by Xincheng Li, University of Auckland. It uses the supplied ACL style without margin or font changes. The PDF has **18 pages: 7 main pages, 6 reference pages, and 5 appendix pages**. It reports no new experiments and does not claim exhaustive systematic coverage.

## Figures and narrative closure

The author's four revised PDFs were copied byte-for-byte and retained at full two-column width. Hashes are in `manuscript/figures/manifest.json`.

| Component | PDF page | Role and connection |
|---|---:|---|
| Fig. 1 | 2 | Synthetic unsupported/contradicted source examples; the caption distinguishes unsupported from world-false. |
| Fig. 2 | 3 | Section navigation; all printed section numbers match the final paper. |
| Fig. 3 | 4 | Evaluation target taxonomy, instantiated by Table 1. |
| Table 1 | 5 | Nine benchmark corpora with task-specific metrics and count caveats. |
| Fig. 4 | 6 | Potential failures and interventions, linked in caption/prose to Fig. 3 and Table 1 for independent evaluation. |

The final PDFs do not include the former Figure 4 feedback arrow. The paper describes an evaluation loop *linking* the figures and table, rather than falsely claiming that arrow is still present. Earlier draw.io and SVG assets are preserved as design-stage working files, not substituted for the user-edited artwork.

## Technical and source checks

- Reviewed source support versus world correctness, the three detection families, generation versus detector evaluation, and hybrid mitigation classification.
- Confirmed Lookback Lens requires supervised labels; FactAlign uses fKTO; RHIO spans training and decoding; TruthX learns auxiliary components; SEAL combines rejection-token learning with decoding regularization.
- Defined the CAD contrast parameter and distinguished contextual adherence from context truth.
- Retained TofuEval's reported 1,479 summaries with its arithmetic inconsistency disclosed; qualified HALoGEN's all-domain count and FaithBench's disagreement-selected sample.
- Preserved uncertainty about reading depth: all selected titles/abstracts were screened, but only targeted full-text checks support detailed claims. The evidence CSVs provide claim-specific locators.
- Proposed controls and future experiments are explicitly unperformed. No heterogeneous paper scores were pooled into a leaderboard.

## Citation checks

Actual final BibTeX contains **88 entries: 86 research studies + 2 design sources**. All 55 unique research studies cited inside the imported figures resolve to the final bibliography with **zero author–year label mismatches**. Fig. 2 has 55 unique studies; Fig. 3 has nine; the final Fig. 4 has twelve. The same study may appear in multiple figures for a different role.

The six suffix groups remain: Chuang 2024a/b, Dziri 2022a/b, Zhang 2023a/b, Zhang 2024a/b, Huang 2025a/b, and Liu 2024a/b/c (the added Lost in the Middle entry is 2024c, leaving the two figure labels unchanged). They come from the unmodified ACL BST, not manually edited years. The discovery library retains ITI as a screened study, but the manuscript uses other representative internal-intervention methods; this avoids changing the HaluEval label already printed in the author-supplied figures. No `nocite{*}` is used. Explicit `nocite` only registers genuine citations inside imported PDFs.

## Build and visual review

Compiled with pdfTeX/BibTeX (TeX Live 2026) through `latexmk`, with no unresolved citations/references, no BibTeX warnings, and no overfull boxes. The seven-page main-paper boundary and reference start on page 8 are checked from both the AUX and PDF. All main pages, bibliography pages, and appendix pages were rendered and reviewed for clipping, overlap, figure placement, table readability, and unwanted blank pages. Figure 2 remains dense and retains the user's original line wrapping; it is displayed at the full available ACL width and can be zoomed as a vector PDF.

`manuscript/validation.json` records the machine checks and final PDF digest. The Overleaf archive contains the complete multipart source and authoritative PDF figures. Historical preparation notes remain explicitly marked as such.
