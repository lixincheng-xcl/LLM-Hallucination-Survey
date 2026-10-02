"""Rebuild the four diagrams as native mxGraph text, shapes and connectors.

Staging files are subsequently opened, saved and previewed in draw.io desktop.
No raster/SVG images are embedded. Native text runs preserve citation italics.
"""
from pathlib import Path
import json, math, html, xml.etree.ElementTree as ET
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT.parent/'tmp/drawio_staging'; STAGE.mkdir(exist_ok=True)
OUT=ROOT/'figures/drawio'; OUT.mkdir(exist_ok=True)
families={'T':('Times New Roman','normal','normal'),'TI':('Times New Roman','normal','italic'),
 'TB':('Times New Roman','bold','normal'),'A':('Arial','normal','normal'),
 'AB':('Arial','bold','normal'),'C':('Comic Sans MS','normal','normal'),'CB':('Comic Sans MS','bold','normal')}
files={'T':'Times New Roman.ttf','TI':'Times New Roman Italic.ttf','TB':'Times New Roman Bold.ttf',
 'A':'Arial.ttf','AB':'Arial Bold.ttf','C':'Comic Sans MS.ttf','CB':'Comic Sans MS Bold.ttf'}
for f,path in files.items():pdfmetrics.registerFont(TTFont(f,'/System/Library/Fonts/Supplemental/'+path))
def tw(t,f,s):return pdfmetrics.stringWidth(t,f,s)
def val(x):return f'{x:.3f}'.rstrip('0').rstrip('.') if isinstance(x,float) else str(x)
def geometry(cell,x,y,w,h):
 return ET.SubElement(cell,'mxGeometry',{'x':val(x),'y':val(y),'width':val(w),'height':val(h),'as':'geometry'})
