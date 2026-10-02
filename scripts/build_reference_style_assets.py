"""Recreate the supplied figure/table design language with original text-LLM content.
Run with the Codex bundled Python (reportlab, pypdf, pypdfium2).
The reference screenshots are design references, not image assets pasted into outputs.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json, csv, re, math, textwrap, argparse
from collections import defaultdict
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import toColor as HexColor
import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'figures'/'reference_style'
OUT.mkdir(parents=True,exist_ok=True)
TMP=ROOT.parent/'tmp'/'pdfs'/'reference_style'; TMP.mkdir(parents=True,exist_ok=True)
FONTS=Path('/System/Library/Fonts/Supplemental')
fontfiles={'T':'Times New Roman.ttf','TI':'Times New Roman Italic.ttf','TB':'Times New Roman Bold.ttf','A':'Arial.ttf','AB':'Arial Bold.ttf','C':'Comic Sans MS.ttf','CB':'Comic Sans MS Bold.ttf'}
for name,file in fontfiles.items(): pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
svgfonts={'T':('Times New Roman','normal','normal'),'TI':('Times New Roman','normal','italic'),'TB':('Times New Roman','bold','normal'),'A':('Arial','normal','normal'),'AB':('Arial','bold','normal'),'C':('Comic Sans MS','normal','normal'),'CB':('Comic Sans MS','bold','normal')}
PAPERS={p['id']:p for p in json.loads((ROOT/'data/papers.json').read_text())}
ACL_LABELS=json.loads((ROOT/'data/acl_citation_labels.json').read_text())['labels']
USED=set()
USED_BY_FIG=defaultdict(list)
ACTIVE_FIG=None

def cite(pid,label=''):
 p=PAPERS[pid]; USED.add(pid)
 resolved=ACL_LABELS[p['citekey']]['label']
 display=(label+' ' if label else '')+f'[{resolved}]'
 item={'id':pid,'citekey':p['citekey'],'display':display,'title':p['title'],'url':p['url'],'year':p['year']}
 if item not in USED_BY_FIG[ACTIVE_FIG]:USED_BY_FIG[ACTIVE_FIG].append(item)
 return display

def tw(s,font,size): return pdfmetrics.stringWidth(s,font,size)

def wrap(s,width,font='T',size=21):
 out=[]
 for paragraph in s.split('\n'):
  line=''
  for word in re.findall(r'et al\.,?|\S+',paragraph):
   if line and tw(line+' '+word,font,size)>width:
    out.append(line);line=word
   else: line=(line+' '+word).strip()
  out.append(line)
 return out

class Drawing:
 def __init__(self,name,w,h,caption):
  global ACTIVE_FIG
  ACTIVE_FIG=name
  self.name,self.w,self.h,self.caption=name,w,h,caption;self.ops=[];self.boxes=[];self.label_checks=[]
 def rect(self,x,y,w,h,fill='white',stroke='#bd22c6',r=8,lw=1.1,dash=False): self.ops.append(('rect',(x,y,w,h,fill,stroke,r,lw,dash)))
 def line(self,pts,color='#494949',lw=1.9,dash=False,arrow=False): self.ops.append(('line',(pts,color,lw,dash,arrow)))
 def circle(self,x,y,r,fill,stroke='#444444',lw=1.2):self.ops.append(('circle',(x,y,r,fill,stroke,lw)))
 def text(self,x,y,s,size=21,font='T',color='#000000',anchor='start',rotate=0):
  if font=='T' and 'et al.' in s and not rotate:
   pieces=re.split(r'(et al\.)',s)
   total=sum(tw(v,'TI' if v=='et al.' else font,size) for v in pieces)
   xx=x-total/2 if anchor=='middle' else x-total if anchor=='end' else x
   for v in pieces:
    ft='TI' if v=='et al.' else font
    self.ops.append(('text',(xx,y,v,size,ft,color,'start',0)));xx+=tw(v,ft,size)
  else:self.ops.append(('text',(x,y,s,size,font,color,anchor,rotate)))
 def rich(self,x,y,runs,size=21,font='T'):
  for item in runs:
   if isinstance(item,str): s,col,ft=item,'#000000',font
   else:
    s,col,*fts=item; ft=fts[0] if fts else font
   self.text(x,y,s,size,ft,col);x+=tw(s,ft,size)
 def paragraph(self,x,y,s,width,size=21,font='T',color='#000000',leading=None):
  ls=wrap(s,width,font,size); lead=leading or size*1.15
  for i,t in enumerate(ls):self.text(x,y+i*lead,t,size,font,color)
  return len(ls)*lead
 def box(self,x,y,w,h,s,fill='white',stroke='#bd22c6',size=21,font='T',center=False):
  self.rect(x,y,w,h,fill,stroke)
  ls=wrap(s,w-14,font,size); lead=size*1.13
  while (len(ls)-1)*lead+size>h-5 and size>17:
   size-=0.5;ls=wrap(s,w-14,font,size);lead=size*1.13
  if (len(ls)-1)*lead+size>h-5:
   raise ValueError(('Text needs larger box',self.name,s,h))
  for i,t in enumerate(ls):
   assert tw(t,font,size)<=w-13,(s,t,w)
   self.text(x+w/2 if center else x+6,y+h/2-(len(ls)-1)*lead/2+size*.34+i*lead,t,size,font,anchor='middle' if center else 'start')
  self.boxes.append((x,y,w,h));self.label_checks.append({'text':s,'font_size':size,'width':w,'height':h})
 def render(self,c,totalh):
  for kind,a in self.ops:
   if kind=='rect':
    x,y,w,h,fill,stroke,r,lw,dash=a;c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(lw);c.setDash([7,5] if dash else [])
    c.roundRect(x,totalh-y-h,w,h,r,stroke=1,fill=1);c.setDash([])
   elif kind=='circle':
    x,y,r,fill,stroke,lw=a;c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(lw);c.circle(x,totalh-y,r,stroke=1,fill=1)
   elif kind=='text':
    x,y,s,size,font,color,anchor,rot=a;c.saveState();c.setFillColor(HexColor(color));c.setFont(font,size)
    if rot:c.translate(x,totalh-y);c.rotate(-rot);x,y=0,totalh
    if anchor=='middle':c.drawCentredString(x,totalh-y,s)
    elif anchor=='end':c.drawRightString(x,totalh-y,s)
    else:c.drawString(x,totalh-y,s)
    c.restoreState()
   elif kind=='line':
    pts,col,lw,dash,arrow=a;c.setStrokeColor(HexColor(col));c.setLineWidth(lw);c.setDash([6,4] if dash else []);p=c.beginPath();p.moveTo(pts[0][0],totalh-pts[0][1])
    for x,y in pts[1:]:p.lineTo(x,totalh-y)
    c.drawPath(p);c.setDash([])
    if arrow:
     x,y=pts[-1];p0=pts[-2];ang=math.atan2(y-p0[1],x-p0[0]);q=[(x,y),(x-11*math.cos(ang)+5*math.sin(ang),y-11*math.sin(ang)-5*math.cos(ang)),(x-11*math.cos(ang)-5*math.sin(ang),y-11*math.sin(ang)+5*math.cos(ang))]
     p=c.beginPath();p.moveTo(q[0][0],totalh-q[0][1])
     for xx,yy in q[1:]:p.lineTo(xx,totalh-yy)
     p.close();c.setFillColor(HexColor(col));c.drawPath(p,fill=1,stroke=0)
 def svg(self):
  lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img">',f'<title>{escape(self.caption)}</title>',f'<rect width="{self.w}" height="{self.h}" fill="white"/>']
  for kind,a in self.ops:
   if kind=='rect':
    x,y,w,h,fill,stroke,r,lw,dash=a;lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
   elif kind=='circle':
    x,y,r,fill,stroke,lw=a;lines.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>')
   elif kind=='line':
    pts,col,lw,dash,arrow=a;lines.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" stroke="{col}" stroke-width="{lw}" fill="none"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
    if arrow:
     x,y=pts[-1];p0=pts[-2];ang=math.atan2(y-p0[1],x-p0[0]);q=[(x,y),(x-11*math.cos(ang)+5*math.sin(ang),y-11*math.sin(ang)-5*math.cos(ang)),(x-11*math.cos(ang)-5*math.sin(ang),y-11*math.sin(ang)+5*math.cos(ang))]
     lines.append('<polygon points="'+' '.join(f'{u},{v}' for u,v in q)+f'" fill="{col}"/>')
   elif kind=='text':
    x,y,s,size,font,col,anchor,rot=a;fam,weight,style=svgfonts[font]
    lines.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" font-style="{style}" font-size="{size}" fill="{col}" text-anchor="{anchor}"'+(f' transform="rotate({rot} {x} {y})"' if rot else '')+f'>{escape(s)}</text>')
  lines.append('</svg>');p=OUT/(self.name+'.svg');p.write_text('\n'.join(lines));ET.parse(p)
 def save(self):
  self.svg();scale=453.5433/self.w
  p=OUT/(self.name+'.pdf');c=canvas.Canvas(str(p),pagesize=(453.5433,self.h*scale));c.setTitle(self.caption);c.setAuthor('Xincheng Li');c.scale(scale,scale);self.render(c,self.h);c.showPage();c.save()
  caption_lines=wrap(self.caption,self.w-26,'T',23)
  caph=len(caption_lines)*27+32;total=self.h+caph
  p=TMP/(self.name+'_captioned.pdf');c=canvas.Canvas(str(p),pagesize=(453.5433,total*scale));c.setTitle(self.caption);c.scale(scale,scale)
  if self.name.startswith('table'):
   c.saveState();c.translate(0,-caph);self.render(c,total);c.restoreState()
  else:self.render(c,total)
  c.setFont('T',23);c.setFillColor(HexColor('#000000'))
  for i,t in enumerate(caption_lines):c.drawCentredString(self.w/2,(total-27-i*27) if self.name.startswith('table') else (total-self.h-25-i*27),t)
  c.showPage();c.save()
  d=pdfium.PdfDocument(str(p));d[0].render(scale=4).to_pil().save(OUT/(self.name+'.png'))
  return p

# Fig. 2: expanded literature leaves, with dynamic height and unchanged classification.
f=Drawing('figure_2_survey_structure',1600,915,'Figure 2: The structure of this survey with representative references. Each green leaf includes four to five studies. Evaluation criteria are detailed in Fig. 3 and Table 1, and intervention mechanisms in Fig. 4. Hybrid studies may appear in more than one section.')
mag='#bc25c6';green='#d1f4c3'
structure=json.loads((ROOT/'data/figure2_structure.json').read_text())
leaf_x=699;leaf_width=881;leaf_font=25
cursor=16;positioned=[];structure_audit=[]
for group in structure['groups']:
 rows=[]
 for n in group['nodes']:
  assert 4<=len(n['papers'])<=5
  studies='; '.join(cite(p['id'],p['label']) for p in n['papers'])
  lines=wrap(studies,leaf_width-14,'T',leaf_font)
  height=max(76,len(lines)*leaf_font*1.13+15)
  cy=cursor+height/2
  rows.append((cy,height,n['label'],studies))
  structure_audit.append({'section':n['section'],'node':n['label'],'paper_count':len(n['papers']),'paper_ids':[p['id'] for p in n['papers']],'line_count':len(lines),'font_pt':round(leaf_font*453.5433/f.w,2)})
  cursor+=height+10
 positioned.append((group['label'],rows,(rows[0][0]+rows[-1][0])/2))
 cursor+=12
f.h=math.ceil(cursor-6)
root_cy=(positioned[0][2]+positioned[-1][2])/2
f.line([(56,root_cy),(76,root_cy)]);f.line([(76,positioned[0][2]),(76,positioned[-1][2])])
f.rect(15,root_cy-180,41,360,'white',mag);f.text(44,root_cy,'Hallucination in text LLMs',27,anchor='middle',rotate=-90)
for label,rows,cy in positioned:
 f.line([(76,cy),(98,cy)]);f.line([(351,cy),(367,cy)]);f.line([(367,rows[0][0]),(367,rows[-1][0])])
 f.box(98,cy-30,253,60,label,size=25)
 for y,h,sub,studies in rows:
  f.line([(367,y),(384,y)]);f.line([(674,y),(leaf_x,y)])
  f.box(384,y-30,290,60,sub,size=25)
  f.box(leaf_x,y-h/2,leaf_width,h,studies,green,mag,size=leaf_font)
(OUT/'figure2_node_citations.json').write_text(json.dumps(structure_audit,ensure_ascii=False,indent=2)+'\n')
FIGS=[f]

# Fig. 1: source cards, two dashed panels, yellow question bubbles, gray responses.
f=Drawing('figure_1_hallucination_examples',1200,780,'Figure 1: Source-faithfulness hallucinations in constructed QA and summarization examples, not measured model outputs. Green marks unsupported additions; magenta and blue mark value and relation contradictions. Highlights are illustrative, not an exhaustive taxonomy; world factuality is a separate criterion.')
GR='#00bd10';PK='#ff0098';BL='#008eff'
def avatar(f,x,y,robot=False):
 if robot:
  f.line([(x,y-24),(x,y-32)],'#007d9d',2);f.circle(x,y-34,3,'#40cce0','#007d9d')
  f.rect(x-25,y-18,7,21,'#9dddea','#007d9d',3,2);f.rect(x+18,y-18,7,21,'#9dddea','#007d9d',3,2)
  f.rect(x-20,y-25,40,43,'#b7e7ee','#007d9d',12,2);f.rect(x-15,y-13,30,17,'#0d303d','#0d303d',6)
  f.circle(x-8,y-5,4,'#ffd658','#ffd658');f.circle(x+8,y-5,4,'#ffd658','#ffd658');f.line([(x-7,y+11),(x+7,y+11)],'#20596c',2)
 else:
  f.circle(x,y,24,'#ffcf9f','#c87952',2);f.rect(x-22,y-26,44,17,'#6a3527','#4b271f',8,1.8)
  f.circle(x-8,y,3,'#35211d','#35211d');f.circle(x+8,y,3,'#35211d','#35211d');f.line([(x-7,y+12),(x,y+15),(x+7,y+12)],'#af4a41',2)

def sourcecard(f,x,y,w,h,title,lines):
 f.rect(x,y,w,h,'#f8f5ec','#c0b9a5',2,1)
 f.text(x+16,y+30,title,23,'CB','#555147')
 yy=y+63
 for s in lines:
  yy+=f.paragraph(x+16,yy,s,w-32,22,'C',leading=27)+12

f.rect(20,20,1160,426,'#ffffff','#a4ad00',0,2.5,True)
f.text(31,57,'Judgement Hallucination Examples',27,'C','#a4ad00')
sourcecard(f,42,97,360,315,'Source: library record',[
 'Northbridge Library opened in 2020.',
 'It holds 12,000 books.',
 'The archive is on the second floor.'
])
qa=[(95,'Is there a cafe in the library?','Yes, there is a cafe in the library.',GR),(220,'Does it hold 20,000 books?','Yes, it holds 20,000 books.',PK),(345,'Is the archive on the first floor?','Yes, the archive is on the first floor.',BL)]
for y,q,a,col in qa:
 f.rect(612,y-24,499,48,'#fff1c5','#fff1c5',14,0);f.text(629,y+7,q,23,'A');avatar(f,1142,y)
 avatar(f,452,y+59,True);f.rect(494,y+32,635,52,'#f4f4f4','#f4f4f4',13,0);f.text(509,y+65,a,23,'A',col)
f.rect(20,451,1160,282,'#ffffff','#ff123b',0,2.5,True)
f.text(31,489,'Description Hallucination Examples',27,'C','#ff123b')
sourcecard(f,42,513,360,202,'Source: delivery note',[
 '200 books arrived Monday. Sorting: Tuesday. Cataloguing: Wednesday.'
])
f.rect(610,507,501,48,'#fff1c5','#fff1c5',14,0);f.text(626,539,'Summarize the delivery note.',23,'A');avatar(f,1142,531)
avatar(f,452,603,True);f.rect(494,572,648,143,'#f4f4f4','#f4f4f4',14,0)
f.rich(511,605,['On ',('Tuesday',PK),', the library received ',('500 books',PK),'.'],23,'A')
f.rich(511,639,['The books came ',('from a university',GR),'.'],23,'A')
f.rich(511,674,[('Cataloguing happened before sorting',BL),'.'],23,'A')
f.text(34,764,'Unsupported does not necessarily mean false in the world; the source does not establish it.',22,'T')
FIGS.append(f)

# Fig. 3: explicit citations inside benchmark leaves, with criterion families above them.
f=Drawing('figure_3_evaluation_taxonomy',1400,646,'Figure 3: Taxonomy of evaluation targets and criteria with benchmark references. Gen evaluates generated content; Dis evaluates detectors against human labels. Criteria are not shared protocols; Table 1 gives benchmark-specific details. The same benchmark may support both targets.')
blue='#005477'; pale='#fffafb'
f.rect(18,170,64,280,'white',blue)
f.text(43,310,'LLM hallucination',23,anchor='middle',rotate=-90)
f.text(68,310,'evaluation targets',23,anchor='middle',rotate=-90)
f.line([(82,310),(98,310)]);f.line([(98,156),(98,447)])
for cy in [156,447]:f.line([(98,cy),(116,cy)])
f.box(116,120,265,72,'Generated content (Gen) / §4.1',stroke=blue,size=23)
f.box(116,411,265,72,'Hallucination detectors (Dis) / §4.2',stroke=blue,size=23)
items=[
 (86,140,'World factuality','Truthfulness / factual precision / hallucination rate',[( '2022.acl-long.229','TruthfulQA'),('2024.naacl-long.167','ExpertQA'),('2025.acl-long.71','HALoGEN'),('2025.acl-long.1587','FactBench')]),
 (226,112,'Source faithfulness','Source consistency / supported-claim rate',[( '2024.naacl-long.167','ExpertQA'),('2024.naacl-long.251','TofuEval'),('2025.naacl-short.38','FaithBench')]),
 (374,140,'Response / sentence classification','Accuracy / balanced accuracy / F1',[( '2023.emnlp-main.397','HaluEval'),('2024.acl-long.442','ANAH'),('2024.naacl-long.251','TofuEval'),('2025.naacl-short.38','FaithBench')]),
 (520,96,'Error-span localization','Span precision / recall / F1',[( '2024.acl-long.585','RAGTruth')])]
for cy,ys in [(156,[86,226]),(447,[374,520])]:
 f.line([(381,cy),(399,cy)]);f.line([(399,ys[0]),(399,ys[1])])
for y,h,label,metric,benchmarks in items:
 f.line([(399,y),(417,y)]);f.line([(707,y),(735,y)])
 f.box(417,y-30,290,60,label,stroke=blue,size=23)
 f.rect(735,y-h/2,645,h,pale,blue)
 f.text(746,y-h/2+25,metric,21,'T')
 for j,(pid,name) in enumerate(benchmarks):f.text(746,y-h/2+51+25*j,cite(pid,name),22,'T')
 if label=='Error-span localization':f.text(746,y-h/2+77,'(also response-level classification)',22,'T')
f.rect(116,597,1264,34,'#f5f9fc',blue,6)
f.text(132,620,'Mitigation evaluation: matched settings + Gen/Dis criteria + coverage, refusal, cost and shift tests (§6).',22,'T')
FIGS.append(f)

# Figure 4: five pastel stage columns, causes row and mitigation row.
f=Drawing('figure_4_causes_mitigation',1450,868,'Figure 4: Potential failure sources and representative mitigation methods in text LLMs. Retrieval is optional. Stage associations summarize the literature; they do not establish one-to-one causal effects or guaranteed fixes. Evaluate outcomes using Fig. 3 and Table 1.')
xs=[20,305,590,875,1160]; ww=270
fills=['#d1e9cf','#ffcccc','#d6e7fc','#fff0c4','#f3f3f3'];strokes=['#7ab953','#d9535a','#6995cb','#e3b62d','#777777']
def divider(y,label,color,arrow=False):
 w=tw(label,'AB',24)+20;cx=725
 f.line([(30,y),(cx-w/2-6,y)],'#202020',1.5,True)
 f.line([(cx+w/2+6,y),(1430,y)],'#202020',1.5,True,arrow)
 f.text(cx,y+7,label,24,'AB',color,'middle')
divider(28,'Text LLM generation pipeline','#ff7a00',True)
for x,fill,st in zip(xs,fills,strokes):f.rect(x,50,ww,192,fill,st,12,1.6)
f.text(34,82,'Data & evidence',26,'C');f.paragraph(34,116,'User prompt, supplied source and knowledge corpus',239,23,'A',leading=29)
f.text(440,115,'Retrieval & context',26,'C',anchor='middle');f.text(440,151,'(optional)',23,'C',anchor='middle');f.text(440,185,'evidence selection',22,'A',anchor='middle')
f.text(725,116,'Large language model',25,'C',anchor='middle');f.text(725,157,'pretraining + alignment',22,'C',anchor='middle')
f.text(1010,116,'Decoding',28,'C',anchor='middle');f.text(1010,157,'token selection',23,'C',anchor='middle')
f.text(1174,81,'Response',27,'C');f.text(1174,118,'Claims to evaluate:',22,'AB')
f.text(1174,153,'World factuality',23,'A');f.text(1174,184,'Source faithfulness',23,'A');f.text(1174,218,'(Fig. 3; Table 1)',22,'T')
divider(267,'Potential causes','#ef00d9')
causes=[['Noisy / outdated facts','Biased associations'],['Irrelevant evidence','Knowledge conflicts'],['Knowledge limitations','Weak source grounding'],['Prior dominates context','Uncertainty miscalibration']]
for x,fill,st,labels in zip(xs,fills,strokes,causes):
 for j,label in enumerate(labels):f.box(x,291+j*66,ww,59,label,fill,st,size=22,font='AB',center=True)
# Response is an outcome, not an additional cause; preserve the empty slot.
divider(441,'Mitigation','#008aff')
mit=[
 [('Faithful data',cite('2022.tacl-1.84','FaithDial')),('Factuality alignment',cite('2024.acl-long.107','Self-Alignment')+'\n'+cite('2024.findings-emnlp.955','FactAlign'))],
 [('Adaptive retrieval',cite('ext-selfrag','Self-RAG')),('Resolve conflicts',cite('2025.acl-long.1476','Astute RAG'))],
 [('Representation editing',cite('2024.acl-long.483','TruthX')),('Attention control',cite('2024.emnlp-main.84','Lookback Lens'))],
 [('Contrastive decoding',cite('2024.naacl-short.69','CAD')+'\n'+cite('ext-dola','DoLa')),('Selective generation',cite('2025.acl-long.1199','SEAL'))],
 [('Verify and revise',cite('2024.findings-acl.212','CoVe')+'\n'+cite('ext-critic','CRITIC'))]
]
for x,fill,st,groups in zip(xs,fills,strokes,mit):
 for j,(title,refs) in enumerate(groups):
  y=465+j*133;h=(124 if j==0 else 148) if len(groups)>1 else 281
  f.rect(x,y,ww,h,fill,st,6,1.5);f.paragraph(x+7,y+28,title,ww-14,22,'AB',leading=25);f.paragraph(x+7,y+60,refs,ww-14,22,'T',leading=25)
f.rect(20,767,1410,79,'#f7f7f7','#777777',6,1.2)
f.text(725,789,'Intervention mechanism (§5) -> evaluate outputs under the same protocol (§4) -> compare utility and limits (§6).',22,'T',anchor='middle')
f.text(725,812,'Report factuality and source support together with useful coverage, refusal and cost.',22,'T',anchor='middle')
f.text(725,835,'Metric-validation limits: '+cite('2025.findings-acl.1175','Verify with Caution'),22,'T',anchor='middle')
FIGS.append(f)

# Table 1: faithful three-rule layout with size units and source-verified values.
bench=[
 ('TruthfulQA','2022.acl-long.229','Gen / MC','817 questions','World factuality','Truthfulness; informativeness','Abstract; §2.2','817-question test set; MC is multiple choice, not hallucination detection.'),
 ('HaluEval','2023.emnlp-main.397','Dis','35,000 samples','Mixed-task hallucination','Recognition accuracy','§1; §2','30k task-specific samples plus 5k general user-query responses.'),
 ('ANAH','2024.acl-long.442','Dis','~12k sentences','QA support / contradiction','Type accuracy; F1','Abstract; §3.4; §4.3','About 4.3k responses. Generative and discriminative annotators both perform the Dis task of classifying hallucination labels; decoder architecture does not make this a Gen evaluation.'),
 ('RAGTruth','2024.acl-long.585','Dis','17,790 responses','RAG source faithfulness','Response / span P, R, F1','Table 2; §5.1','Full corpus: 2,965 source instances times 6 generators; not a single held-out split.'),
 ('ExpertQA','2024.naacl-long.167','Gen','2,177 questions','Correctness & attribution','Human factuality / support','Abstract; §3; §4','Questions span 32 fields; factuality and attribution are annotated separately.'),
 ('TofuEval','2024.naacl-long.251','Dis / Gen','1,479 summaries*','Dialogue-summary consistency','Balanced accuracy; error rate','§3.3; §4; §5','Paper reports 1,500 generated and 1,479 retained summaries (3,966 sentences); its text also says 23 removed, an arithmetic inconsistency. Retained count is quoted, not recomputed.'),
 ('HALoGEN','2025.acl-long.71','Gen','10,923 prompts','Domain-specific factuality','Atomic hallucination rate','Abstract; §2','Full nine-domain suite includes programming; survey discussion is limited to text-relevant tasks. No invented text-only count.'),
 ('FaithBench','2025.naacl-short.38','Dis / Gen','750 summaries','Summary source faithfulness','Balanced accuracy; macro F1','§2.4; §3.3','Final 75 source passages times 10 LLMs, selected for detector disagreement; not the earlier 800-sample intermediate set.'),
 ('FactBench','2025.acl-long.1587','Gen','1,000 prompts','Verifiable factual claims','Hallucination score; precision','§1; §4.6; §5.2','The 2025 paper snapshot; a dynamic resource may change. 150 topics.')
]
f=Drawing('table_1_benchmarks',1550,605,'Table 1: Hallucination evaluation benchmarks for text LLMs. Dis: hallucination discrimination; Gen: generated-content evaluation; MC: multiple choice. Size refers to the stated corpus unit, not a common test-set size.')
# Headline above the table, like the reference. The same caption appears in the combined proof PDF.
cols=[(20,408),(428,170),(598,250),(848,339),(1187,343)]
headers=['Benchmark','Evaluation','Size','Hallucination focus','Metrics']
f.line([(20,15),(1530,15)],'#000000',1.7)
for (x,w),head in zip(cols,headers):f.text(x+w/2,50,head,26,anchor='middle')
f.line([(20,69),(1530,69)],'#000000',1.0)
for n,row in enumerate(bench):
 name,pid,ev,size,focus,metric,locator,note=row;y=103+n*48
 vals=[cite(pid,name),ev,size,focus,metric]
 for (x,w),v in zip(cols,vals):
  ls=wrap(v,w-12,'T',23)
  for j,t in enumerate(ls):f.text(x+w/2,y-(len(ls)-1)*12+j*24,t,23,anchor='middle')
f.line([(20,526),(1530,526)],'#000000',1.7)
f.text(20,555,'* Retained count reported in the paper. Dataset sizes count different units; these rows are not a pooled leaderboard.',21)
f.text(20,583,'HALoGEN size is for the complete suite; only text-relevant tasks fall within this survey. Paper snapshots: 2022-2025.',21)
FIGS.append(f)

FIGS.sort(key=lambda d: d.name)
parser=argparse.ArgumentParser()
parser.add_argument('--only',nargs='+',choices=[d.name for d in FIGS],help='Rebuild only selected assets, then refresh the combined review.')
args=parser.parse_args()
captioned=[]
for d in FIGS:
 p=TMP/(d.name+'_captioned.pdf')
 if not args.only or d.name in args.only or not p.exists():p=d.save()
 captioned.append(p)
writer=PdfWriter()
for p in captioned:writer.append(str(p))
writer.add_metadata({'/Title':'Reference-style figures and benchmark table - text LLM hallucination survey','/Author':'Xincheng Li','/Subject':'Four original figures and one table; no manuscript prose'})
with (OUT/'Figures_and_Table_Review.pdf').open('wb') as out:writer.write(out)

# Machine-readable provenance and table data.
with (OUT/'benchmark_table.csv').open('w') as fp:
 w=csv.writer(fp);w.writerow(['benchmark','paper_id','evaluation','size','hallucination_focus','metrics','source_locator','counting_notes'])
 w.writerows(bench)
(OUT/'figure_references.json').write_text(json.dumps([{'id':pid,'title':PAPERS[pid]['title'],'url':PAPERS[pid]['url'],'year':PAPERS[pid]['year']} for pid in sorted(USED)],indent=2,ensure_ascii=False))
(OUT/'layout_checks.json').write_text(json.dumps({'figure_count':4,'table_count':1,'width_mm':160,'figures':[{'name':d.name,'canvas':[d.w,d.h],'minimum_box_font_pt':round(min([x['font_size'] for x in d.label_checks] or [23])*453.5433/d.w,2),'boxes_checked':len(d.label_checks)} for d in FIGS]},indent=2))
(OUT/'asset_manifest.json').write_text(json.dumps([{'name':d.name,'caption':d.caption,'width':d.w,'height':d.h} for d in FIGS],indent=2))
print('Rebuilt',len(args.only) if args.only else len(FIGS),'assets plus the five-page combined review in',OUT)

(OUT/'figure_citation_map.json').write_text(json.dumps(dict(USED_BY_FIG),indent=2,ensure_ascii=False)+'\n')
(OUT/'drawing_operations.json').write_text(json.dumps([{'name':d.name,'width':d.w,'height':d.h,'caption':d.caption,'ops':d.ops} for d in FIGS],ensure_ascii=False,indent=2)+'\n')
