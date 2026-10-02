# Search and screening protocol

Snapshot: 1 October 2026. Preparation completed: 2 October 2026.

This is a bounded, targeted literature survey preparation, **not an exhaustive systematic review**. Its target size is approximately the 87 reference entries in the supplied logical-reasoning survey. The 87 included studies are a candidate citation library, not a requirement to cite every item in the eventual paper.

## Sources and discovery

1. Download official ACL Anthology XML collections for ACL, EMNLP, NAACL, EACL, Findings and TACL, years 2022–2026. Twenty-five collections were available. Five requested year/venue combinations returned 404; these failures are recorded, not counted as searched collections with zero papers.
2. Title matching used the case-insensitive expression recorded in `scripts/fetch_acl.py`: hallucination, factuality, faithfulness, truthfulness, attribution, knowledge conflict, self-checking, retrieval augmentation, uncertainty, abstention and related spellings. This deliberately broad pass yielded 1,766 candidates, including false positives such as counterfactual data augmentation and feature attribution.
3. Add three targeted Anthology papers missed by the title filter: ALCE, the internal-state probe, and Lost in the Middle. Add seven mechanism-defining studies verified against ICLR/NeurIPS/AAAI/Nature records and author-deposited papers. Total candidate records: **1,776**.
4. Select representative studies for mechanism coverage, benchmark diversity, evaluation criticism and temporal development. Read titles and abstracts for the 87 included items. Inspect selected full-text passages for 15 downloaded representative papers. No external citation-count threshold was used.

Raw XML exports and downloaded PDFs remain in the local preparation directory, outside this public repository. `data/source_manifest.json` records the source filenames, sizes and SHA-256 digests. `data/retrieval_log.json` records attempted source URLs and outcomes. Official BibTeX was fetched for all 80 included Anthology records. Seven external BibTeX entries were formed from verified publication metadata; DOI fields absent from a verified conference source were left absent.

## Inclusion rules

- Published in 2022–2026, with a verifiable primary record; prefer main conferences, Findings and established journals.
- Direct relevance to factuality or source faithfulness of generated text, detection, mitigation, evaluation or a necessary methodological criticism.
- Cover distinct mechanisms or provide evidence that challenges a common conclusion.
- A small number of boundary studies are explicitly tagged as contextual support: long-context utilization, an existing factuality survey, and reasoning-related refusal behavior.

## Exclusion, reserve and deduplication

401 records were excluded by **automatic title triage**, principally because the keyword match concerns another task or modality. These are not represented as 401 individually full-text-assessed exclusions. Another **1,288 records remain reserve**, not individually abstract-screened; omission from a seven-page survey is not a finding of low quality. The full status/reason/stage log is available in `data/screening_log.csv`.

The 87 selected records were checked for matching DOI or exact normalized title; no exact duplicates were found. Canonical published versions were preferred over separate preprint records. This check does not establish that all reserve records are free of near-duplicates. `data/duplicates.csv` records the implemented check and currently contains only its header.

## Reading and inference boundaries

`screening_level` and `fulltext_status` distinguish abstract screening from limited full-text inspection. The `include_reason` is the curator's summary; `review_question` is a proposed critical question, **not a claim that the cited paper failed that test**. Source abstracts and published scores are not treated as independently replicated findings. Numerical rankings across different prompts, model versions, source corpora, label definitions or metrics are not pooled.

The scope is mostly English-language, text-based research, and the sampling strongly favors ACL-family venues. It does not claim comprehensive multilingual, medical, legal, agentic or multimodal coverage. New 2026 entries were checked against existing formal proceedings, not inferred from submission titles. Metadata snapshotting does not prove reproducibility or successful code execution.

OpenReview API/PDF access returned 403 during local batch retrieval. Metadata was instead verified using accessible official proceedings, publisher pages, author arXiv records and the web-indexed conference PDF. Full-text download is not claimed for those blocked files.

## Workflow adaptation and handoff

The Academic Search and SCI literature-screening skills supplied provenance, conservative deduplication, inclusion reasons and hierarchical Zotero preparation. The user's explicit 7-page course scope overrides the full SCI workflow's generic top-500 target. No institution login, citation-count gate or extra topic-approval round was introduced.

`bibliography/references.ris` is an importable flat set. `bibliography/zotero/` and `zotero_collections.csv` map the two-level categories. RIS keywords do **not** guarantee automatic creation of nested Zotero collections. Zotero has not been operated in this round. The manuscript was subsequently completed with targeted primary-source checks. See `data/manuscript_detection_evidence.csv`, `data/manuscript_mitigation_evidence.csv`, and `docs/manuscript_validation.md`; the original screening-depth fields remain a record of the initial snapshot.
