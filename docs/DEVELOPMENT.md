# Development

User-facing entry points: [Start here](../START_HERE.md), [web](WEB_QUICKSTART.md), [Codex](CODEX_QUICKSTART.md).

## Layout

- `figma-plugin/`: prebuilt plugin plus HTML, CSS and controller sources.
- `.agents/skills/paper-figure-to-figma/`: repository-scoped reconstruction workflow.
- `prompts/`: shared model instructions and scene contract.
- `examples/planwam/`: curated attributed example, reviewed native export and portable project.
- `demo/`: self-contained interactive preview and its sources.
- `web/`: dependency-free prompt generator; opens directly or deploys to GitHub Pages.
- `tools/`: common validation, rendering, image preparation and builders.

The UI and demo are dependency-free. Python3.10+ is sufficient for the builders. Node is used for JS checks. Pillow is optional for image crops and media authoring.

## Build and check

```text
python tools/build_plugin.py
python tools/build_demo.py
python tools/build_plugin.py --check
python tools/build_demo.py --check
python -m unittest discover -s tools -p "test_*.py" -v
node --test tools/test_figma_import.cjs
node --check demo/app.js
node --check web/app.js
node --check figma-plugin/ui.js
```

Commit both the sources and the generated `figma-plugin/code.js`, `ui.html` and `demo/index.html`. End users open these built files directly.

## Scene tools

```text
python tools/scene_to_svg.py examples/minimal.scene.json local-outputs/example.svg
python tools/bundle_figma.py examples/minimal.scene.json local-outputs/example.figma.js
python tools/prepare_scene.py input.scene.json local-outputs/prepared --reference reference.png
```

The optional preparation step uses original reference pixels for allowed input/output RGB crops; it can substitute original files with `--asset ID=PATH`. Upload those files through actual Figma asset tools, map each asset ID to its returned hash string, and pass `--image-hashes` to the bundler. MCP bundles retain the host's50,000-character cap. Split by panel, or split a large panel with `--node-range 0:80`, `--node-range 80:160` and so on (end exclusive, after panel filtering). Preserve original order and continue with the latest returned root ID. All batches must complete before final verification.

The plugin and MCP embed `scene_validate.js` and `figma_import.js`. Full-scene updates stage a clone and replace managed nodes, so native IDs change while logical IDs remain stable. Partial panel updates retain absent nodes. Read [the validation scope](entrypoint-validation.md) before interpreting test results.

## Showcase provenance

`prepare_showcase.py --pilot <local pilot directory>` curates the reviewed PlanWAM run, normalizes its stable IDs and converts xlink references to SVG2 href for reliable HTML embedding. It checks that all398 authored elements exist in the native export. `build_demo.py` packages the resulting example into an offline page. Public example files contain no account IDs, access tokens or signed export URLs.

The GIF and preview screenshots show this real browser interaction. They are product demonstrations rather than recordings of model inference or native desktop-plugin execution.

## Internal records

[Decisions](decisions.md) · [Workflow](workflow-proposal.md) · [First pilot](pilot-01.md) · [Visual corrections](visual-review.md) · [Reference repository](reference-project.md)
