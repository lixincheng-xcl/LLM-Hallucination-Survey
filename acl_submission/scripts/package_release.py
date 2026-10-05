"""Package verified public sources and anonymous review materials."""
from pathlib import Path
import hashlib,json,re,shutil,zipfile
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
release=R/'release';release.mkdir(exist_ok=True)
assert json.loads((R/'validation.json').read_text())['status']=='passed'
review=R/'build/main.pdf';public=R/'build_author/author_version.pdf'
assert hashlib.sha256(review.read_bytes()).hexdigest()==json.loads((R/'validation.json').read_text())['pdf_sha256']
r=PdfReader(review);a=PdfReader(public)
assert 'Xincheng Li' in a.pages[0].extract_text()
assert 'xli798@aucklanduni.ac.nz' in a.pages[0].extract_text()
repo='https://github.com/lixincheng-xcl/LLM-Hallucination-Survey'
uris=[str(x.get_object().get('/A',{}).get('/URI','')) for p in a.pages for x in p.get('/Annots',[])]
assert repo in uris
for p in r.pages:
 assert not any(x.lower() in p.extract_text().lower() for x in ['Xincheng Li','xli798','lixincheng-xcl','/Users/'])
for file,label in [(review,'ACL_Review_Anonymous.pdf'),(public,'ACL_Author_Version.pdf')]:shutil.copyfile(file,release/label)
base=[R/x for x in ['main.tex','acl.sty','acl_natbib.bst','references.bib','design_sources.bib']]+sorted((R/'sections').glob('*.tex'))+sorted((R/'figures').glob('*.pdf'))
audit=[p for p in (R/'audit').iterdir() if p.is_file() and p.suffix in ['.md','.csv','.json','.bib']]
def anon_text(s):
 s=s.replace('frozen coursework release ca6e155 (Appendix Table 8)','pre-existing representative-method resource table')
 s=s.replace('coursework','earlier survey')
 assert not any(x.lower() in s.lower() for x in ['xincheng','xli798','lixincheng','/Users/'])
 return s
readme='''# Anonymous materials

The manuscript is a critical narrative survey with a bounded thirteen-study documentary audit. The data are source-linked descriptions, not new model experiments or human annotation. The CSV, codebook, source manifests, and notes record inspected passages and uncertainties. Full source-paper PDFs are not redistributed. No field-wide prevalence estimate is supported.

For the anonymous source package, compile main.tex using pdfLaTeX/BibTeX or latexmk -pdf main.tex. The optional public identity wrapper is intentionally excluded. The separate supplement contains the detailed audit records. Original figures are preserved unchanged and their visual-design sources are cited in Appendix A.
'''
with zipfile.ZipFile(release/'ACL_Anonymous_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in base:z.writestr(str(p.relative_to(R)),anon_text(p.read_text()) if p.suffix!='.pdf' else p.read_bytes())
 z.writestr('README.md',readme)
with zipfile.ZipFile(release/'ACL_Anonymous_Supplement.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in audit:z.writestr(str(p.relative_to(R)),anon_text(p.read_text()))
 z.writestr('README.md',readme)
 z.writestr('ASSET_NOTICE.md',anon_text((R/'ASSET_NOTICE.md').read_text()))
with zipfile.ZipFile(release/'ACL_Overleaf_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in base+[R/'identity.tex',R/'author_version.tex',R/'ASSET_NOTICE.md']+audit:
  z.write(p,str(p.relative_to(R)))
 z.writestr('README.md','Compile main.tex for anonymous review; choose author_version.tex for the named version. Both use the same section and figure files. This is an unsubmitted research draft. Author verification is required.\n')
manifest={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in release.iterdir() if p.suffix in ['.pdf','.zip']}
(release/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'anonymous_identity_scan':'passed','author_name_email_repo_link':'passed','release_files':list(manifest)},indent=2))
