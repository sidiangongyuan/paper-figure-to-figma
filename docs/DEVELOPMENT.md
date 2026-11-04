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

The Python and JavaScript tests cover scene contracts, gradients, curves, text, raster boundaries, partial updates, failed-update recovery, portable installation and backups. Tests and node counts check execution correctness; visual fidelity is assessed through the whole-figure and detail review in [prompts/02-review.md](../prompts/02-review.md).

## Package

```text
python tools/install_skill.py --package local-outputs/paper-figure-to-figma-0.2.0.zip
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

## Vector assets

The installed runtime includes `assets/icons/`, its catalog and upstream licenses. `icon_assets.py search frozen` searches offline; `prepare --icon lucide:snowflake --output local-outputs/frozen.svg` produces a self-contained SVG and provenance record. `--online` retrieves other named icons from pinned official sources. Supplied SVGs use `--svg`. See [asset workflow](../prompts/03-vector-assets.md).

`trace_icon.py` uses optional Pillow and VTracer 0.6.15. Install them in a task environment when tracing is needed. Oversized results may be optimized with an available SVG optimizer, then normalized and visually reviewed again. Keep vector inputs below the execution bundle limit without replacing them with bitmaps.

`build_v2_showcase.py` regenerates a V1/V2 overview, four-way full figures, five groups of enlarged details and a focused compound-icon comparison from the committed native Figma previews. The V2 input is the complete screenshot-only redraw. The source-assisted case is labeled separately; older local trials are not used as the full V2 result. Portable scenes retain provenance, while execution bundles omit it to preserve space for drawing operations.

## Source recovery

[Source routing](../prompts/04-source-routing.md) separates optional source retrieval from screenshot reconstruction. Retrieval uses the assistant's available host tools. `extract_pdf_assets.py paper.pdf local-outputs/pdf-assets --page 4 --source-url URL` extracts original bitmap objects and transparency masks from a local PDF, with positions and source hashes. It needs PyMuPDF and Pillow, preserves native pixel dimensions, deduplicates repeated image references, and refuses to overwrite an existing directory. It does not download documents or convert PDF vectors/text into a scene.

`trace_icon.py --palette-colors 16` optionally reduces interpolation shades in flat-colored local artwork before tracing; inspect whether it removes meaningful details. Leave it disabled for artwork that needs continuous shading. Tests verify extraction transparency, source dimensions, placements and installed-runtime access in addition to the core scene checks.
