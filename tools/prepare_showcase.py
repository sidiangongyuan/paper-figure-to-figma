"""Prepare the explicitly selected PlanWAM showcase from the reviewed pilot.

Run once with --pilot pointing to local-outputs/pilot-01. Only curated outputs
are copied; account state, signed export URLs and working files stay local.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from scene_to_svg import validate_scene

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving'
PAPER = 'https://arxiv.org/abs/2610.11382'


def prepare(pilot):
    destination = ROOT / 'examples' / 'planwam'
    destination.mkdir(parents=True,exist_ok=True)
    scene = json.loads((pilot/'review-02/scene-revised.json').read_text(encoding='utf-8'))
    scene.update(projectId='planwam-figure-1',name='PlanWAM · Figure 1',referenceSize={'width':1089,'height':385},
                 sourceNote=TITLE+' — Figure 1; reconstructed with adjusted typography.',
                 attribution={'title':TITLE,'url':PAPER,'figure':'Figure 1','changes':['Editable reconstruction','Times New Roman body text','Enlarged editing canvas','Vector-redrawn car icons']})
    for asset in scene['assets'].values():
        asset['source']=PAPER+' — Figure 1 reference crop'
    validate_scene(scene)
    (destination/'planwam.scene.json').write_text(json.dumps(scene,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    shutil.copyfile(pilot/'reference.png',destination/'reference.png')
    native=ET.parse(pilot/'review-02/figure-editable.svg').getroot()
    ET.register_namespace('','http://www.w3.org/2000/svg')
    # Native export names include punctuation and transport-encoding artifacts.
    # Give every managed object the same stable ID as its portable project.
    nodes={n['id']:n for n in scene['nodes']}
    found=set()
    for element in native.iter():
        # SVG2 href also works when the export is inlined into an HTML document.
        # Arbitrary XML namespace prefixes are not resolved by the HTML parser.
        xlink='{http://www.w3.org/1999/xlink}href'
        if xlink in element.attrib:
            element.set('href',element.attrib.pop(xlink))
        identifier=element.get('id','')
        match=re.match(r'^([a-z][a-z0-9-]+)(?=\s|$)',identifier)
        if match and match.group(1) in nodes:
            key=match.group(1)
            element.set('id',key)
            element.set('data-figure-node',key)
            element.set('data-kind',nodes[key]['type'])
            found.add(key)
        elif identifier.startswith('Pilot '):
            element.set('id','planwam-figure-1')
    missing=set(nodes)-found
    if missing:
        raise ValueError('Native export is missing scene IDs: '+str(sorted(missing)))
    title=ET.Element('{http://www.w3.org/2000/svg}title')
    title.text='Editable reconstruction of '+TITLE+' — Figure 1'
    native.insert(0,title)
    description=ET.Element('{http://www.w3.org/2000/svg}desc')
    description.text='Source: '+PAPER+'. Body typography adjusted to Times New Roman. RGB input/output crops remain images; labels and diagram objects are editable.'
    native.insert(1,description)
    (destination/'reconstruction.svg').write_text(ET.tostring(native,encoding='unicode'),encoding='utf-8',newline='\n')
    counts=Counter(n['type'] for n in scene['nodes'])
    manifest={'title':TITLE,'paperUrl':PAPER,'figure':'Figure 1','referenceSize':scene['referenceSize'],
              'canvas':{'width':scene['width'],'height':scene['height']},'elements':len(nodes),
              'textLayers':counts['text'],'vectorObjects':counts['rect']+counts['svg'],
              'rgbLayers':counts['image'],'distinctRgbAssets':len(scene['assets']),
              'gradients':sum(n['type']=='rect' and isinstance(n.get('fill'),dict) for n in scene['nodes']),
              'minimumEditorFontSize':min(n['size'] for n in scene['nodes'] if n['type']=='text'),
              'nativeExport':True,'notes':scene['issues']}
    (destination/'showcase.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    print(json.dumps(manifest,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot',type=Path,required=True)
    prepare(parser.parse_args().pilot)
