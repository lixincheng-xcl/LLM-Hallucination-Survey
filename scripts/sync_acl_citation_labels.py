"""Obtain artwork citation labels from the supplied ACL BST using real BibTeX.

The default set is the papers visibly cited in figures/table plus design sources.
Pass --aux /path/to/final.aux once manuscript citations exist. No prose is created.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'bibliography/acl_label_proof'
parser = argparse.ArgumentParser()
parser.add_argument('--aux', type=Path)
args = parser.parse_args()
OUT.mkdir(exist_ok=True)
maps = json.loads((ROOT/'figures/reference_style/figure_citation_map.json').read_text())
keys = {a['citekey'] for rows in maps.values() for a in rows}
keys.update(['liu-etal-2024-lvlm-design', 'liu-etal-2025-logical-design'])
if args.aux:
    def read_aux(p):
        text = p.read_text()
        for row in re.findall(r'\\citation\{([^}]+)\}', text):
            keys.update(row.split(','))
        for name in re.findall(r'\\@input\{([^}]+)\}', text):
            read_aux(p.parent/name)
    read_aux(args.aux.resolve())
aux = '\\relax\n' + ''.join('\\citation{'+k+'}\n' for k in sorted(keys))
aux += '\\bibstyle{acl_natbib}\n\\bibdata{../references,../design_sources}\n'
(OUT/'citation_labels.aux').write_text(aux)
exe = shutil.which('bibtex') or '/Library/TeX/texbin/bibtex'
run = subprocess.run([exe, 'citation_labels'], cwd=OUT, capture_output=True, text=True)
if run.returncode or 'Warning--' in run.stdout:
    raise RuntimeError(run.stdout + run.stderr)
bbl = (OUT/'citation_labels.bbl').read_text()
labels = {}
for optional, key in re.findall(r'\\bibitem\[\{(.*?)\}\]\{([^}]+)\}', bbl, re.S):
    author, year = re.match(r'(.+?)\((.*?)\)', optional, re.S).groups()
    author = ' '.join(author.replace('~', ' ').split())
    year = re.sub(r'\{\\natexlab\{([a-z]+)\}\}', r'\1', year)
    labels[key] = {'author': author, 'year_label': year, 'label': author+', '+year}
assert len(labels) == len(keys), (len(labels), len(keys))
payload = {'scope': 'current figure/table citations and design sources; add final manuscript AUX when available',
           'bibtex': run.stdout.splitlines()[0],
           'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [ROOT/'bibliography/references.bib', ROOT/'bibliography/design_sources.bib', OUT/'acl_natbib.bst']},
           'cited_keys': sorted(keys), 'labels': labels}
(ROOT/'data/acl_citation_labels.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
print(f'ACL BibTeX: {len(labels)} labels, {sum(bool(re.search("[a-z]$", x["year_label"])) for x in labels.values())} suffixed entries.')
for key, row in labels.items():
    if re.search('[a-z]$',row['year_label']): print(key, '=>', row['label'])
