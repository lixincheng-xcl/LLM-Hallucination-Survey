# Final manuscript validation — 4 October 2026

## Delivered scope

The completed English survey is **Hallucination in Large Language Models: A Survey of Detection, Evaluation, and Mitigation**, by Xincheng Li, School of Computer Science, University of Auckland (xli798@aucklanduni.ac.nz). It uses the supplied ACL style without margin or font changes. The PDF has **18 pages: 7 main pages, 6 reference pages, and 5 appendix pages**. It reports no new experiments and does not claim exhaustive systematic coverage.

## Figures and narrative closure

The author's four revised PDFs remain byte-for-byte unchanged. Figure 1 is proportionally scaled to the right column of page 1; Figures 2–4 retain full two-column width. Hashes are in `manuscript/figures/manifest.json`.

| Component | PDF page | Role and connection |
|---|---:|---|
| Fig. 1 | 1 | Synthetic unsupported/contradicted source examples; the caption distinguishes unsupported from world-false. |
| Fig. 2 | 2 | Section navigation; all printed section numbers match the final paper. |
| Fig. 3 | 3 | Evaluation target taxonomy, instantiated by Table 1. |
| Table 1 | 5 | Nine benchmark corpora with task-specific metrics and count caveats. |
| Fig. 4 | 6 | Potential failures and interventions, linked in the analysis to Fig. 3 and Table 1 for independent evaluation. |

The final PDFs do not include the former Figure 4 feedback arrow. The paper describes an evaluation loop *linking* the figures and table, rather than falsely claiming that arrow is still present. Earlier draw.io and SVG assets are preserved as design-stage working files, not substituted for the user-edited artwork.

## Revision and writing-guide use

The repository link appears only in the abstract’s final sentence. Page 7 now contains substantive discussion and the complete conclusion, with both columns extending to the normal lower text area; references start on page 8. The conclusion explicitly answers RQ1–RQ3. Added synthesis connects detector access to benchmark compatibility, separates offline and online costs, and proposes joint detector–intervention validation with independent auditing and matched coverage. These additions strengthen the chain from definitions through methods and evaluation to mitigation and future work.

The supplied Chinese writing guide informed the common comparison dimensions, methods-to-metrics links, evidence-derived future questions, and explicit research-question closure. Its catastrophic-forgetting examples and topic-specific taxonomy were not imported into this hallucination survey. No guide instruction superseded the requested ACL format or seven-page limit.

## Final editorial and technical revision

The abstract was rewritten after directly reading the abstracts of the supplied logical-reasoning and LVLM-hallucination surveys. It follows their problem, scope, ordered synthesis, and future-directions structure using original wording and this paper's actual scope. It now introduces concepts, detection, evaluation, mitigation, and open questions in manuscript order, with the repository sentence last. The latest abstract follows the supplied example's narrative progression without publication years or literature counts; the Chinese Word abstract has been updated to match. Main and supplementary captions use concise descriptive titles, followed only by necessary explanations of colors, abbreviations, counting units, or interpretation. Figure 1 retains the distinction between unsupported and false content; Table 1 now defines P and R as well as Dis, Gen, and MC.

The final language pass expands LLM, CAD, CoVe, NLI, and SFT at their first relevant uses and removes repetitive navigation or scope statements. The RQ3 conclusion now recognizes independently verified reliability gains assessed with informative coverage and cost; it does not require an increase in supported-claim count, since correcting errors while retaining supported content can also be useful. The four supplied figure files, bibliography entries, and ACL style files remain unchanged. Float declarations were positioned to preserve Figures 2 and 3 on pages 2 and 3 without resizing the artwork or changing typography.

The author block now gives the School of Computer Science and the requested university email. Main captions contain scientific descriptions; visual-design credit is consolidated in Appendix A with both sources still cited. A dedicated Limitations section follows the conclusion within page 7. Appendix prose uses two columns with full-width table floats. The requested Figure 1 enlargement has been removed; Figure 1 remains in the right column of page 1.

