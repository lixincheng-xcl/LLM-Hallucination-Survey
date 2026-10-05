"""Validate, package, and fresh-compile the two venue deliverables."""
from pathlib import Path
import concurrent.futures,hashlib,json,re,shutil,subprocess,tempfile,zipfile
import pypdfium2 as pdfium
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];W=R/'build_venue_packages';O=R/'submission_packages'
repo_url='https://github.com/lixincheng-xcl/LLM-Hallucination-Survey'
expected=json.loads((R/'audit/frozen_figure_labels.json').read_text())
baselines={'arxiv':R/'release/ACL_Author_Version.pdf','acl_arr':R/'release/ACL_Review_Anonymous.pdf'}
reports=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def labels(bbl):
    out={}
    for o,k in re.findall(r'\\bibitem\[\{(.*?)\}\]\{([^}]+)\}',bbl,re.S):
        a,y=re.match(r'(.+?)\((.*?)\)',o,re.S).groups();a=' '.join(a.replace('~',' ').split());y=re.sub(r'\{\\natexlab\{([a-z]+)\}\}',r'\1',y);out[k]=a+', '+y
    return out
for venue in ['arxiv','acl_arr']:
    src=W/(venue+'_source');out=O/venue;build=src/'build'
    aux=(build/'main.aux').read_text();log=(build/'main.log').read_text();bbl=(build/'main.bbl').read_text()
    assert 'Overfull' not in log and 'undefined' not in log.lower() and 'Float too large' not in log
    end=int(re.search(r'\\newlabel\{sec:mainend\}\{\{7\}\{(\d+)\}',aux)[1]);assert end==8
    biblabels=labels(bbl);assert len(biblabels)==92
    assert all(biblabels[k]==v for k,v in expected.items())
    for p in (src/'figures').glob('*.pdf'):assert digest(p)==digest(R/'figures'/p.name)
    pdf=PdfReader(build/'main.pdf');text='\n'.join(p.extract_text() for p in pdf.pages);assert len(pdf.pages)==23
    uris=[str(x.get_object().get('/A',{}).get('/URI','')) for p in pdf.pages for x in p.get('/Annots',[])]
    if venue=='arxiv':
        assert 'Xincheng Li' in text and 'xli798@aucklanduni.ac.nz' in text
        assert 'School of Computer Science, University of Auckland' in text and repo_url in uris
        assert 'Anonymous ACL submission' not in text
    else:
        combined=text+' '+str(pdf.metadata)+' '+' '.join(uris)
        assert not any(x.lower() in combined.lower() for x in ['Xincheng Li','xli798','lixincheng-xcl','University of Auckland','/Users/'])
    # Full-document rendered equality with the already reviewed corresponding PDF.
    old=pdfium.PdfDocument(baselines[venue]);new=pdfium.PdfDocument(build/'main.pdf');equal=[]
    for i in range(len(new)):
        im=new[i].render(scale=1).to_pil().convert('RGB');ref=old[i].render(scale=1).to_pil().convert('RGB')
        equal.append(im.size==ref.size and im.tobytes()==ref.tobytes())
        if i in [0,7]:im.save(W/f'{venue}-page-{i+1}.png')
    assert all(equal),(venue,equal)
    shutil.copyfile(build/'main.bbl',src/'main.bbl')
    pdfname='arXiv_Paper.pdf' if venue=='arxiv' else 'ACL_ARR_Anonymous.pdf'
    zipname='arXiv_Source.zip' if venue=='arxiv' else 'ACL_ARR_Anonymous_Source.zip'
    shutil.copyfile(build/'main.pdf',out/pdfname)
    source_files=[src/n for n in ['main.tex','main.bbl','acl.sty','acl_natbib.bst','references.bib','design_sources.bib']]+sorted((src/'sections').glob('*.tex'))+sorted((src/'figures').glob('*.pdf'))
    with zipfile.ZipFile(out/zipname,'w',zipfile.ZIP_DEFLATED) as z:
        for p in source_files:z.write(p,p.relative_to(src))
    reports.append({'venue':venue,'pdf':pdfname,'source_zip':zipname,'main_pages':end,'total_pages':len(pdf.pages),'references':len(biblabels),'figure_labels_checked':len(expected),'single_explicit_entry':'main.tex','compiled_bibliography_included':True,'frozen_figure_pdfs_unchanged':True,'all_pages_render_identical_to_reviewed_version':True,'local_compiler':'pdfTeX/BibTeX, TeX Live 2026','platform_processing':'not performed','pdf_sha256':digest(out/pdfname),'source_zip_sha256':digest(out/zipname)})
shutil.copyfile(R/'release/ACL_Anonymous_Supplement.zip',O/'acl_arr/ACL_ARR_Anonymous_Supplement.zip')
with zipfile.ZipFile(O/'acl_arr/ACL_ARR_Anonymous_Supplement.zip') as z:
    for n in z.namelist():
        t=z.read(n).decode('utf-8');assert not any(x.lower() in t.lower() for x in ['xincheng','xli798','lixincheng','/Users/']),n

def fresh_compile(report):
    venue=report['venue'];d=Path(tempfile.mkdtemp(prefix='venue_submission_check_'))
    with zipfile.ZipFile(O/venue/report['source_zip']) as z:z.extractall(d)
    assert sum(r'\documentclass' in p.read_text() for p in d.rglob('*.tex'))==1
    assert not (d/'identity.tex').exists() and not (d/'author_version.tex').exists()
    # A plain pdfLaTeX run exercises the included .bbl without invoking BibTeX.
    for _ in range(3):
        proc=subprocess.run(['/Library/TeX/texbin/pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=d,capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(proc.stdout[-4000:])
    log=(d/'main.log').read_text();assert 'undefined' not in log.lower() and 'Overfull' not in log
    actual=PdfReader(d/'main.pdf');assert len(actual.pages)==23
    return report,d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    compiled=list(ex.map(fresh_compile,reports))
# PDFium is not thread-safe; render the independently compiled PDFs sequentially.
reports=[]
for report,d in compiled:
    a=pdfium.PdfDocument(d/'main.pdf');b=pdfium.PdfDocument(O/report['venue']/report['pdf'])
    assert all(a[i].render(scale=.75).to_pil().tobytes()==b[i].render(scale=.75).to_pil().tobytes() for i in range(len(a)))
    a.close();b.close()
    report['fresh_zip_compile_without_bibtex']='passed'
    reports.append(report)
for report in reports:(O/report['venue']/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'validation.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports,indent=2))
