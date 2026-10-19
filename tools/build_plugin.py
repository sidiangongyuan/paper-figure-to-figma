"""Build the dependency-free plugin; end users use the committed built files."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(check=False):
    read = lambda name: (ROOT / name).read_text(encoding='utf-8')
    code = '\n'.join(read(p) for p in ('tools/scene_validate.js','tools/figma_import.js','figma-plugin/controller.js'))
    # Escape '<' so model instructions/SVG examples cannot terminate a script tag.
    packed = json.dumps({'build':read('prompts/01-reconstruct.md'),'review':read('prompts/02-review.md'),
                         'example':json.loads(read('examples/minimal.scene.json'))},ensure_ascii=False).replace('<','\\u003c')
    ui = read('figma-plugin/ui.template.html').replace('/*__PACK__*/', 'const PACK = '+packed+';').replace('/*__VALIDATOR__*/',read('tools/scene_validate.js'))
    for name, content in [('code.js',code),('ui.html',ui)]:
        path = ROOT / 'figma-plugin' / name
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                raise SystemExit('Stale plugin build: '+str(path))
        else:
            path.write_text(content,encoding='utf-8',newline='\n')
    print('Plugin build is current' if check else 'Built plugin: figma-plugin/manifest.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
