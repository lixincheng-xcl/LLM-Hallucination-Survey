"""Write ACL float fragments and provenance; no standalone manuscript or prose."""
from pathlib import Path
import json,csv,re
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'figures/reference_style'
P={a['id']:a for a in json.loads((ROOT/'data/papers.json').read_text())}
bench=list(csv.DictReader((OUT/'benchmark_table.csv').open()))
assets=json.loads((OUT/'asset_manifest.json').read_text())
citation_map=json.loads((OUT/'figure_citation_map.json').read_text())
height_mm=sum(a['height']/a['width']*160 for a in assets)
def esc(t):
 for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('~',r'\(\sim\)')]:t=t.replace(a,b)
 return t
tex=[r'% ACL table fragment. Requires booktabs, tabularx, array and natbib (ACL supplies natbib).',r'% Load bibliography/references.bib and bibliography/design_sources.bib in the eventual manuscript.',r'\begin{table*}[t]',r'\centering',r'\small',r'\setlength{\tabcolsep}{3pt}',r'\renewcommand{\arraystretch}{1.13}',r'\caption{Hallucination evaluation benchmarks for text LLMs. Dis: hallucination discrimination; Gen: generated-content evaluation; MC: multiple choice. Sizes refer to different corpus units. The three-rule design follows \citet{liu-etal-2024-lvlm-design}; benchmark contents are independently compiled.}',r'\label{tab:hallucination-benchmarks}',r'\begin{tabularx}{\textwidth}{@{}>{\centering\arraybackslash}p{.245\textwidth}>{\centering\arraybackslash}p{.095\textwidth}>{\centering\arraybackslash}p{.15\textwidth}>{\centering\arraybackslash}p{.205\textwidth}>{\centering\arraybackslash}X@{}}',r'\toprule',r'Benchmark & Evaluation & Size & Hallucination focus & Metrics \\',r'\midrule']
for a in bench:
 vals=[esc(a['benchmark'])+r' [\citealp{'+P[a['paper_id']]['citekey']+'}]']+[esc(a[k]) for k in ['evaluation','size','hallucination_focus','metrics']]
 tex.append(' & '.join(vals)+r' \\')
tex +=[r'\bottomrule',r'\end{tabularx}',r'\par\vspace{2pt}\begin{minipage}{\textwidth}\footnotesize',r'* Retained count reported in the paper. HALoGEN counts the complete nine-domain suite; only text-relevant tasks are in this survey. Dataset and metric details, including counting caveats, are retained in the companion evidence ledger.',r'\end{minipage}',r'\end{table*}']
(OUT/'table_1_benchmarks.tex').write_text('\n'.join(tex)+'\n')
base='figures/reference_style/'
floats=[r'% Float fragments only. Insert individually at the appropriate locations.',r'% Requires graphicx and the ACL natbib bibliography. No manuscript prose is included.',r'% The PDF assets omit embedded captions so the ACL template controls numbering and font size.']
figures=[
 ('figure_1_hallucination_examples','hallucination-examples','Section 1: motivation; revisit in Section 2','liu-etal-2024-lvlm-design'),
 ('figure_2_survey_structure','survey-structure','Section 1: closing roadmap, after Figure 1','liu-etal-2025-logical-design'),
 ('figure_3_evaluation_taxonomy','evaluation-taxonomy','Section 4: evaluation targets; followed by Table 1','liu-etal-2024-lvlm-design'),
 ('figure_4_causes_mitigation','causes-mitigation','Section 5: mitigation overview; refer back to Section 4','liu-etal-2024-lvlm-design')]
for name,label,placement,design in figures:
 caption=re.sub(r'^Figure \d+: ', '', next(a['caption'] for a in assets if a['name']==name))
 for number,ref in [(1,'hallucination-examples'),(2,'survey-structure'),(3,'evaluation-taxonomy'),(4,'causes-mitigation')]:
  caption=caption.replace(f'Fig. {number}',r'Figure~\ref{fig:'+ref+'}')
 caption=caption.replace('Table 1',r'Table~\ref{tab:hallucination-benchmarks}')
 caption+=r' Layout adapted from \citet{'+design+'}.'
 keys=list(dict.fromkeys(a['citekey'] for a in citation_map.get(name,[])))
 floats+=['% First mention: '+placement]
 if keys:
  floats+=['% These studies are visibly cited inside the vector artwork; register them with BibTeX.',r'\nocite{'+','.join(keys)+'}']
 floats +=[r'\begin{figure*}[t]',r'\centering',r'\includegraphics[width=\textwidth]{'+base+name+'.pdf}',r'\caption{'+caption+'}',r'\label{fig:'+label+'}',r'\end{figure*}','']
