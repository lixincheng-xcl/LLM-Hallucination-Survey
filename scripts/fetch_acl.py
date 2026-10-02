import concurrent.futures, json, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / 'local_cache'
ROOT.mkdir(exist_ok=True)
RAW = ROOT / 'raw'
RAW.mkdir(exist_ok=True)
names = [f'{y}.{v}' for y in range(2022,2027) for v in ['acl','emnlp','naacl','eacl','findings','tacl']]
def fetch(name):
    path = RAW / (name+'.xml')
    url = f'https://raw.githubusercontent.com/acl-org/acl-anthology/master/data/xml/{name}.xml'
    try:
        if not path.exists():
            path.write_bytes(urllib.request.urlopen(url, timeout=40).read())
        root = ET.parse(path).getroot()
        items=[]
        for vol in root.findall('volume'):
            meta=vol.find('meta')
            venue=''.join(meta.find('booktitle').itertext()) if meta is not None and meta.find('booktitle') is not None else ''
            for paper in vol.findall('paper'):
                def txt(key):
                    el=paper.find(key)
                    return ''.join(el.itertext()).strip() if el is not None else ''
                title=txt('title')
                if not re.search(r'hallucinat|factual|faithful|truthful|attribution|attributed|knowledge conflict|self.?check|self.?rag|corrective retrieval|retrieval.augmented|abstain|abstention|uncertainty|know what|know when|context.faithful|chain.of.verification|refus',title,re.I):continue
                pid=f'{name}-{vol.attrib["id"]}.{paper.attrib["id"]}'
                if paper.find('url') is not None: pid=txt('url')
                authors=[]
                for a in paper.findall('author'):
                    authors.append({'first':a.findtext('first',''),'last':a.findtext('last','')})
                items.append({'id':pid,'title':title,'abstract':txt('abstract'),'authors':authors,'year':int(name[:4]),'venue_full':venue,'doi':txt('doi'),'pages':txt('pages'),'url':f'https://aclanthology.org/{pid}/','source_xml':name+'.xml'})
        return {'file':name+'.xml','url':url,'status':'ok','candidate_count':len(items)},items
    except Exception as e:return {'file':name+'.xml','url':url,'status':str(e)},[]
records=[];log=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for status,items in pool.map(fetch,names):log.append(status);records+=items
(ROOT/'raw_candidates.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(ROOT/'retrieval_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print(json.dumps({'records':len(records),'sources':log},ensure_ascii=False))
