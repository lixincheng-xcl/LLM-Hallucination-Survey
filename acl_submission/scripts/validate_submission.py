"""Validate compiled review draft, frozen figures, evidence records and citation labels."""
from pathlib import Path
import csv, hashlib, json, re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
build=ROOT/'build'
aux=(build/'main.aux').read_text()
bbl=(build/'main.bbl').read_text()
log=(build/'main.log').read_text()
assert 'Overfull' not in log
assert 'undefined' not in log.lower()
assert 'Warning' not in (build/'main.blg').read_text()
end=int(re.search(r'\\newlabel\{sec:mainend\}\{\{7\}\{(\d+)\}',aux)[1])
assert end<=8,end
labels={}
for optional,key in re.findall(r'\\bibitem\[\{(.*?)\}\]\{([^}]+)\}',bbl,re.S):
    author,year=re.match(r'(.+?)\((.*?)\)',optional,re.S).groups()
    author=' '.join(author.replace('~',' ').split())
    year=re.sub(r'\{\\natexlab\{([a-z]+)\}\}',r'\1',year)
    labels[key]=author+', '+year
baseline=json.loads((ROOT/'audit/frozen_figure_labels.json').read_text())
assert len(baseline)==55
for key,label in baseline.items(): assert labels[key]==label,(key,labels[key],label)
expected={
'Fig1_hallucination_examples.pdf':'474b32a23550f60804a062c14964c52e26ded41484ae3e7af869d75d23621f46',
'Fig2_survey_structure.pdf':'89f391591c37fa1d9f5c4ea3017fb27179f5ada3bf024736440b6dcea232ce30',
'Fig3_evaluation_taxonomy.pdf':'72db9ae075199df26a58880263f1a4525a888a0d4a4ce8ebfc21f375436ba514',
'Fig4_causes_mitigation.pdf':'474dacf5b8182f9bdeb12fe83557b2b9e43acfe0c30534a3dafc6d146b177e0e'}
for name,digest in expected.items():
    assert hashlib.sha256((ROOT/'figures'/name).read_bytes()).hexdigest()==digest,name
baseline_pdf=REPO/'manuscript/LLM_Hallucination_Survey.pdf'
if baseline_pdf.exists():
    assert hashlib.sha256(baseline_pdf.read_bytes()).hexdigest()=='7dd4e43a6717586603617430c5de1f026d3e45d08124fb433bf2b54fcbb26ab9'
pdf=PdfReader(build/'main.pdf')
text='\n'.join(p.extract_text() for p in pdf.pages)
for identifier in ['Xincheng Li','xli798','lixincheng-xcl','/Users/','University of Auckland']:
    assert identifier.lower() not in text.lower(),identifier
figpages={}
for k in ['examples','structure','evaluation','mitigation']:
    m=re.search(r'\\newlabel\{fig:'+k+r'\}\{\{(\d+)\}\{(\d+)\}',aux)
    assert m
    figpages[m[1]]=int(m[2])
assert list(figpages)==['1','2','3','4'] and max(figpages.values())<=8
assert figpages['1']==1
placements=[]
def visitor(op, operands, cm, tm):
    if op!=b'Do': return
    obj=pdf.pages[0]['/Resources']['/XObject'][operands[0]].get_object()
    if obj.get('/Subtype')!='/Form': return
    bb=list(map(float,obj['/BBox']))
    a,b,c,d,x,y=cm
    assert abs(b)<1e-6 and abs(c)<1e-6 and abs(a-d)<1e-6
    placements.append({'x':x,'width':(bb[2]-bb[0])*a})
pdf.pages[0].extract_text(visitor_operand_before=visitor)
assert len(placements)==1 and placements[0]['x']>float(pdf.pages[0].mediabox.width)/2
assert 217<placements[0]['width']<220
n_tables=0
for source in (ROOT/'sections').glob('*.tex'):
    for block in re.findall(r'\\begin\{table\*?\}.*?\\end\{table\*?\}',source.read_text(),re.S):
        endtab=max(block.rfind(r'\end{tabularx}'),block.rfind(r'\end{tabular}'))
        assert endtab<block.index(r'\caption{')<block.index(r'\label{tab:')
        n_tables+=1
rows=list(csv.DictReader((ROOT/'audit/evidence_cases.csv').open()))
assert len(rows)==13 and len({x['citekey'] for x in rows})==13
fields=['study','citekey','source_url','pdf_url','source_sha256','inspected_sections','information_control','information_locator','evaluation_separation','evaluation_locator','resource_reporting','resource_locator','joint_validation','joint_locator','caveat','verified_on']
for row in rows:
    for field in fields: assert row[field].strip(),(row['study'],field)
    assert re.fullmatch('[a-f0-9]{64}',row['source_sha256'])
    assert row['citekey'] in labels,row['citekey']
assert not any('Enlarged view of Figure' in p.extract_text() for p in pdf.pages)
report={'status':'passed','main_end_page':end,'total_pages':len(pdf.pages),'references':len(labels),'figure_label_keys':55,'figure_pages':figpages,'figure1_right_single_column':True,'frozen_figures_unchanged':True,'coursework_pdf_unchanged':True if baseline_pdf.exists() else 'not checked in standalone package','table_captions_below':n_tables,'audit_cases':len(rows),'anonymous_pdf_identity_scan':'passed','overfull_boxes':0,'unresolved_references':0,'pdf_sha256':hashlib.sha256((build/'main.pdf').read_bytes()).hexdigest()}
(ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
