"""Build the self-contained offline product demo from curated real outputs."""
import argparse
import base64
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def build(check=False):
    read=lambda name:(ROOT/name).read_text(encoding='utf-8')
    scene=json.loads(read('examples/planwam/planwam.scene.json'))
    info=json.loads(read('examples/planwam/showcase.json'))
    source='data:image/png;base64,'+base64.b64encode((ROOT/'examples/planwam/reference.png').read_bytes()).decode('ascii')
    packed=json.dumps({'scene':scene,'info':info},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    html=read('demo/index.template.html')
    replacements={'/*__STYLES__*/':read('demo/style.css'),'/*__FIGURE__*/':read('examples/planwam/reconstruction.svg'),
                  '/*__REFERENCE__*/':source,'/*__DATA__*/':'const SHOWCASE='+packed+';',
                  '/*__APP__*/':read('demo/app.js'),'/*__TEXT_COUNT__*/':str(info['textLayers']),
                  '/*__VECTOR_COUNT__*/':str(info['vectorObjects'])}
    for marker,value in replacements.items():
        if marker not in html:raise ValueError('Missing template marker: '+marker)
        html=html.replace(marker,value)
    target=ROOT/'demo/index.html'
    if check:
        if not target.exists() or target.read_text(encoding='utf-8')!=html:raise SystemExit('Demo build is stale: run python tools/build_demo.py')
    else:target.write_text(html,encoding='utf-8',newline='\n')
    print('Offline demo is current' if check else 'Built demo/index.html; open directly in a browser')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
