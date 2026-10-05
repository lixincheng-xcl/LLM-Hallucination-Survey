# Comparative evidence audit protocol

Protocol recorded: 5 October 2026, before the new coding round.

## Question and sampling frame

What must be held comparable before evidence of hallucination detection or mitigation can support a claim of more reliable useful generation?

The audit is a purposive, bounded documentary analysis, not a systematic search of the whole field, a meta-analysis, or a model benchmark. Its sampling frame is all thirteen named studies in the resource/access table of the frozen coursework release ca6e155 (Appendix Table 8). This table spans source alignment, atomic verification, sampling, uncertainty, internal detection, training, retrieval, decoding, editing, revision, and abstention. Membership is fixed before coding reporting properties. All thirteen are retained regardless of findings. Other bibliography entries provide context and are not included in the audit denominator.

Studies: AlignScore; FActScore; SelfCheckGPT; Semantic entropy (Farquhar et al., 2024); Lookback Lens; FactAlign; Self-RAG; CAD; DoLa; TruthX; CoVe; CRITIC; SEAL.

The selected set represents mechanism diversity, not the prevalence of practices in the literature. It favors English text tasks and the original representative-method choices. No field-wide percentage can be inferred from these cases. A subsequent systematic review would require a separately defined search population and screening workflow.

## Reading and extraction

Retrieve primary full texts (formal proceedings preferred); retain exact URLs, versions, retrieval date, PDF digests, and section/table/page locators. Inspect the method, main experimental protocol/results, and relevant appendix material for the fields below. Abstract-only evidence cannot support a definitive experimental-protocol code. Record inaccessible or unresolved fields instead of imputing them. Numerical findings remain within their original study and protocol; do not pool heterogeneous performance scores.

Each row must include study, citekey, role, source_url, pdf_url, source_sha256, inspected_sections, reference_frame, scoring_unit, evidence_and_access, information_control, information_locator, evaluation_separation, evaluation_locator, resource_reporting, resource_locator, joint_validation, joint_locator, caveat, and verified_on.

## Coding rules

- reference_frame: world-factuality, source-faithfulness, task-correctness proxy, or mixed. Code the actual study target; do not equate source support with universal truth.
- scoring_unit: response, sentence, claim, span/token, or mixed. Describe task-dependent aggregation.
- information_control: list concrete reported safeguards such as answered-question coverage, fact quantity, required-aspect coverage, informativeness, task-quality proxy, or unresolved. A count of generated facts does not establish completeness; a task-quality metric is not a matched-coverage control.
- evaluation_separation: describe human auditing, a distinct evaluator, reuse of a scorer, or unresolved components. A different prompt or model is not a guarantee of statistically independent errors. No binary independent/not-independent score is assigned from model names alone.
- resource_reporting: qualitative access requirements, call/token count, measured latency, training compute, or unresolved. Report tested scope; no universal cost ranking.
- joint_validation: explicit joint generator/intervention/detector test, related component analysis, not located in inspected sections, or not applicable. Not located is a bounded search result, not proof that the study is defective or omits it everywhere.
- Every nontrivial description requires a precise locator and a paraphrase explaining the supporting evidence. Short verbatim excerpts may be kept in source notes, respecting quotation limits when web excerpts are used.

## Verification and limits

Coding is AI-assisted and is checked against the primary text. It is not independent human double annotation; agreement statistics must not be reported. A second agent may check disputed extractions but does not constitute a human replication. Preserve revisions and unresolved entries. Final author verification of the coding and its interpretation remains necessary before submission.

The principal outputs are explicit compatibility conditions and traceable case comparisons. Descriptive counts may be generated only from coded observations with a declared denominator and cannot be interpreted as publication-quality prevalence estimates. Proposed prospective experiments remain labeled unperformed.