The introduction now identifies the comparison contributed by this survey. The Methods discussion contrasts feedback sources, defines all CAD symbols, and points to the common access/resource matrix. The evaluation section explains VeriScore’s F1@K and why its supported-claim target differs from task-aspect coverage. The joint-validation analysis uses the conditional-probability identity for erroneous releases, with variables and its positive-error condition defined. This is a mathematical deduction and a proposed protocol, not a reported experiment. Appendix A adds coding rules for hybrid methods and distinguishes target, proxy, and verifier access.

## Technical and source checks

- Reviewed source support versus world correctness, the three detection families, generation versus detector evaluation, and hybrid mitigation classification.
- Verified VeriScore’s F1@K formula and domain-specific median K in the primary method, and TruthfulQA’s original MC true-answer likelihood mass; the evidence ledger records exact source sections and pages.
- Rechecked the FOCUS primary method: its accessible proxy provides token probabilities and attention for historical uncertainty propagation; the target generator can remain black-box. Updated the public evidence ledger and method matrix consistently.
- Confirmed Lookback Lens requires supervised labels; FactAlign uses fKTO; RHIO spans training and decoding; TruthX learns auxiliary components; SEAL combines rejection-token learning with decoding regularization.
- Defined the CAD contrast parameter and distinguished contextual adherence from context truth.
- Retained TofuEval's reported 1,479 summaries with its arithmetic inconsistency disclosed; qualified HALoGEN's all-domain count and FaithBench's disagreement-selected sample.
- Preserved uncertainty about reading depth: all selected titles/abstracts were screened, but only targeted full-text checks support detailed claims. The evidence CSVs provide claim-specific locators.
- Proposed controls and future experiments are explicitly unperformed. No heterogeneous paper scores were pooled into a leaderboard.

## Citation checks

Actual final BibTeX contains **88 entries: 86 research studies + 2 design sources**. All 55 unique research studies cited inside the imported figures resolve to the final bibliography with **zero author–year label mismatches**. Fig. 2 has 55 unique studies; Fig. 3 has nine; the final Fig. 4 has twelve. The same study may appear in multiple figures for a different role.

The six suffix groups remain: Chuang 2024a/b, Dziri 2022a/b, Zhang 2023a/b, Zhang 2024a/b, Huang 2025a/b, and Liu 2024a/b/c (the added Lost in the Middle entry is 2024c, leaving the two figure labels unchanged). They come from the unmodified ACL BST, not manually edited years. The discovery library retains ITI as a screened study, but the manuscript uses other representative internal-intervention methods; this avoids changing the HaluEval label already printed in the author-supplied figures. No `nocite{*}` is used. Explicit `nocite` only registers genuine citations inside imported PDFs.

## Build and visual review

Compiled with pdfTeX/BibTeX (TeX Live 2026) through `latexmk`, with no unresolved citations/references, no BibTeX warnings, and no overfull boxes. The seven-page main-paper boundary and reference start on page 8 are checked from both the AUX and PDF. Figure 1’s actual PDF transform confirms equal horizontal/vertical scaling, approximately 218.3 pt width, and placement in the right column. The main source contains the repository URL exactly once, at the end of the abstract. All main pages, bibliography pages, and appendix pages were rendered and reviewed for clipping, overlap, figure placement, table readability, and unwanted blank pages. Figure 2 remains dense and retains the user's original line wrapping; it is displayed at the full available ACL width and can be zoomed as a vector PDF.

`manuscript/validation.json` records the machine checks and final PDF digest. The Overleaf archive contains the complete multipart source and authoritative PDF figures. Its 22 files were byte-compared with the source, extracted to a separate directory, and independently compiled: the result has 18 pages and identical page-by-page text to the delivered PDF. Historical preparation notes remain explicitly marked as such.
