"""Validate a version-1 scene and render SVG without a model API.

This executes a model/human-authored scene. It does not infer a scene from images.
"""
import argparse
from collections import Counter
from html import escape
import json
from pathlib import Path
import math
import xml.etree.ElementTree as ET

ALLOWED = {'rect', 'text', 'svg', 'image'}
RASTER_ROLES = {'input_rgb', 'output_result'}
VECTOR_TAGS = {'svg','g','defs','path','rect','circle','ellipse','line','polyline','polygon',
               'linearGradient','radialGradient','stop','clipPath','mask','title','desc'}


def validate_scene(scene):
    if scene.get('version') != 1:
        raise ValueError('Unsupported scene version')
    for key in ('width','height'):
        if not isinstance(scene.get(key),(int,float)) or not math.isfinite(scene[key]) or scene[key]<=0:
            raise ValueError(f'Invalid canvas {key}')
    ids = set()
    for n in scene['nodes']:
        if n['id'] in ids:
            raise ValueError(f'Duplicate node ID: {n["id"]}')
        ids.add(n['id'])
        if n['type'] not in ALLOWED:
            raise ValueError(f'Unsupported node type: {n["type"]}')
        for key in ('x','y','w','h'):
            if not isinstance(n[key],(int,float)) or not math.isfinite(n[key]):
                raise ValueError(f'Nonfinite geometry: {n["id"]}.{key}')
        if n['w']<=0 or n['h']<=0:
            raise ValueError(f'Nonpositive dimensions: {n["id"]}')
        if n['type']=='image':
            asset=scene['assets'][n['asset']]
            if n.get('role') not in RASTER_ROLES or asset.get('role')!=n['role']:
                raise ValueError(f'Raster outside approved roles: {n["id"]}')
            if asset['mime'] not in {'image/png','image/jpeg'}:
                raise ValueError('Only PNG/JPEG raster assets are allowed')
        if n['type']=='svg':
            root=ET.fromstring(n['svg'])
            for el in root.iter():
                tag=el.tag.split('}')[-1]
                if tag not in VECTOR_TAGS:
                    raise ValueError(f'Unexpected embedded {tag}: {n["id"]}')
                if any('href' in key or key.lower().startswith('on') for key in el.attrib):
                    raise ValueError(f'External reference/event in vector: {n["id"]}')
        if n['type']=='text' and not isinstance(n['text'],str):
            raise ValueError('Text must remain text')
    return {'nodes':len(ids),'types':dict(Counter(n['type'] for n in scene['nodes'])),
            'rasterRoles':dict(Counter(n['role'] for n in scene['nodes'] if n['type']=='image'))}


def attrs(**kw):
    return ' '.join(f'{key.replace("_","-")}="{escape(str(value),quote=True)}"' for key,value in kw.items() if value is not None)


def render_scene(scene):
    validate_scene(scene)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{scene["width"]}" height="{scene["height"]}" viewBox="0 0 {scene["width"]} {scene["height"]}">',
         f'<title>{escape(scene["name"])}</title>',
         f'<rect width="100%" height="100%" fill="{scene.get("background","#ffffff")}"/>']
    current=None
    for n in scene['nodes']:
        if current!=n.get('panel','canvas'):
            if current is not None:
                out.append('</g>')
            current=n.get('panel','canvas')
            out.append(f'<g id="panel-{escape(current)}">')
        common=attrs(id=n['id'],data_name=n['name'])
        x,y,w,h=(n[k] for k in ('x','y','w','h'))
        if n['type']=='rect':
            out.append(f'<rect {common} '+attrs(x=x,y=y,width=w,height=h,rx=n.get('r',0),fill=n.get('fill','none'),stroke=n.get('stroke'),stroke_width=n.get('sw',1),stroke_dasharray=n.get('dash'))+'/>')
        elif n['type']=='text':
            align=n.get('align','center')
            tx=x if align=='left' else x+w if align=='right' else x+w/2
            anchor='start' if align=='left' else 'end' if align=='right' else 'middle'
            ty=y+n['size']*.88
            weight=700 if n.get('weight')=='Bold' else 400
            ta=attrs(x=tx,y=ty,fill=n.get('color','#000000'),font_family=n.get('family','Arial'),font_size=n['size'],font_weight=weight,text_anchor=anchor)
            spans=''.join(f'<tspan x="{tx}" dy="{0 if i==0 else n.get("lineHeight",n["size"]*1.12)}">{escape(line)}</tspan>' for i,line in enumerate(n['text'].split('\n')))
            out.append(f'<text {common} {ta}>{spans}</text>')
        elif n['type']=='image':
            a=scene['assets'][n['asset']]
            out.append(f'<image {common} '+attrs(x=x,y=y,width=w,height=h,preserveAspectRatio='none',data_raster_role=n['role'],href=f'data:{a["mime"]};base64,{a["data"]}')+'/>')
        elif n['type']=='svg':
            sub=ET.fromstring(n['svg'])
            # Use translated groups rather than nested SVG viewports, which
            # some PDF renderers place at the origin instead of honoring x/y.
            sub.tag='{http://www.w3.org/2000/svg}g'
            for key in ('width','height','viewBox','x','y'):
                sub.attrib.pop(key,None)
            sub.set('transform',f'translate({x} {y})'); sub.set('id',n['id'])
            # Namespace every paint server ID so repeated icons remain independent.
            id_map={el.attrib['id']:n['id']+'-'+el.attrib['id'] for el in sub.iter() if 'id' in el.attrib and el is not sub}
            for el in sub.iter():
                for k,v in list(el.attrib.items()):
                    if k=='id' and el is not sub:
                        el.set(k,id_map[v])
                    else:
                        for before,after in id_map.items():
                            v=v.replace('url(#'+before+')','url(#'+after+')')
                        el.set(k,v)
            out.append(ET.tostring(sub,encoding='unicode'))
    if current is not None:
        out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    scene=json.loads(args.scene.read_text(encoding='utf-8'))
    audit=validate_scene(scene)
    args.output.write_text(render_scene(scene),encoding='utf-8')
    print(json.dumps(audit))


if __name__=='__main__':
    main()
