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
with (ROOT/'data/manuscript_citations.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['citekey','record_id','title','in_manuscript','acl_label'])
    for p in json.loads((ROOT/'data/papers.json').read_text()):
        w.writerow([p['citekey'],p['record_id'],p['title'],p['citekey'] in labels,labels.get(p['citekey'],'')])
report = {'status':'passed','main_pages':7,'references_start_page':8,
          'appendix_start_page':appendix_page,'total_pages':len(pages),
          'research_references':86,'design_references':2,'total_references':88,
          'figure_citation_keys_checked':55,'figure_label_mismatches':0,
          'figures_on_pages':fig_pages,'undefined_citations_or_references':0,
          'figure1_placement':fig1,'figure1_proportional_single_column':True,
          'github_link_only_in_abstract_final_sentence':True,
          'overfull_boxes':0,'user_figure_hashes':'all match manifest',
          'pdf_sha256':hashlib.sha256((M/'build/main.pdf').read_bytes()).hexdigest(),
          'compiler':'pdfTeX / BibTeX, TeX Live 2026; unmodified supplied ACL style',
          'checks':'Structural/citation checks; visual review is recorded separately.'}
(M/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