(OUT/'figure_includes.tex').write_text('\n'.join(floats))
# Keep design references separate from the 87 content studies.
(ROOT/'bibliography/design_sources.bib').write_text('''@article{liu-etal-2024-lvlm-design,
  title = {A Survey on Hallucination in Large Vision-Language Models},
  author = {Liu, Hanchao and Xue, Wenyuan and Chen, Yifei and Chen, Dapeng and Zhao, Xiutian and Wang, Ke and Hou, Liping and Li, Rongjun and Peng, Wei},
  year = {2024},
  journal = {arXiv preprint arXiv:2402.00253},
  url = {https://arxiv.org/abs/2402.00253v2},
  note = {Design reference; supplied version v2}
}

@article{liu-etal-2025-logical-design,
  title = {Logical Reasoning in Large Language Models: A Survey},
  author = {Liu, Hanmeng and Fu, Zhizhang and Ding, Mengru and Ning, Ruoxi and Zhang, Chaoli and Liu, Xiaozhang and Zhang, Yue},
  year = {2025},
  journal = {arXiv preprint arXiv:2502.09100},
  url = {https://arxiv.org/abs/2502.09100v1},
  note = {Design reference; supplied version v1}
}
''')
lines=['# 图表对应、来源与使用说明','','更新：2026-10-02。本轮仅制作图、表、图注、LaTeX 插入片段和证据记录，没有撰写摘要或正文。新版位于 `figures/reference_style/`；上一轮的三张概念图保留供追溯。','','## 逐项对应','','| 用户参考 | 本论文交付 | 保留的设计元素 | 内容调整 |','|---|---|---|---|',
'| LVLM Figure 1 | Figure 1 幻觉示例 | 上下虚线框、黄/灰对话气泡、人和机器人头像、绿/粉/蓝标注 | 原创图书馆文本示例；文本证据卡取代照片；分类与证据逐项对应 |',
'| Logical Reasoning Figure 1 | Figure 2 综述结构 | 竖排根节点、正交树、紫色圆角边框、绿色文献叶节点、作者年份引用 | 改为本文 §2–§6；每个子节列 4–5 篇代表作，机制与指标留给 Fig.3–4 |',
'| LVLM Figure 2 | Figure 3 评估 taxonomy | 深蓝圆角树、白色中间节点、浅色文献节点 | 区分生成文本的打分与检测器的基准评估 |',
'| LVLM Figure 3 | Figure 4 成因与缓解 | 绿/红/蓝/黄/灰五列、流程/原因/缓解三层、虚线分隔 | 文本数据、可选检索、LLM、解码、输出；不包含视觉编码器 |',
'| LVLM Table 1 | Table 1 基准 | 表题在上、Times 字体、五列居中、三条横线、无竖线 | 9 个文本相关基准，实际规模单位、幻觉关注点与指标 |',
'','## 设计归属','','版式是按用户要求对给定参考图进行的重绘和改编，不能称为完全独立的视觉设计。文字、节点、文本例子与表内数据均针对本论文重新编制；没有复用参考图中的照片或截图。人物与机器人图标由矢量基本形状绘制。',
'','- Hanmeng Liu et al. (2025), [Logical Reasoning in Large Language Models: A Survey](https://arxiv.org/abs/2502.09100v1), Figure 1。',
'- Hanchao Liu et al. (2024), [A Survey on Hallucination in Large Vision-Language Models](https://arxiv.org/abs/2402.00253v2), Figures 1–3 and Table 1。',
'','两篇设计来源单独存于 `bibliography/design_sources.bib`，不混入已筛选的 87 篇内容文献计数。LaTeX 图注已经加入 design/layout adapted from 引用。',
'','## 内容与证据边界','','- Figure 1 是作者构造的来源忠实性示例，不是模型实测输出。绿色表示来源未支持，不自动意味着世界事实为假；粉色/蓝色显示数值与关系矛盾，不代替完整 taxonomy。下方来源明确 sorting Tuesday、cataloguing Wednesday，蓝色输出仅颠倒顺序。',
'- Figure 2 的章节号以当前提纲为准：§3 检测、§4 评估、§5 缓解、§6 分析；§1 引言与 §7 结论不展开为分类枝。',
'- Figure 3 按评价对象分枝，生成内容与检测器可以使用同一批已标注输出。每个基准名称后直接标出作者年份；枝末指标属于评价维度概括，各基准具体协议依 Table 1 和证据表，不能将同枝全部指标分配给每个基准。FActScore/VeriScore 是评估方法，未作为数据集行。',
'- Figure 4 是文献归纳的潜在失败来源与干预位置对应，不是经实验识别的因果图。灰色输出列不列作原因。检索对闭卷生成不是必需模块。',
'- 图内标签已由用户提供的 `acl_natbib.bst` 和真实 BibTeX 输出统一，当前 57 项引用（55 篇内容研究 + 2 篇设计来源）包含六组 a/b 消歧；`figure_citation_map.json` 保留逐图的显示文本、唯一论文 ID、BibTeX key 和来源 URL。',
'- `figure_includes.tex` 为图中实际出现的论文加入显式 `\\nocite{具体键}`，因为矢量图片中的作者年份不会被 BibTeX 自动识别。这只登记图内已经引用的研究，不使用 `\\nocite{*}` 填充文献。',
'','## Table 1 核验记录','','表中数字以对应论文版本为准。Dis/Gen/MC 是本表的导航标签，不声称原论文采用同一协议。表内规模跨单位，不能直接相加或据此排序。','','| 基准 | 规模 | 原文定位 | 口径说明 |','|---|---|---|---|']
for a in bench:
 lines.append(f"| [{a['benchmark']}]({P[a['paper_id']]['url']}) | {a['size']} | {a['source_locator']} | {a['counting_notes']} |")
