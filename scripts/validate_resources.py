from pathlib import Path
import json,re,csv,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
papers=json.loads((R/'data/papers.json').read_text());stats=json.loads((R/'data/statistics.json').read_text())
assert len(papers)==stats['count']==87
assert len({p['id'] for p in papers})==87
assert len({p['citekey'] for p in papers})==87
assert all(2022<=p['year']<=2026 and p['title'] and p['authors'] and p['url'].startswith('https://') for p in papers)
assert all(p['category'] and p['subcategory'] and p['include_reason'] and p['review_question'] for p in papers)
assert len(list(csv.DictReader((R/'data/papers.csv').open())))==87
bib=(R/'bibliography/references.bib').read_text();keys=re.findall(r'@\w+\{([^,]+),',bib)
assert len(keys)==87 and set(keys)=={p['citekey'] for p in papers}
assert (R/'bibliography/references.ris').read_text().count('ER  -')==87
depth=0
for i,c in enumerate(bib):
 if i and bib[i-1]=='\\':continue
 if c=='{':depth+=1
 elif c=='}':depth-=1
 assert depth>=0
assert depth==0
for p in (R/'figures').glob('*.svg'):ET.parse(p)
assert len(list((R/'figures').glob('*.svg')))==3
assert len(list((R/'figures').glob('*.pdf')))==3
assert len(list((R/'figures').glob('*.png')))==3
missing=[]
for p in R.rglob('*.md'):
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if dest.startswith(('https://','http://','#')):continue
  if not (p.parent/dest.split('#')[0]).exists():missing.append((str(p),dest))
assert not missing,missing
print('PASS: 87 unique records and citations; metadata/CSV/RIS consistency; balanced BibTeX braces; 3 vector diagrams; local Markdown links.')
