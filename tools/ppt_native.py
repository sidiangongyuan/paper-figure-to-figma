"""Render a figure scene with native PowerPoint text/geometry and independent SVG artwork.

Windows renderer. Requires installed PowerPoint and pywin32. Never modifies
other open decks or closes the PowerPoint application. Outputs must be new paths.
"""
from pathlib import Path
import argparse,base64,json,math,re,tempfile,zipfile
import xml.etree.ElementTree as ET

NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
for prefix,uri in NS.items():ET.register_namespace(prefix,uri)
def q(name):prefix,local=name.split(':');return '{'+NS[prefix]+'}'+local
def element(parent,name,**attrs):return ET.SubElement(parent,q(name),{k:str(v) for k,v in attrs.items()})
def rgb(color):
 color={'black':'#000000','white':'#ffffff'}.get(color,color)
 if not re.fullmatch(r'#[0-9a-fA-F]{6}',color):raise ValueError('Unsupported color: '+str(color))
 r,g,b=(int(color[i:i+2],16) for i in (1,3,5));return r+256*g+65536*b
def color_hex(color):
 rgb(color)
 return {'black':'000000','white':'FFFFFF'}.get(color,color.lstrip('#').upper())

def native_svg_shape(pic,node,scale):
 svg=ET.fromstring(node['svg']);children=list(svg)
 if len(children)!=1 or children[0].tag.split('}')[-1]!='path':raise ValueError('Native geometry needs one flat path: '+node['id'])
 path=children[0]
 if 'transform' in path.attrib or 'transform' in svg.attrib:raise ValueError('Bake native path transforms first: '+node['id'])
 vx,vy,vw,vh=map(float,svg.get('viewBox').split())
 if not all(math.isfinite(v) for v in (vx,vy,vw,vh)) or vw<=0 or vh<=0:raise ValueError('Invalid native path viewBox: '+node['id'])
 fill=path.get('fill','#000000');stroke=path.get('stroke','none');sw=float(path.get('stroke-width',1))
 sp=ET.Element(q('p:sp'));nv=element(sp,'p:nvSpPr');nv.append(ET.fromstring(ET.tostring(pic.find('p:nvPicPr/p:cNvPr',NS))))
 element(nv,'p:cNvSpPr');element(nv,'p:nvPr');pr=element(sp,'p:spPr');pr.append(ET.fromstring(ET.tostring(pic.find('p:spPr/a:xfrm',NS))))
 cg=element(pr,'a:custGeom')
 for name in ['a:avLst','a:gdLst','a:ahLst','a:cxnLst']:element(cg,name)
 element(cg,'a:rect',l=0,t=0,r='r',b='b');paths=element(cg,'a:pathLst')
 ap=element(paths,'a:path',w=max(1,round(vw*1000)),h=max(1,round(vh*1000)),fill='none' if fill=='none' else 'norm',stroke='false' if stroke=='none' else 'true',extrusionOk='false')
 tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?',path.get('d',''));j=0
 while j<len(tokens):
  op=tokens[j];j+=1
  if op=='Z':element(ap,'a:close');continue
  if op not in ['M','L','C']:raise ValueError('Use absolute M/L/C/Z for native paths: '+node['id'])
  amount={'M':2,'L':2,'C':6}[op];values=list(map(float,tokens[j:j+amount]));j+=amount
  if len(values)!=amount or not all(math.isfinite(v) for v in values):raise ValueError('Incomplete or invalid native path: '+node['id'])
  command=element(ap,{'M':'a:moveTo','L':'a:lnTo','C':'a:cubicBezTo'}[op])
  for i in range(0,amount,2):element(command,'a:pt',x=round((values[i]-vx)*1000),y=round((values[i+1]-vy)*1000))
 if fill=='none':element(pr,'a:noFill')
 else:
  f=element(pr,'a:solidFill');c=element(f,'a:srgbClr',val=color_hex(fill))
  opacity=float(path.get('fill-opacity',1))*float(path.get('opacity',1))*node.get('opacity',1)
  if opacity<1:element(c,'a:alpha',val=round(opacity*100000))
 ln=element(pr,'a:ln',w=round(sw*node['w']/vw*scale*12700),cap='rnd' if path.get('stroke-linecap')=='round' else 'flat')
 if stroke=='none':element(ln,'a:noFill')
 else:
  f=element(ln,'a:solidFill');c=element(f,'a:srgbClr',val=color_hex(stroke))
  opacity=float(path.get('stroke-opacity',1))*float(path.get('opacity',1))*node.get('opacity',1)
  if opacity<1:element(c,'a:alpha',val=round(opacity*100000))
  if path.get('stroke-dasharray'):element(ln,'a:prstDash',val='dash')
  element(ln,'a:round')
 return sp