lines +=['','TofuEval 原文 §3.3 的“1,500、移除 23、保留 1,479”存在算术不一致。本表按其明确报告的保留规模 1,479 标注星号，未擅自改为推算数字。最终使用时可进一步核对作者仓库版本。',
'','## 逻辑与重复检查','','本轮已经将结构导航、评价分类、机制对应和数据目录分开；逐项检查、首次引用顺序与后续正文约束见 [图表与全文逻辑闭环](图表与全文逻辑闭环.md)。ANAH 中生成式/判别式标注器都用于判断幻觉标签，统一标为 Dis。FaithBench 的 Gen 只指已标注摘要的内容质量分析，不把经过争议样本筛选的集合当成总体幻觉发生率样本。',
'','## 文件与排版','','- `Figures_and_Table_Review.pdf`：按 Fig.1 示例、Fig.2 结构、Fig.3 评估、Fig.4 缓解、Table 1 排列，共 5 页带图注审阅稿；不是五页或七页论文。',
'- 4 张图与 1 张表各提供：可编辑 SVG、160 mm 宽矢量 PDF、带图注 PNG 预览。单项 PDF/SVG 无重复图注，由 ACL 控制正式编号与字号。',
'- `figure_includes.tex` 与 `table_1_benchmarks.tex`：LaTeX 片段，尚未与完整 ACL 工程一起编译；没有建立正文文稿。表格应优先使用原生 LaTeX，而不是截图。',
'- `benchmark_table.csv`：可维护的表数据及证据定位；`figure_references.json`：图中方法来源。',
'- 密集结构图和表格必须跨双栏放置。160 mm 下结构图的最小框内标签约 7.1 pt。审阅 PDF 可放大检查，最终 ACL 排版时应优先扩大节点、简化叶节点而不是进一步缩字。',
f'- 四图一表按现有高宽比合计约 {height_mm:.0f} mm 高（不含正式 ACL 图注）；实际浮动与分页需要之后在 ACL 模板中验证。全部五项作为正文必备图表，扩展表与额外支持内容放附录。',
'','## 重建','','先运行 `scripts/sync_acl_citation_labels.py`，再运行 `scripts/build_reference_style_assets.py`，随后运行 `scripts/write_figure_integration.py`。需要 reportlab、pypdf、pypdfium2，以及 Times New Roman、Arial、Comic Sans MS 字体。字体文件不随仓库分发。']
(ROOT/'docs/图表风格对应与证据核验.md').write_text('\n'.join(lines)+'\n')
(OUT/'README.md').write_text('''# Reference-style assets

Four figures and one table adapted to the text-LLM hallucination survey, following the five user-supplied design references. Content and vector drawings were rebuilt; no source-paper photograph is reused.

- [Five-page review PDF](Figures_and_Table_Review.pdf)
- [Figure 1: illustrative hallucinations](figure_1_hallucination_examples.png)
- [Figure 2: survey structure](figure_2_survey_structure.png)
- [Figure 3: evaluation taxonomy](figure_3_evaluation_taxonomy.png)
- [Figure 4: causes and mitigation](figure_4_causes_mitigation.png)
- [Table 1: benchmarks](table_1_benchmarks.png)
- [Evidence and design attribution](../../docs/图表风格对应与证据核验.md)
- [Figure-to-section logic audit](../../docs/图表与全文逻辑闭环.md)
- [In-figure citations and BibTeX mapping](../../docs/图内引用核对.md)

Each item has a caption-free vector PDF and editable SVG for insertion; PNG previews and the review PDF include captions. The table also has native LaTeX and CSV. LaTeX files here are float fragments, not a manuscript. They have not been compiled inside the final ACL project.
''')
clines=['# 图内引用核对','',
 '2026-10-02：按用户要求，Fig.2、Fig.3、Fig.4 在节点内使用作者—年份引用，并保留范文的树形/流水线风格。本文件记录每个显示标签对应的唯一文献；未撰写论文正文。','',
 'Fig.2 每个子节选 4–5 篇代表作；Fig.3 对九个基准逐项引用；Fig.4 保留十二篇方法文献，另加入一篇评价可靠性文献。重复出现同一论文是章节导航、评价分类或机制说明的交叉引用，不是重复增加文献条目。','',
 '作者、年份、标题和 BibTeX key 来自已筛选文献库。分类依据沿用方法/基准矩阵与选择性全文阅读记录；本轮重新核对了 PrefixNLI、Recall vs. truthfulness、Correctness and faithfulness、Internal-state probe 的 ACL 官方记录，扩充 Fig.2 时另核对了 RHIO、UAlign、ReFL、Stable-RAG 的官方记录和摘要；未声称完成所有论文全文复核。','',
 '图内文字不是 LaTeX 命令；`figure_includes.tex` 使用逐图显式 `\\nocite{实际显示的键}` 登记参考文献。这与 `\\nocite{*}` 不同，不会把未使用的全部 87 篇自动加入论文。当前标签已与 `bibliography/acl_label_proof/citation_labels.bbl` 一致；五组内容文献冲突及设计来源引入的第六组均已处理。正文增删引用后，运行 `scripts/sync_acl_citation_labels.py --aux 正文.aux`，再重建图形并重新导入 draw.io，以匹配最终引用集合。','']