manifest=[]
for fig in json.loads((ROOT/'figures/reference_style/drawing_operations.json').read_text()):
 if not fig['name'].startswith('figure_'):continue
 number=fig['name'].split('_')[1]
 doc=ET.Element('mxfile',{'host':'Electron','agent':'Native diagram reconstruction','version':'29.0.0'})
 diagram=ET.SubElement(doc,'diagram',{'name':f'Fig{number} - editable','id':fig['name']})
 model=ET.SubElement(diagram,'mxGraphModel',{'dx':'1600','dy':'1000','grid':'0','gridSize':'10','guides':'1',
  'tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'0','pageScale':'1',
  'pageWidth':str(fig['width']),'pageHeight':str(fig['height']),'math':'0','shadow':'0','background':'#ffffff'})
 root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',{'id':'0'});ET.SubElement(root,'mxCell',{'id':'1','parent':'0','value':f'Fig{number} native objects'})
 idx=0; rectangles=[]; textboxes=[]; ops=fig['ops']; i=0
 def cell(style,value='',edge=False):
  global idx
  idx+=1
  return ET.SubElement(root,'mxCell',{'id':f'c{idx}','parent':'1','style':style,'value':value,'edge' if edge else 'vertex':'1'})
 while i<len(ops):
  kind,a=ops[i];i+=1
  if kind=='rect':
   x,y,w,h,fill,stroke,r,lw,dash=a
   c=cell(f'rounded={int(bool(r))};absoluteArcSize=1;arcSize={2*r};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke if lw else "none"};strokeWidth={lw};dashed={int(dash)};dashPattern=7 5;')
   geometry(c,x,y,w,h);rectangles.append((c,x,y,w,h))
  elif kind=='circle':
   x,y,r,fill,stroke,lw=a
   c=cell(f'ellipse;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={lw};');geometry(c,x-r,y-r,2*r,2*r)
  elif kind=='line':
   pts,col,lw,dash,arrow=a
   if len(set(tuple(p) for p in pts))<2:continue
   c=cell(f'edgeStyle=none;html=1;rounded=0;endArrow={"block" if arrow else "none"};endSize=11;strokeColor={col};strokeWidth={lw};dashed={int(dash)};dashPattern=6 4;',edge=True)
   g=ET.SubElement(c,'mxGeometry',{'relative':'1','as':'geometry'})
   ET.SubElement(g,'mxPoint',{'x':val(pts[0][0]),'y':val(pts[0][1]),'as':'sourcePoint'})
   ET.SubElement(g,'mxPoint',{'x':val(pts[-1][0]),'y':val(pts[-1][1]),'as':'targetPoint'})
   if len(pts)>2:
    arr=ET.SubElement(g,'Array',{'as':'points'})
    for px,py in pts[1:-1]:ET.SubElement(arr,'mxPoint',{'x':val(px),'y':val(py)})
  elif kind=='text':
   x,y,s,size,font,col,anchor,rot=a
   runs=[(s,font,col)];width=tw(s,font,size)
   if not rot and anchor=='start':
    while i<len(ops) and ops[i][0]=='text':
     b=ops[i][1]
     if b[1]!=y or b[3]!=size or b[6]!='start' or b[7] or abs(b[0]-(x+width))>.1:break
     runs.append((b[2],b[4],b[5]));width+=tw(b[2],b[4],size);i+=1
   family=families[font][0]
   label='<div style="white-space:nowrap;line-height:1;">'+''.join(
    f'<span style="font-family:{families[ft][0]};font-weight:{families[ft][1]};font-style:{families[ft][2]};color:{co};">{html.escape(t)}</span>' for t,ft,co in runs)+'</div>'
   w=width+4;h=size*1.16
   xx=x if anchor=='start' else x-width/2 if anchor=='middle' else x-width
   yy=y-size*.90
   if rot:
    dx=(xx+w/2)-x;dy=(yy+h/2)-y;theta=math.radians(rot)
    cx=x+dx*math.cos(theta)-dy*math.sin(theta);cy=y+dx*math.sin(theta)+dy*math.cos(theta)
    xx=cx-w/2;yy=cy-h/2
   c=cell(f'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=nowrap;overflow=visible;spacing=0;fontFamily={family};fontSize={size};fontColor={col};rotation={rot};',label)
   geometry(c,xx,yy,w,h)
   if not rot:textboxes.append((c,xx,yy,w,h))
 # Group a labelled rectangle with its own text. This preserves easy node movement.
 assigned={};grouped=0
 for tc,tx,ty,twid,th in textboxes:
  candidates=[r for r in rectangles if r[1]-.5<=tx and r[2]-.5<=ty and tx+twid<=r[1]+r[3]+6 and ty+th<=r[2]+r[4]+2]
  if candidates:
   rec=min(candidates,key=lambda r:r[3]*r[4]);assigned.setdefault(rec[0].get('id'),[]).append(tc)
 for rc,rx,ry,rw,rh in rectangles:
  children=assigned.get(rc.get('id'),[])
  if not children:continue
  group=cell('group;');gid=group.get('id');geometry(group,rx,ry,rw,rh);grouped+=1
  # Insert group immediately before its rectangle to retain SVG-like z-order.
  root.remove(group);root.insert(list(root).index(rc),group)
  for child in [rc]+children:
   child.set('parent',gid);g=child.find('mxGeometry');g.set('x',val(float(g.get('x','0'))-rx));g.set('y',val(float(g.get('y','0'))-ry))
  # Keep all children adjacent to the parent, in their drawing order.
  for child in [rc]+children:root.remove(child)
  at=list(root).index(group)+1
  for child in [rc]+children:root.insert(at,child);at+=1
 name=f'Fig{number}_{fig["name"].split("_",2)[2]}.drawio'
 ET.indent(doc);p=STAGE/name;ET.ElementTree(doc).write(p,encoding='utf-8',xml_declaration=True)
 cells=root.findall('mxCell');manifest.append({'file':name,'stage':str(p),'output':str(OUT/name),
  'vertices':sum(c.get('vertex')=='1' for c in cells),'edges':sum(c.get('edge')=='1' for c in cells),
  'text_cells':sum(bool(c.get('value')) and c.get('vertex')=='1' for c in cells),'node_groups':grouped,
  'embedded_images':0,'source_asset':fig['name'],'width':fig['width'],'height':fig['height']})
(STAGE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
