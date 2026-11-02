# Development

## Layout

- `.agents/skills/paper-figure-to-figma/`: repository skill entrypoint.
- `prompts/`: reconstruction contract and review instructions.
- `tools/`: scene validation, SVG rendering, Figma execution bundles and skill packaging.
- `examples/`: attributed reference images, portable scenes and reviewed native exports.
- `demo/`: offline comparison and editing demonstration.
- `web/`: optional prompt builder.

Python 3.10+ runs the core tools. Pillow is needed for image preparation and showcase assets; Node runs the JavaScript checks.

## Checks

```text
python -m unittest discover -s tools -p "test_*.py" -v
node --test tools/test_figma_import.cjs
node --check demo/app.js
node --check web/app.js
python tools/build_demo.py --check
```

The Python and JavaScript tests cover scene contracts, gradients, curves, text, raster boundaries, partial updates, failed-update recovery, portable installation and backups. See [validation scope](entrypoint-validation.md) for live evidence and limits.

## Package

```text
python tools/install_skill.py --package local-outputs/paper-figure-to-figma-0.1.0.zip
```

The ZIP contains one self-contained skill directory, its runtime, MIT license and version. It excludes working outputs and reference-image collections. A fresh installation can render and bundle the included minimal scene from an unrelated working directory.

## Figure execution

```text
python tools/scene_to_svg.py examples/minimal.scene.json local-outputs/example.svg
python tools/bundle_figma.py examples/minimal.scene.json local-outputs/example.figma.js
python tools/prepare_scene.py input.scene.json local-outputs/prepared --reference reference.png
```

Upload allowed RGB assets through the connected Figma tools before executing a bundle. Split large bundles with `--panel` or `--node-range`; continue with the latest returned root ID. Full reimports stage a replacement, while partial imports retain absent nodes. Inspect existing artwork before editing.

## Showcase

`build_demo.py` rebuilds `demo/index.html`; commit it with its template and sources. `build_showcase_assets.py` rebuilds the two example comparison sheets. `make_demo_gif.py` uses slower frame timing and opening/closing holds. The GIF demonstrates the offline editor, not model inference time.
