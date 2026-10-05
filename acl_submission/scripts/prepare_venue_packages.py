"""Build single-entry arXiv and ACL/ARR sources from the reviewed master."""
from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parents[1]
W=R/'build_venue_packages'
O=R/'submission_packages'
master=(R/'main.tex').read_text()
style=r'''\ifdefined\PublicVersion
\usepackage[preprint]{acl}
\else
\usepackage[review]{acl}
\fi'''
identity=r'''\ifdefined\PublicVersion
\input{identity}
\else
\author{Anonymous ACL submission}
\newcommand{\SurveyMaterials}{The accompanying materials provide the extraction protocol and source-linked evidence records.}
\fi'''
assert master.count(style)==1 and master.count(identity)==1
for venue in ['arxiv','acl_arr']:
    root=W/(venue+'_source');root.mkdir(parents=True,exist_ok=True)
    out=O/venue;out.mkdir(parents=True,exist_ok=True)
    for n in ['acl.sty','acl_natbib.bst','references.bib','design_sources.bib']:
        shutil.copyfile(R/n,root/n)
    (root/'sections').mkdir(exist_ok=True);(root/'figures').mkdir(exist_ok=True)
    for p in (R/'sections').glob('*.tex'):shutil.copyfile(p,root/'sections'/p.name)
    for p in (R/'figures').glob('*.pdf'):shutil.copyfile(p,root/'figures'/p.name)
    if venue=='arxiv':
        source=master.replace(style,r'\usepackage[preprint]{acl}').replace(identity,(R/'identity.tex').read_text().strip())
    else:
        source=master.replace(style,r'\usepackage[review]{acl}').replace(identity,r'''\author{Anonymous ACL submission}
\newcommand{\SurveyMaterials}{The accompanying materials provide the extraction protocol and source-linked evidence records.}''')
    assert 'PublicVersion' not in source and r'\input{identity}' not in source
    (root/'main.tex').write_text(source)
    assert sum(r'\documentclass' in p.read_text() for p in root.rglob('*.tex'))==1
    if venue=='acl_arr':
        for p in root.rglob('*'):
            if p.is_file() and p.suffix in ['.tex','.bib','.sty','.bst']:
                assert not any(x.lower() in p.read_text().lower() for x in ['xincheng','xli798','lixincheng-xcl','/Users/']),p
print(json.dumps({'working_directory':str(W),'deliverables':str(O)},indent=2))
