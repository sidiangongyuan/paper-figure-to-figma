"""Search bundled icons and prepare self-contained SVGs for scene nodes (stdlib only)."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / 'assets/icons'
NS = 'http://www.w3.org/2000/svg'
TAGS = {'svg', 'g', 'defs', 'path', 'rect', 'circle', 'ellipse', 'line', 'polyline',
        'polygon', 'linearGradient', 'radialGradient', 'stop', 'clipPath', 'mask', 'title', 'desc'}
PAINT_CSS = {'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin',
             'fill-rule', 'clip-rule', 'opacity', 'fill-opacity', 'stroke-opacity',
             'stop-color', 'stop-opacity'}
ET.register_namespace('', NS)

def catalog():
    return json.loads((LIBRARY / 'catalog.json').read_text(encoding='utf-8'))

def search(query):
    terms = query.casefold().split()
    return [item for item in catalog()['icons']
            if all(t in (item['id'] + ' ' + ' '.join(item['keywords'])).casefold() for t in terms)]

def normalize_svg(source, color='#33464d', stroke_width=None):
    """Reject unsupported content; resolve presentation styles and currentColor explicitly."""
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise ValueError('Color must be a six-digit hex value')
    if stroke_width is not None and (not math.isfinite(stroke_width) or stroke_width <= 0):
        raise ValueError('Stroke width must be positive and finite')
    if re.search(r'<!DOCTYPE|<!ENTITY', source, re.I):
        raise ValueError('DTD and entities are unsupported')
    tree = ET.fromstring(source)
    if tree.tag.split('}')[-1] != 'svg':
        raise ValueError('Expected an SVG root')
    vb = [float(v) for v in re.split(r'[\s,]+', tree.get('viewBox', '').strip()) if v]
    if len(vb) != 4 or not all(map(math.isfinite, vb)) or vb[2] <= 0 or vb[3] <= 0:
        raise ValueError('A finite viewBox with positive width and height is required')
    ids = set()
    for node in tree.iter():
        tag = node.tag.split('}')[-1]
        if tag not in TAGS:
            raise ValueError('Unsupported SVG element: ' + tag)
        node.tag = '{' + NS + '}' + tag
        if node.get('id'):
            if node.get('id') in ids:
                raise ValueError('Duplicate SVG id')
            ids.add(node.get('id'))
        for key in list(node.attrib):
            local = key.split('}')[-1]
            if local.lower().startswith('on') or 'href' in local.lower():
                raise ValueError('External references and event handlers are unsupported')
        style = node.attrib.pop('style', '')
        for statement in filter(str.strip, style.split(';')):
            key, sep, value = statement.partition(':')
            key, value = key.strip(), value.strip()
            if not sep:
                raise ValueError('Malformed SVG style')
            if key in PAINT_CSS:
                node.set(key, value)
            elif node is tree and key in {'flex', 'line-height', 'display', 'vertical-align', 'enable-background'}:
                pass  # Host layout and legacy filter-buffer hints have no effect in this filter-free subset.
            else:
                raise ValueError('Unsupported SVG CSS: ' + key)
        node.attrib.pop('class', None)
        for key, value in list(node.attrib.items()):
            if re.search(r'url\(\s*[^#]', value, re.I) or re.search(r'var\(|expression\(', value, re.I):
                raise ValueError('SVG must not depend on external CSS or URLs')
            node.set(key, re.sub('currentColor', color, value, flags=re.I))
    prefix = 'i' + hashlib.sha256((source + color + str(stroke_width)).encode()).hexdigest()[:12] + '-'
    for node in tree.iter():
        if node.get('id'):
            node.set('id', prefix + node.get('id'))
        for key, value in list(node.attrib.items()):
            for target in re.findall(r'url\(#([^)]*)\)', value):
                if target not in ids:
                    raise ValueError('Unresolved local SVG reference: ' + target)
                value = value.replace('url(#' + target + ')', 'url(#' + prefix + target + ')')
            node.set(key, value)
    tree.attrib.pop('width', None)
    tree.attrib.pop('height', None)
    if stroke_width is not None:
        # Only changes an existing stroke; multi-color filled artwork stays intact.
        for node in tree.iter():
            if 'stroke-width' in node.attrib:
                node.set('stroke-width', str(stroke_width))
    return ET.tostring(tree, encoding='unicode')

def prepare(icon_id=None, svg_path=None, color='#33464d', stroke_width=None, online=False,
            source_url=None, license_name=None):
    if bool(icon_id) == bool(svg_path):
        raise ValueError('Choose one bundled icon ID or local SVG file')
    if svg_path:
        data = Path(svg_path).read_bytes()
        provenance = {'method': 'provided-svg', 'source': source_url or Path(svg_path).name,
                      'license': license_name or 'unspecified; retain original asset terms'}
    else:
        entries = {i['id']: i for i in catalog()['icons']}
        if icon_id in entries:
            provenance = dict(entries[icon_id])
            data = (LIBRARY / provenance['path']).read_bytes()
            if hashlib.sha256(data).hexdigest() != provenance['sha256']:
                raise ValueError('Bundled icon differs from its recorded source')
        elif online:
            provider, sep, name = icon_id.partition(':')
            providers = catalog()['providers']
            if not sep or provider not in providers or not re.fullmatch('[a-z0-9][a-z0-9-]*', name):
                raise ValueError('Unsupported provider or icon name')
            p = providers[provider]
            url = f"https://raw.githubusercontent.com/{p['repository']}/{p['revision']}/{p['directory']}/{name}.svg"
            with urllib.request.urlopen(url, timeout=20) as response:
                data = response.read(2_000_001)
            if len(data) > 2_000_000:
                raise ValueError('Icon exceeds 2 MB')
            provenance = {'id': icon_id, 'source': url, 'revision': p['revision'], 'license': p['license']}
        else:
            raise ValueError('Icon is not bundled; search the catalog, supply --svg, or use --online')
        provenance['method'] = 'library-svg'
    result = normalize_svg(data.decode('utf-8-sig'), color, stroke_width)
    provenance.update(sourceSha256=hashlib.sha256(data).hexdigest(),
                      outputSha256=hashlib.sha256(result.encode()).hexdigest(),
                      color=color, strokeWidth=stroke_width)
    return result, provenance

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('search'); s.add_argument('query')
    s = sub.add_parser('prepare')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--icon'); g.add_argument('--svg', type=Path)
    s.add_argument('--color', default='#33464d'); s.add_argument('--stroke-width', type=float)
    s.add_argument('--online', action='store_true'); s.add_argument('--source'); s.add_argument('--license')
    s.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.command == 'search':
        print(json.dumps(search(args.query), ensure_ascii=True, indent=2)); return
    svg, info = prepare(args.icon, args.svg, args.color, args.stroke_width,
                        args.online, args.source, args.license)
    if args.output.exists() or args.output.with_suffix('.source.json').exists():
        raise FileExistsError('Choose a new output path; existing assets are retained')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding='utf-8')
    args.output.with_suffix('.source.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'svg': str(args.output), 'source': info['source']}, ensure_ascii=True))

if __name__ == '__main__':
    main()
