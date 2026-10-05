"""Audit the compiled ACL paper, imported figures, and actual BibTeX labels."""
from pathlib import Path
import csv
import hashlib
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / 'manuscript'
aux = (M / 'build/main.aux').read_text()
bbl = (M / 'build/main.bbl').read_text()
log = (M / 'build/main.log').read_text()
main_end = int(re.search(r'\\newlabel\{sec:mainend\}\{\{7\}\{(\d+)\}', aux)[1])
assert main_end == 7, f'Main paper ends on page {main_end}'
assert 'Overfull' not in log and 'undefined' not in log.lower()
assert 'Warning' not in (M / 'build/main.blg').read_text()
labels = {}
for optional, key in re.findall(r'\\bibitem\[\{(.*?)\}\]\{([^}]+)\}', bbl, re.S):
    author, year = re.match(r'(.+?)\((.*?)\)', optional, re.S).groups()
    author = ' '.join(author.replace('~', ' ').split())
    year = re.sub(r'\{\\natexlab\{([a-z]+)\}\}', r'\1', year)
    labels[key] = author + ', ' + year
assert len(labels) == 88, len(labels)
assert 'extiti2023' not in labels
baseline = json.loads((ROOT / 'data/acl_citation_labels.json').read_text())['labels']
figure_map = json.loads((ROOT / 'figures/reference_style/figure_citation_map.json').read_text())
figure_keys = {x['citekey'] for rows in figure_map.values() for x in rows}
assert len(figure_keys) == 55
for key in figure_keys:
    assert labels[key] == baseline[key]['label'], (key, labels[key], baseline[key])
for name in ['references.bib', 'design_sources.bib']:
    assert (M/name).read_bytes() == (ROOT/'bibliography'/name).read_bytes()
for item in json.loads((M/'figures/manifest.json').read_text()):
    actual = hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()
    assert actual == item['sha256'], item['file']
pages = PdfReader(M/'build/main.pdf').pages
assert pages[7].extract_text().lstrip().startswith('References')
appendix_page = next(i+1 for i,p in enumerate(pages) if p.extract_text().startswith('A Selection, Provenance'))
fig_pages = {}
for key in ['examples','structure','evaluation','mitigation']:
    match = re.search(r'\\newlabel\{fig:'+key+r'\}\{\{(\d+)\}\{(\d+)\}', aux)
    fig_pages[match[1]] = int(match[2])
assert list(fig_pages) == ['1','2','3','4'] and max(fig_pages.values()) <= 7
assert fig_pages['1'] == 1, 'Figure 1 must be on page one'
main_table_pages = {}
for expected, key in enumerate(['hallucination-benchmarks', 'method-comparison'], 1):
    match = re.search(r'\\newlabel\{tab:'+key+r'\}\{\{(\d+)\}\{(\d+)\}', aux)
    assert match and int(match[1]) == expected and int(match[2]) <= 7, (key, match)
    main_table_pages[str(expected)] = int(match[2])


# Match the supplied ACL example: caption and label follow the table body.
table_caption_count = 0
for source in (M/'sections').glob('*.tex'):
    for block in re.findall(r'\\begin\{table\*?\}.*?\\end\{table\*?\}', source.read_text(), re.S):
        caption = block.index(r'\caption{')
        table_end = max(block.rfind(r'\end{tabularx}'), block.rfind(r'\end{tabular}'))
        label = block.index(r'\label{tab:')
        assert table_end >= 0 and table_end < caption < label, source
        table_caption_count += 1
assert table_caption_count == 8, table_caption_count

# Check the placed PDF form, not just the LaTeX width declaration.
placements = []
def inspect_form(operator, operands, cm, tm):
    if operator != b'Do':
        return
    obj = pages[0]['/Resources']['/XObject'][operands[0]].get_object()
    if obj.get('/Subtype') != '/Form':
        return
    bbox = [float(x) for x in obj['/BBox']]
    a, b, c, d, x, y = cm
    assert abs(b) < 1e-6 and abs(c) < 1e-6 and abs(a-d) < 1e-6
    placements.append({'x_pt': x, 'y_pt': y,
                       'width_pt': (bbox[2]-bbox[0])*a,
                       'height_pt': (bbox[3]-bbox[1])*d})
pages[0].extract_text(visitor_operand_before=inspect_form)
assert len(placements) == 1, placements
fig1 = placements[0]
assert fig1['x_pt'] > float(pages[0].mediabox.width)/2
assert 217 < fig1['width_pt'] < 220, fig1
main = (M/'main.tex').read_text()
repo_url = 'https://github.com/lixincheng-xcl/LLM-Hallucination-Survey'
abstract = main.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0].strip()
assert abstract.endswith(r'\url{'+repo_url+'}.')
main_sources = main + ''.join(p.read_text() for p in (M/'sections').glob('0*.tex'))
assert main_sources.count(repo_url) == 1
assert 'School of Computer Science, University of Auckland' in main
assert r'Email: \texttt{xli798@aucklanduni.ac.nz}' in main
assert r'\section*{Limitations}' in main
main_pdf_text = '\n'.join(p.extract_text() for p in pages[:7])
assert 'School of Computer Science, University of Auckland' in main_pdf_text
assert 'xli798@aucklanduni.ac.nz' in main_pdf_text
for phrase in ['Layout adapted', 'Tree design adapted', 'Tree layout follows',
               'examples are original, not measured outputs', 'three-rule design follows']:
    assert phrase not in main_pdf_text, phrase
appendix_source = (M/'sections/appendix.tex').read_text()
assert r'\onecolumn' not in appendix_source
assert 'app:example-large' not in aux and 'app:example-large' not in main
assert len(pages) == 18
assert not any('Enlarged view of Figure' in p.extract_text() for p in pages)
assert '15 September 2026' in appendix_source
assert '1 October 2026' not in appendix_source
with (ROOT/'data/manuscript_citations.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['citekey','record_id','title','in_manuscript','acl_label'])
    for p in json.loads((ROOT/'data/papers.json').read_text()):
        w.writerow([p['citekey'],p['record_id'],p['title'],p['citekey'] in labels,labels.get(p['citekey'],'')])
report = {'status':'passed','main_pages':7,'references_start_page':8,
          'appendix_start_page':appendix_page,'total_pages':len(pages),
          'research_references':86,'design_references':2,'total_references':88,
          'figure_citation_keys_checked':55,'figure_label_mismatches':0,
          'figures_on_pages':fig_pages,'main_tables_on_pages':main_table_pages,
          'table_captions_below_table_body':table_caption_count,
          'undefined_citations_or_references':0,
          'figure1_placement':fig1,'figure1_proportional_single_column':True,
          'github_link_only_in_abstract_final_sentence':True,
          'affiliation_and_email_verified':True,'dedicated_limitations_section':True,
          'main_caption_process_wording_removed':True,'appendix_text_two_columns':True,
          'figure1_enlarged_appendix_removed':True,
          'literature_snapshot':'2026-09-15',
          'overfull_boxes':0,'user_figure_hashes':'all match manifest',
          'pdf_sha256':hashlib.sha256((M/'build/main.pdf').read_bytes()).hexdigest(),
          'compiler':'pdfTeX / BibTeX, TeX Live 2026; unmodified supplied ACL style',
          'checks':'Structural/citation checks; visual review is recorded separately.'}
(M/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
