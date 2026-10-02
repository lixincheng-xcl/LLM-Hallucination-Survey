from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[1]
papers=json.loads((R/'data/papers.json').read_text());by={r['short_name']:r for r in papers}
def link(name):
 p=by[name];return '['+name+']('+p['url']+') ('+p['venue']+')'
def table(file,title,intro,headers,lines):
 rows=[r.split('|') for r in lines.strip().splitlines()]
 text='# '+title+'\n\n'+intro+'\n\n'+'| '+' | '.join(headers)+' |\n'+'| '+' | '.join(['---']*len(headers))+' |\n'
 for r in rows:text+='| '+link(r[0])+' | '+' | '.join(r[1:])+' |\n'
 (R/'docs'/file).write_text(text)
 with (R/'data'/file.replace('.md','.csv')).open('w',newline='') as f:
  w=csv.writer(f);w.writerow(headers+['source_url'])
  for r in rows:w.writerow(r+[by[r[0]]['url']])
table('benchmark_matrix.md','Benchmark and evaluation matrix',
'''Preparation table, not a pooled leaderboard. The task, reference frame, annotation unit and source provenance must be aligned before comparing scores. Counts, when provided, refer to the source paper's stated dataset scope, not necessarily one evaluation split. A benchmark and a metric are different objects: FActScore/VeriScore are primarily metrics and appear in the method table.''',
['Benchmark / source','Task and reference','Data / annotation','Evaluation focus','Comparison caveat'],'''
TruthfulQA|Closed-book QA; world truth|817 misconception-oriented questions|Truthfulness and informativeness; multiple-choice setting also available|Question selection is adversarial, not a sample of all user requests
TRUE|Multiple grounded generation tasks; source support|11 standardized existing datasets with human consistency labels|Example-level meta-evaluation of consistency metrics|Task and error prevalence differ across component datasets
BEGIN|Knowledge-grounded dialogue; source support|12k dialogue turns; human attribution judgments|Can a metric distinguish attributable responses?|Paraphrase and source length can create shortcuts
HaluEval|QA, dialogue, summarization and general prompts; mixed reference conditions|35k total samples, including generated and human-annotated portions|Hallucination recognition accuracy|Prompt-induced and naturally occurring errors are different distributions
ALCE|Long-form QA with citations|ASQA, QAMPARI and ELI5-based settings|Fluency, answer correctness, citation correctness and completeness|A citation's presence does not establish that it supports the claim
ANAH|Bilingual generative QA; retrieved references|About 12k sentence annotations for about 4.3k responses|Sentence-level type, evidence fragment and correction|Retrieval completeness and annotation policy affect labels
RAGTruth|QA, summarization and data-to-text under RAG|Nearly 18k naturally generated responses; human response/span labels|Response-level and span-level precision, recall and F1|Same sources, generators, split and span matching are needed for comparison
ExpertQA|Expert-curated long-form QA; attribution and world factuality|2,177 questions across 32 fields; expert verification|Claim correctness and attributable support|Expert cost and domain coverage differ from general-purpose evaluation
TofuEval|Topic-focused dialogue summarization|Human sentence labels, error explanations and taxonomy|Sentence factual consistency and evaluator reliability|News-summary results do not automatically transfer to dialogue
HALoGEN|Nine-domain generation; domain-specific sources|10,923 prompts with high-precision automatic verifiers|Atomic hallucinations and proposed error-source categories|Verifier coverage is domain-dependent; high precision is not exhaustive recall
HalluLens|Intrinsic/extrinsic tasks under the paper's own definitions|Dynamic generation of three extrinsic task sets|Factual generation, refusal, recall and precision trade-offs|Its training-data reference frame differs from source-faithfulness terminology
FactBench|In-the-wild user-style generation; Web evidence|1k prompts across 150 topics, split by difficulty|Supported / unsupported / undecidable units; refusal behavior|Web changes and query coverage can change verification outcomes
FaithBench|Summaries from 10 modern LLMs across 8 families|Expert annotations on detector-disagreement cases|Balanced accuracy and macro F1 for detection|Difficulty-enriched sampling is not a deployment prevalence estimate
RGB|RAG question answering in English and Chinese|Four controlled testbeds|Noise robustness, negative rejection, integration and counterfactual robustness|Robustness dimensions should be reported separately
TRIVIA+|Long-context RAG hallucination detection|Human labels plus controlled sample-dependent noisy-label variants|Detector evaluation under long context and label noise|Distinguish clean-test performance, noisy supervision and benchmark ceiling
''')
table('method_matrix.md','Technical comparison of representative methods',
'''Qualitative mechanism comparison. “Access” describes required signals, not a standardized API or measured latency. Cost drivers and failure questions are curator analysis, not new experiments. A method can appear on several taxonomy axes. No cross-paper numerical ranking is implied.''',
['Method / source','Mechanism','Access and supervision','Main cost driver','Limit / comparison question'],'''
QAFactEval|Generate questions and compare source-supported answers|Source and output text; pretrained QA components|Question generation and answering|QA errors can become evaluator errors
AlignScore|Unified alignment model over text pairs|Source/output text; trained verifier, generator can remain black box|Chunk alignment and verifier calls|Generalization across task, length and error type
FActScore|Decompose, retrieve and verify atomic facts|Generated text, knowledge corpus and verifier|Claim count, retrieval and verification calls|Precision alone omits completeness; decomposition can inflate counts
VeriScore|Extract and verify only verifiable claims|Generated text and external evidence; verifier model|Claim extraction and search|Keep unverifiable, unsupported and false distinct
SelfCheckGPT|Consistency across repeated generations|Sampling access; no external knowledge corpus required|Repeated generation and pairwise checking|A consistently repeated falsehood may evade detection
Semantic uncertainty|Entropy over semantic equivalence classes|Multiple generations; likelihoods for weighted semantic entropy|Sampling and semantic equivalence checks|Meaning clusters and sample budget affect the estimate
Semantic entropy|Detect confabulations through meaning-level uncertainty|Sampled generations; estimator variant determines probability access|Sampling and clustering|Designed for confabulations, not all stable false beliefs
FOCUS|Focused token-level uncertainty aggregation|Token probability signals; no external evidence required|Generation probabilities and token weighting|Uncertainty is not identical to factual error
Internal-state probe|Supervised truth classifier over hidden states|Internal activations and labeled training examples|Feature collection and probe training|Artificial true/false pairs may not transfer to generated errors
Lookback Lens|Context-versus-generation attention ratios|Attention maps and detector supervision|Attention extraction and optional guided decoding|Correlation with support does not establish source truth
PrefixNLI|Entailment checks on incomplete prefixes|Source/prefix text and a specially trained verifier|Frequent prefix evaluation|Early detection quality versus latency
Self-RAG|Learned retrieval and reflection tokens|Generator training, retrieval system and reflection supervision|Training plus conditional retrieval and candidate ranking|Reflection quality and evidence availability limit reliability
CAD|Contrast context-conditioned and unconditioned token distributions|Generator logits under both conditions; no new training|Additional decoding distribution|Strong context adherence can reproduce wrong context
DoLa|Contrast mature and earlier-layer logits|Internal layer outputs; no new model training|Layer projections and contrastive decoding|Layer selection and task transfer require checking
TruthX|Edit truth-related latent representations|Internal representations; learned encoder and direction|Representation learning and inference intervention|Truthfulness steering may affect other output qualities
Self-Alignment|Self-evaluation and knowledge tuning followed by DPO|Trainable generator; self-generated factuality supervision|Response generation, evaluation and preference training|Correlated self-label errors
FactAlign|Fine-grained factuality-based long-form alignment|Trainable model and sentence-level feedback|Verification for training and alignment updates|Reward quality, factual precision and useful coverage
Astute RAG|Source-aware consolidation of internal and retrieved knowledge|Text generation and retrieval access|Iterative knowledge consolidation|Evidence reliability must be assessed, not assumed
CoVe|Draft, independently verify, then revise|Text-generation access; no external source required by core procedure|Multiple verification generations|Shared parametric misconceptions can persist
CRITIC|External-tool feedback followed by revision|Black-box generator and task-appropriate tools|Search/tool calls and iterative regeneration|An unreliable tool can provide misleading correction signals
SEAL|Selective rejection token learning and decoding regularization|Trainable generator and rejection-aware objective|Training and refusal calibration|Measure coverage and over-refusal, not just error reduction
''')
print('Created benchmark matrix (15 rows) and method matrix (21 rows)')