nodes=json.loads((OUT/'figure2_node_citations.json').read_text())
clines += ['## Fig.2 逐节点数量','', '| 子节 | 节点 | 引用数 |', '|---|---|---:|']
for n in nodes:clines.append(f"| {n['section']} | {n['node']} | {n['paper_count']} |")
clines += ['', f"共 {len(nodes)} 个绿色节点、{sum(n['paper_count'] for n in nodes)} 次引用；去重后 {len(set(i for n in nodes for i in n['paper_ids']))} 篇。", '']
csvrows=[]
for name,number in [('figure_2_survey_structure',2),('figure_3_evaluation_taxonomy',3),('figure_4_causes_mitigation',4)]:
 entries=citation_map[name]
 clines += [f'## Fig.{number}：{len(entries)} 篇文献','', '| 图内显示 | 原始文献 | BibTeX key |', '|---|---|---|']
 for a in entries:
  clines.append(f"| {a['display']} | [{a['title']}]({a['url']}) | `{a['citekey']}` |")
  csvrows.append({'figure':number,**a})
 clines.append('')
(ROOT/'docs/图内引用核对.md').write_text('\n'.join(clines)+'\n')
with (OUT/'figure_citations.csv').open('w',newline='') as fp:
 w=csv.DictWriter(fp,fieldnames=['figure','id','citekey','display','title','url','year']);w.writeheader();w.writerows(csvrows)
print('Wrote table/figure TeX fragments, two design BibTeX records, and provenance notes.')
