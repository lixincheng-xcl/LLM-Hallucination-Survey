"""Cross-check native text and vector PDF labels against ACL BibTeX."""
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import xml.etree.ElementTree as ET
import json, re, html, hashlib

ROOT=Path(__file__).resolve().parents[1]
labels=json.loads((ROOT/'data/acl_citation_labels.json').read_text())
mapping=json.loads((ROOT/'figures/reference_style/figure_citation_map.json').read_text())
def compact(s): return re.sub(r'\s+', '', html.unescape(s))
results=[]
for path in sorted((ROOT/'figures/drawio').glob('Fig[1-4]_*.drawio')):
    cells=ET.parse(path).findall('.//mxCell')
    assert cells, 'Native mxGraph cells missing'
    ids={c.get('id') for c in cells}
    assert len(ids)==len(cells)
    assert all(c.get('parent') in ids for c in cells if c.get('parent'))
    assert all('image=' not in c.get('style','') and '<img' not in c.get('value','') for c in cells)
    native=compact(' '.join(re.sub('<[^>]+>','',c.get('value','')) for c in cells))
    n=path.name[3]
    key='figure_1_hallucination_examples' if n=='1' else next(k for k in mapping if k.startswith('figure_'+n+'_'))
    for entry in mapping.get(key,[]):
        assert labels['labels'][entry['citekey']]['label'] in entry['display']
        assert compact(entry['display']) in native, (path.name, entry['display'])
    image=Image.open(path.with_suffix('.png'))
    assert image.width>2000
    results.append({'file':path.name,'vertices':sum(c.get('vertex')=='1' for c in cells),
                    'edges':sum(c.get('edge')=='1' for c in cells),
                    'text_cells':sum(bool(c.get('value')) and c.get('vertex')=='1' for c in cells),
                    'embedded_images':0,'png_size':image.size,
                    'citations_verified':len(mapping.get(key,[]))})
assert len(results)==4
for key,entries in mapping.items():
    text=compact(PdfReader(ROOT/'figures/reference_style'/f'{key}.pdf').pages[0].extract_text())
    for entry in entries:assert compact(entry['display']) in text,(key,entry['display'])
for filename,digest in labels['hashes'].items():
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest, filename
assert len(PdfReader(ROOT/'figures/reference_style/Figures_and_Table_Review.pdf').pages)==5
(ROOT/'figures/drawio/validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
print('PASS: current citation labels match ACL BibTeX, vector PDF and native draw.io text.')
