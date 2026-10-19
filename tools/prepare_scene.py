"""Resolve approved RGB crops locally and prepare image files for MCP uploads.

Pillow is needed only when --reference or --asset replaces an image.
"""
import argparse
import base64
import io
import json
from pathlib import Path
from scene_to_svg import validate_scene


def prepare(scene, output_dir, reference=None, replacements=None):
    validate_scene(scene)
    output_dir.mkdir(parents=True,exist_ok=True)
    replacements = replacements or {}
    opened = None
    manifest = {}
    for index, key in enumerate(dict.fromkeys(n['asset'] for n in scene['nodes'] if n['type']=='image')):
        asset = scene['assets'][key]
        if key in replacements or 'data' not in asset:
            try:
                from PIL import Image
            except ImportError as error:
                raise ValueError('Resolving crops requires Pillow: python -m pip install Pillow') from error
            if key in replacements:
                image = Image.open(replacements[key]).convert('RGB')
            else:
                if reference is None:
                    raise ValueError('Missing --reference for crop: '+key)
                if opened is None:
                    opened = Image.open(reference).convert('RGB')
                if scene.get('referenceSize') != {'width':opened.width,'height':opened.height}:
                    raise ValueError('referenceSize does not match original reference pixels')
                left,top,right,bottom = asset['crop']
                if right>opened.width or bottom>opened.height:
                    raise ValueError('Crop exceeds the reference bounds: '+key)
                image = opened.crop(tuple(round(v) for v in (left,top,right,bottom)))
            buffer = io.BytesIO()
            image.save(buffer,format='PNG')
            asset.update(mime='image/png',data=base64.b64encode(buffer.getvalue()).decode('ascii'))
        ext = '.png' if asset['mime']=='image/png' else '.jpg'
        # Never use model-supplied asset IDs as filesystem paths.
        path = output_dir / f'asset-{index:03d}{ext}'
        path.write_bytes(base64.b64decode(asset['data'],validate=True))
        manifest[key] = str(path.resolve())
    validate_scene(scene)
    (output_dir/'scene.resolved.json').write_text(json.dumps(scene,ensure_ascii=False,indent=2),encoding='utf-8')
    (output_dir/'asset-files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene',type=Path)
    parser.add_argument('output_dir',type=Path)
    parser.add_argument('--reference',type=Path)
    parser.add_argument('--asset',action='append',default=[],metavar='ID=PATH',help='Use an original dataset RGB/output image instead of a crop')
    args = parser.parse_args()
    replacements = {}
    for item in args.asset:
        key,separator,value = item.partition('=')
        if not separator:
            parser.error('--asset must be ID=PATH')
        replacements[key] = Path(value)
    scene = json.loads(args.scene.read_text(encoding='utf-8-sig'))
    print(json.dumps(prepare(scene,args.output_dir,args.reference,replacements),ensure_ascii=False))
