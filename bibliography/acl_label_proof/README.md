# ACL citation label proof

Generated with the user's supplied `acl_natbib.bst` and the installed BibTeX 0.99e (TeX Live 2026). The `.aux` now registers the final manuscript citation set: 86 research studies and two design sources. `citation_labels.bbl` is real BibTeX output for these 88 entries. All 55 research studies printed inside the final user-supplied figures keep their labels unchanged.

| Citation family | a | b |
|---|---|---|
| Chuang et al., 2024 | Lookback Lens | DoLa |
| Dziri et al., 2022 | FaithDial | BEGIN |
| Zhang et al., 2023 | SAC3 | FOCUS |
| Zhang et al., 2024 | TruthX | Self-Alignment |
| Huang et al., 2025 | SEAL | RHIO |
| Liu et al., 2024 | LVLM hallucination survey (design source) | Truthfulness hyperplane |

The final bibliography also assigns **Liu et al., 2024c** to *Lost in the Middle*; the a/b labels already printed in the figures do not change.

The `.bib` year fields remain the original numeric years. The ACL style generates the suffixes; figures consume the same labels through `data/acl_citation_labels.json`.

Reproduce from the repository root:

```sh
python3 scripts/sync_acl_citation_labels.py --aux manuscript/build/main.aux
python3 scripts/build_reference_style_assets.py --only figure_2_survey_structure figure_3_evaluation_taxonomy figure_4_causes_mitigation
python3 scripts/write_figure_integration.py
python3 scripts/build_drawio_sources.py
```

Open the staged native diagrams in draw.io, check them and save to `figures/drawio`, then export the PNG previews. The generator never overwrites UI-edited native deliverables automatically. Preserve any later manual edits before rebuilding.

When manuscript citations change, first run `python3 scripts/sync_acl_citation_labels.py --aux /absolute/path/to/manuscript.aux`, then rebuild/recheck the diagrams. Adding a study can change suffix assignments; the eventual manuscript `.bbl` must remain the authority. Use the supplied ACL BST for that build. The completed paper and validation record are in `manuscript/`. Artwork rebuild commands above apply to historical working assets, not the author-supplied final PDFs.
