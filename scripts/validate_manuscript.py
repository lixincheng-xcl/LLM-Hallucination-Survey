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
with (ROOT/'data/manuscript_citations.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['citekey','record_id','title','in_manuscript','acl_label'])
    for p in json.loads((ROOT/'data/papers.json').read_text()):
        w.writerow([p['citekey'],p['record_id'],p['title'],p['citekey'] in labels,labels.get(p['citekey'],'')])
report = {'status':'passed','main_pages':7,'references_start_page':8,
          'appendix_start_page':appendix_page,'total_pages':len(pages),
          'research_references':86,'design_references':2,'total_references':88,
          'figure_citation_keys_checked':55,'figure_label_mismatches':0,
          'figures_on_pages':fig_pages,'undefined_citations_or_references':0,
          'overfull_boxes':0,'user_figure_hashes':'all match manifest',
          'pdf_sha256':hashlib.sha256((M/'build/main.pdf').read_bytes()).hexdigest(),
          'compiler':'pdfTeX / BibTeX, TeX Live 2026; unmodified supplied ACL style',
          'checks':'Structural/citation checks; visual review is recorded separately.'}
(M/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