def render(scene,output):
 from scene_to_svg import validate_scene
 validate_scene(scene)
 output=Path(output).resolve();preview=output.with_suffix('.png');report=output.with_suffix('.report.json')
 if any(p.exists() for p in [output,preview,report]):raise FileExistsError('Choose a new output filename')
 scale=float(scene.get('ppt',{}).get('pointsPerUnit',1))
 if not math.isfinite(scale) or scale<=0:raise ValueError('Invalid ppt.pointsPerUnit')
 width=scene['width']*scale;height=scene['height']*scale
 if max(width,height)>4032:raise ValueError('PowerPoint slide dimension exceeds 56 inches')
 minimum=float(scene.get('ppt',{}).get('minFontSize',16))
 if not math.isfinite(minimum) or minimum<=0:raise ValueError('Invalid ppt.minFontSize')
 for n in scene['nodes']:
  if n['type']=='text':
   sizes=[n['size']]+[r.get('size',n['size']) for r in n.get('runs',[])]
   if min(sizes)*scale<minimum-.001:raise ValueError('PPT font below minimum after unit conversion: '+n['id'])
 try:import win32com.client
 except ImportError as exc:raise RuntimeError('PPT output requires Windows, installed PowerPoint and pywin32 in the current Python environment') from exc
 output.parent.mkdir(parents=True,exist_ok=True);app=win32com.client.Dispatch('PowerPoint.Application');deck=None
 with tempfile.TemporaryDirectory(prefix='ppt-build-',dir=output.parent) as temp:
  build=Path(temp)
  try:
   deck=app.Presentations.Add(False);deck.PageSetup.SlideWidth=width;deck.PageSetup.SlideHeight=height;slide=deck.Slides.Add(1,12)
   slide.FollowMasterBackground=False;slide.Background.Fill.ForeColor.RGB=rgb(scene.get('background','#ffffff'))
   byid={n['id']:n for n in scene['nodes']}
   for index,n in enumerate(scene['nodes']):
    x,y,w,h=[n[k]*scale for k in ['x','y','w','h']]
    if n['type']=='text':
     sh=slide.Shapes.AddTextbox(1,x,y,w,h);tf=sh.TextFrame2
     tf.MarginLeft=tf.MarginRight=tf.MarginTop=tf.MarginBottom=0;tf.WordWrap=0;tf.AutoSize=0;tf.VerticalAnchor=1
     tr=tf.TextRange;tr.Text=n['text'];tr.Font.Name=n.get('family','Times New Roman');tr.Font.Size=n['size']*scale
     tr.Font.Bold=-1 if 'Bold' in n.get('weight','Regular') else 0;tr.Font.Italic=-1 if 'Italic' in n.get('weight','Regular') else 0
     tr.Font.Fill.ForeColor.RGB=rgb(n.get('color','#000000'));tr.ParagraphFormat.SpaceBefore=0;tr.ParagraphFormat.SpaceAfter=0
     tr.ParagraphFormat.Alignment={'left':1,'center':2,'right':3}[n.get('align','left')]
     tr.ParagraphFormat.LineRuleWithin=0;tr.ParagraphFormat.SpaceWithin=n.get('lineHeight',n['size']*1.15)*scale
     for run in n.get('runs',[]):
      sr=win32com.client.Dispatch(tr._oleobj_.Invoke(tr._oleobj_.GetIDsOfNames('Characters'),0,2,True,run['start']+1,run['length']));sr.Font.BaselineOffset=run.get('baseline',0)
      if 'size' in run:sr.Font.Size=run['size']*scale
      if 'italic' in run:sr.Font.Italic=-1 if run['italic'] else 0
      if 'bold' in run:sr.Font.Bold=-1 if run['bold'] else 0
     sh.Width=w;sh.Height=h
     if 'angle' in n:
      cx,cy=[v*scale for v in n.get('center',[n['x']+n['w']/2,n['y']+n['h']/2])];sh.Left=cx-w/2;sh.Top=cy-h/2;sh.Rotation=n['angle']%360
    elif n['type']=='rect':
     sh=slide.Shapes.AddShape(5 if n.get('r') else 1,x,y,w,h)
     if n.get('fill','none')=='none':sh.Fill.Visible=0
     else:sh.Fill.ForeColor.RGB=rgb(n['fill']);sh.Fill.Transparency=1-n.get('opacity',1)
     if n.get('stroke','none')=='none':sh.Line.Visible=0
     else:
      sh.Line.ForeColor.RGB=rgb(n['stroke']);sh.Line.Weight=n.get('sw',1)*scale
      if n.get('dash'):sh.Line.DashStyle=4
     if n.get('r'):sh.Adjustments._oleobj_.Invoke(sh.Adjustments._oleobj_.GetIDsOfNames('Item'),0,4,0,1,min(.5,n['r']*scale/min(w,h)))
    elif n['type']=='svg':
     svg=ET.fromstring(n['svg']);svg.set('width',str(w));svg.set('height',str(h));path=build/f'asset-{index}.svg';ET.ElementTree(svg).write(path,encoding='utf-8',xml_declaration=True)
     sh=slide.Shapes.AddPicture(str(path),False,True,x,y,w,h)
    elif n['type']=='image':
     asset=scene['assets'][n['asset']]
     if 'data' not in asset:raise ValueError('Resolve photo assets with prepare_scene before rendering')
     path=build/f'photo-{index}.png';path.write_bytes(base64.b64decode(asset['data']));sh=slide.Shapes.AddPicture(str(path),False,True,x,y,w,h)
    else:raise ValueError('Unsupported node '+n['id'])
    sh.Name=n['id'];sh.AlternativeText=n.get('name',n['id'])
    if index%40==0:print(f'Created {index+1}/{len(scene["nodes"])} objects',flush=True)
   slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text=scene.get('notes','Reconstructed from user-supplied reference. Native text/regular shapes; independent SVG illustrations. Original figure rights retained.')
   draft=build/'draft.pptx';deck.SaveAs(str(draft),24);deck.Close();deck=None
   with zipfile.ZipFile(draft) as z:files={name:z.read(name) for name in z.namelist()}
   root=ET.fromstring(files['ppt/slides/slide1.xml']);tree=root.find('.//p:spTree',NS)
   for node in list(tree):
    props=node.find('p:nvPicPr/p:cNvPr',NS) if node.tag==q('p:pic') else node.find('p:nvSpPr/p:cNvPr',NS)
    if props is None:continue
    n=byid.get(props.get('name'))
    if not n:continue
    if n['type']=='svg' and n.get('pptNative'):
     sp=native_svg_shape(node,n,scale);i=list(tree).index(node);tree.remove(node);tree.insert(i,sp)
    elif n['type']=='text':
     w=n['w']*scale;h=n['h']*scale;x=n['x']*scale;y=n['y']*scale
     if 'angle' in n:
      cx,cy=[v*scale for v in n.get('center',[n['x']+n['w']/2,n['y']+n['h']/2])];x=cx-w/2;y=cy-h/2
     xf=node.find('p:spPr/a:xfrm',NS);xf.find('a:off',NS).attrib.update(x=str(round(x*12700)),y=str(round(y*12700)));xf.find('a:ext',NS).attrib.update(cx=str(round(w*12700)),cy=str(round(h*12700)))
     bp=node.find('p:txBody/a:bodyPr',NS);bp.set('wrap','none')
     for item in list(bp):
      if item.tag in [q('a:spAutoFit'),q('a:normAutofit'),q('a:noAutofit')]:bp.remove(item)
     element(bp,'a:noAutofit')
   files['ppt/slides/slide1.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
   candidate=build/'candidate.pptx'
   with zipfile.ZipFile(candidate,'w',zipfile.ZIP_DEFLATED) as z:
    for name,data in files.items():z.writestr(name,data)
   deck=app.Presentations.Open(str(candidate),False,False,False);slide=deck.Slides(1)
   texts=[]
   for i in range(1,slide.Shapes.Count+1):
    sh=slide.Shapes(i);n=byid.get(sh.Name,{})
    if n.get('type')!='text':continue
    tr=sh.TextFrame2.TextRange;texts.append({'id':sh.Name,'font':tr.Font.Name,'size':tr.Font.Size,'width':sh.Width,'height':sh.Height,'textWidth':tr.BoundWidth,'textHeight':tr.BoundHeight,'rotated':bool(n.get('angle'))})
   probe=next((n for n in scene['nodes'] if n['type']=='text' and not n.get('runs') and not n.get('angle')),None)
   edit_verified=None
   if probe:
    tb=slide.Shapes(probe['id']);original=tb.TextFrame2.TextRange.Text
    before=[tb.Left,tb.Top,tb.Width,tb.Height,tb.TextFrame2.TextRange.Font.Size];tb.TextFrame2.TextRange.Text=original+' test';after=[tb.Left,tb.Top,tb.Width,tb.Height,tb.TextFrame2.TextRange.Font.Size];tb.TextFrame2.TextRange.Text=original
    if before!=after:raise RuntimeError('Text edit changed geometry')
    edit_verified=True
   deck.SaveAs(str(output),24);deck.Close();deck=None
   deck=app.Presentations.Open(str(output),True,False,False);slide=deck.Slides(1)
   rw=round(min(2400,scene['width']));rh=round(rw*height/width);slide.Export(str(preview),'PNG',rw,rh)
   result={'pptx':str(output),'preview':str(preview),'objects':slide.Shapes.Count,'nativeText':len(texts),'nativeGeometry':sum(n['type']=='rect' or n.get('pptNative',False) for n in scene['nodes']),'svgObjects':sum(n['type']=='svg' and not n.get('pptNative') for n in scene['nodes']),'textEditPreservedGeometry':edit_verified,'saveReopenPassed':True,'textMetrics':texts,'visualReview':'pending'}
   report.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='textMetrics'}),flush=True)
   return result
  finally:
   if deck is not None:deck.Saved=True;deck.Close()

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('scene',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
 render(json.loads(args.scene.read_text(encoding='utf-8')),args.output)
