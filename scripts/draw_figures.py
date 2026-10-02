"""Original vector diagrams. SVG and PDF share the same drawing primitives.
Requires reportlab and pypdfium2. Run from any directory.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import math, xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.colors import toColor as HexColor
import pypdfium2 as pdfium

OUT=Path(__file__).resolve().parents[1]/'figures'
OUT.mkdir(exist_ok=True)
NAVY='#17324d'; BLUE='#2864a0'; TEAL='#187c80'; PURPLE='#765392'; ORANGE='#b96731'; GRAY='#5e6d7c'
class Figure:
 def __init__(self,name,w,h):
  self.name,self.w,self.h=name,w,h
  self.lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', '<style>text {font-family: Helvetica, Arial, sans-serif;}</style>',f'<rect width="{w}" height="{h}" fill="white"/>']
  self.c=canvas.Canvas(str(OUT/(name+'.pdf')),pagesize=(453.543,453.543*h/w))
  self.c.setTitle(name.replace('_',' ')); self.c.setAuthor('Xincheng Li')
  self.c.scale(453.543/w,453.543/w)
 def rect(self,x,y,w,h,fill='white',stroke='#ccd6df',radius=7):
  self.lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
  self.c.setFillColor(HexColor(fill));self.c.setStrokeColor(HexColor(stroke));self.c.setLineWidth(1.5)
  self.c.roundRect(x,self.h-y-h,w,h,radius,fill=1,stroke=1)
 def text(self,x,y,s,size=18,color=NAVY,bold=False,anchor='start'):
  self.lines.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')
  self.c.setFillColor(HexColor(color));self.c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
  method=self.c.drawCentredString if anchor=='middle' else self.c.drawString
  method(x,self.h-y,s)
 def line(self,pts,color='#7c8b98',arrow=False,dash=False):
  coords=' '.join(f'{x},{y}' for x,y in pts)
  self.lines.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="1.6"'+(' stroke-dasharray="5,4"' if dash else '')+'/>')
  self.c.setStrokeColor(HexColor(color));self.c.setLineWidth(1.6);self.c.setDash([5,4] if dash else [])
  p=self.c.beginPath();p.moveTo(pts[0][0],self.h-pts[0][1])
  for x,y in pts[1:]:p.lineTo(x,self.h-y)
  self.c.drawPath(p);self.c.setDash([])
  if arrow:
   x,y=pts[-1];a=math.atan2(y-pts[-2][1],x-pts[-2][0]);q=[(x,y),(x-8*math.cos(a)+4*math.sin(a),y-8*math.sin(a)-4*math.cos(a)),(x-8*math.cos(a)-4*math.sin(a),y-8*math.sin(a)+4*math.cos(a))]
   self.lines.append(f'<polygon points="'+ ' '.join(f'{u},{v}' for u,v in q)+f'" fill="{color}"/>')
   p=self.c.beginPath();p.moveTo(q[0][0],self.h-q[0][1]);p.lineTo(q[1][0],self.h-q[1][1]);p.lineTo(q[2][0],self.h-q[2][1]);p.close();self.c.setFillColor(HexColor(color));self.c.drawPath(p,fill=1,stroke=0)
 def save(self):
  self.lines.append('</svg>');p=OUT/(self.name+'.svg');p.write_text('\n'.join(self.lines));ET.parse(p)
  self.c.showPage();self.c.save()
  d=pdfium.PdfDocument(str(OUT/(self.name+'.pdf')));d[0].render(scale=3).to_pil().save(OUT/(self.name+'.png'))

f=Figure('figure_1_survey_structure',960,540)
f.text(20,30,'The structure of this survey',24,bold=True)
f.rect(20,49,920,39,'#f1f5f8');f.text(37,75,'1  Introduction: scope, motivation, and three review questions',18)
f.line([(200,285),(237,285)]);f.line([(237,133),(237,453)])
rows=[('2  Concepts and taxonomy','Reference frames, failures, and causes',BLUE,'#eff5fc'),('3  Detection methods','Evidence verification, sampling, internals',TEAL,'#edf8f6'),('4  Mitigation methods','Training, retrieval, decoding, revision',PURPLE,'#f5f0f8'),('5  Benchmarks and evaluation','Tasks, annotation, metrics, robustness',ORANGE,'#fcf3ec'),('6  Analysis and future work','Validity, coverage, transfer, and cost',GRAY,'#f1f5f8')]
for i,(a,b,col,fill) in enumerate(rows):
 y=110+i*80
 f.line([(237,y+23),(274,y+23)],col);f.line([(580,y+23),(619,y+23)],col,arrow=True)
 f.rect(274,y,306,47,fill,col);f.text(291,y+29,a,18,col,True)
 f.rect(619,y,321,47,'white',col);f.text(634,y+29,b,16.5)
f.rect(20,247,180,76,'#e9f0f7',NAVY)
f.text(110,279,'Hallucination',21,NAVY,True,'middle');f.text(110,305,'in text LLMs',19,NAVY,False,'middle')
f.rect(20,495,920,30,'#f1f5f8');f.text(37,516,'7  Conclusion    |    References and supplementary evidence follow the seven-page main text',17)
f.save()

f=Figure('figure_2_taxonomy',960,578)
f.text(20,30,'A taxonomy along three independent axes',24,bold=True)
f.text(20,55,'Classify the error, the evidence used to detect it, and the point of intervention.',17,GRAY)
panels=[(20,BLUE,'A  What is the reference?'),(333,TEAL,'B  What evidence is used?'),(646,PURPLE,'C  Where to intervene?')]
for x,col,title in panels:
 f.rect(x,76,294,440,'white','#cbd5df');f.rect(x,76,294,43,col,col);f.text(x+14,104,title,18,'#ffffff',True)
def box(x,y,h,title,lines,col,fill):
 f.rect(x,y,270,h,fill,col);f.text(x+12,y+26,title,18,col,True)
 for k,s in enumerate(lines):f.text(x+12,y+51+k*22,s,16.5)
box(32,137,118,'World factuality',['Incorrect factual claims','Reference: external world','e.g., TruthfulQA; FActScore'],BLUE,'#eff5fc')
box(32,278,118,'Source faithfulness',['Contradicted or unsupported','Reference: supplied evidence','e.g., RAGTruth; FaithBench'],BLUE,'#eff5fc')
f.text(44,431,'These criteria can disagree.',17,BLUE,True)
f.text(44,459,'Unsupported is not always false;',16.5)
f.text(44,481,'source-consistent can be wrong.',16.5)
box(345,137,105,'External / source evidence',['NLI / QA / atomic claims','AlignScore; VeriScore'],TEAL,'#edf8f6')
box(345,259,105,'Sampled-text consistency',['Repeated / cross-model outputs','SelfCheckGPT; semantic entropy'],TEAL,'#edf8f6')
box(345,381,105,'Model-internal signals',['Probabilities / states / attention','FOCUS; Lookback Lens'],TEAL,'#edf8f6')
box(658,132,83,'Training and alignment',['FaithDial; Self-Alignment'],PURPLE,'#f5f0f8')
box(658,225,83,'Retrieval and prompting',['Self-RAG; Astute RAG'],PURPLE,'#f5f0f8')
box(658,318,83,'Decoding and intervention',['CAD; DoLa; TruthX'],PURPLE,'#f5f0f8')
box(658,411,83,'Revision and abstention',['CoVe; CRITIC; SEAL'],PURPLE,'#f5f0f8')
f.text(20,543,'Cross-cutting comparisons: granularity · model access · supervision · cost · coverage · robustness',17,NAVY,True)
f.text(20,568,'Original synthesis. A method may occupy multiple categories; the axes do not assert causal relationships.',16.5,GRAY)
f.save()

f=Figure('figure_3_evidence_loop',960,356)
f.text(20,30,'From detection to a controlled response',24,bold=True)
nodes=[(20,95,175,'Prompt + sources',['Check relevance','and reliability'],BLUE),(240,95,190,'Generate candidate',['Model parameters','+ supplied context'],PURPLE),(475,95,220,'Verify claims',['Source support / truth','Uncertainty / consistency'],TEAL),(740,95,200,'Choose an action',['Keep · retrieve · revise','or abstain'],ORANGE)]
for i in range(3):f.line([(nodes[i][0]+nodes[i][2],147),(nodes[i+1][0],147)],arrow=True)
f.line([(840,201),(840,242),(335,242),(335,201)],ORANGE,True,True)
for x,y,w,title,ls,col in nodes:
 f.rect(x,y,w,106,'#f7f9fb',col);f.text(x+w/2,y+27,title,18,col,True,'middle')
 for k,s in enumerate(ls):f.text(x+w/2,y+54+23*k,s,16.5,NAVY,False,'middle')
f.text(360,234,'Feedback: additional evidence or a revised claim',16.5,ORANGE)
f.rect(20,274,920,60,'#f1f5f8');f.text(38,298,'Evaluate the whole system, not just the detector:',18,NAVY,True)
f.text(38,322,'factuality + source support + useful coverage + refusal + latency + transfer',18)
f.save()
print('Created 3 SVG + 3 PDF + 3 PNG diagrams in',OUT)
