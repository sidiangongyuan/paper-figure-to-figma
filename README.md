# Paper Figure to Figma

An early-stage workflow project for reconstructing AI-generated and existing research figures as editable vector artwork in Figma, with exports suitable for research papers.

**Start here: [中文使用入口](START_HERE.md) · [Web-chat guide](docs/WEB_QUICKSTART.md) · [Local Codex guide](docs/CODEX_QUICKSTART.md)**

**Status:** a prototype toolkit with a prebuilt local Figma plugin, a repository-scoped Codex skill, portable web-chat instructions, a scene validator, an SVG renderer, and an MCP script bundler. The shared renderer has been exercised against real Figma, and the plugin UI has been browser-tested with a mocked Figma transport. Installing the development plugin in Figma Desktop still needs a manual smoke test. There is no automatic image-to-scene model or general fidelity benchmark. [Validation scope](docs/entrypoint-validation.md).

## Use the toolkit

| Entry point | One-time setup | Per figure |
| --- | --- | --- |
| Web visual-model chat | Download the repository ZIP; import `figma-plugin/manifest.json` in Figma Desktop | Select reference → copy built-in instructions to your model → import returned scene JSON → compare previews and revise → export |
| Local Codex | Open this repository as a project; use `$paper-figure-to-figma` | Attach the full reference; the skill discovers and calls connected Figma tools, draws, reviews and exports without a separate `@Figma` mention |

No VLM API key or original image-generation prompt is required. The model does the image analysis; the kit executes its scene. Web users do not need Python, Node.js, or a build step. The local development plugin requires Figma Desktop and is not yet published to Community. The Codex skill does not provide a Figma connection: without one, the agent can deliver the scene for manual import through the same plugin.

The skill uses available Figma tools by default, loading deferred tools and the relevant Figma execution guidance itself. Users do not have to invoke those tools or prerequisite skills separately. Existing project targets are reused; new Design files are created within the requested scope when supported. Account login, expired authorization and unresolved destination selection can still require user action.

Both routes use the same scene files, logical IDs, rendering rules and JS validation. Save the resolved `.scene.json` to move between them. Full reimports rebuild managed nodes and can overwrite manual edits; duplicate the artwork first and select the intended update target if several copies share a project ID. Project JSON records the authored scene, not arbitrary later Figma edits.

For a first run, open the plugin and choose **加载入门示例 → 在 Figma 生成 / 更新**. This creates editable text, separate modules and vector arrows without calling a model.

## Goal

Start from a research-figure image, preserve its intended appearance as closely as practical, and produce a figure that can be edited in Figma and prepared for a paper. Visual fidelity, vector representation, useful editability, and scientific correctness will be evaluated separately.

The reference image is the required input. Its original generation prompt, figure caption, or text list is optional. Image-only reconstruction must work for existing figures whose creation prompts are unavailable. The image guides visual reconstruction; optional materials help interpretation. Unclear content and conflicts are reported for review before corrections. The kit supplies its own reconstruction instructions for the web-chat model.

Provide the full reference image. The planned workflow analyzes the global layout before reconstructing regions in a shared coordinate system, then checks the complete editable figure. Region-level pilots are internal validation steps; users do not need to crop the input or select panel (d).

## Project documents

- [Decision log](docs/decisions.md): confirmed requirements, open decisions, and the current interview step.
- [Reference project notes](docs/reference-project.md): relevant mechanisms and limits of Image To Slice.
- [Workflow proposal](docs/workflow-proposal.md): a draft kit for web-based visual-model conversations, Figma reconstruction, and review.
- [First full-figure pilot](docs/pilot-01.md): executed steps, structural checks, exports, and known differences.
- [Visual review and corrections](docs/visual-review.md): missed gradients, label backing, curve geometry, and the revised typography defaults.
- [Entrypoint validation](docs/entrypoint-validation.md): what was tested and what remains manual.

## Developer tools

The local scene tools need Python 3.10+ and use only the standard library. Run the synthetic example from the repository root:

```text
python tools/scene_to_svg.py examples/minimal.scene.json example.svg
python tools/bundle_figma.py examples/minimal.scene.json example.figma.js
python -m unittest discover -s tools -p "test_*.py" -v
node --test tools/test_figma_import.cjs
python tools/build_plugin.py --check
```

These tools execute an authored scene; they do not extract a scene from an image. Run the generated script through Figma MCP `use_figma` after selecting a Design file. For unresolved RGB crops, `python tools/prepare_scene.py input.scene.json local-outputs/prepared --reference reference.png` resolves original-pixel crops and writes image files for upload; this optional step needs Pillow. Resolved scenes and SVG rendering otherwise use the standard library. Upload images using `upload_assets` and pass an asset-ID-to-image-hash JSON file with `--image-hashes`. Split large scenes with repeated `--panel` arguments, then use the latest returned `--root-id` to append to the inspected target frame. Preserve Figma skill prerequisites when using MCP tools. Importing SVG manually does not establish that Figma text remains editable.

After changing shared rendering code, instructions, or UI sources, run `python tools/build_plugin.py` and commit the regenerated `figma-plugin/code.js` and `ui.html`. The plugin uses the ordinary Plugin API with no model calls or network access. Its UI handles file selection, reference cropping, optional original-RGB substitution, scene import, project saving and native PNG/SVG/PDF export. The complete scene contract is included in the copied model instructions.

Typography defaults to Times New Roman, with Times New Roman or Comic for headings. Scene validation defaults to a minimum editor font size of 16; a per-figure `typographyPolicy` can record an explicit exception. The final printed font size requires a separate check after paper scaling. Rectangles support linear-gradient fills and opacity. An optional `visualFeatures` inventory checks required gradients, translucent label backing and curves; this inventory must itself be reviewed against the reference because it cannot discover omissions automatically.

The intended workflow must work with existing web-chat visual-model subscriptions and must not require a VLM API key. The first version uses manual uploads, downloads, or copy-paste between web chat and reconstruction tools; the tools handle reconstruction and validation.

Reference inputs and generated outputs are kept in local-only directories by default. This repository does not contain the original chat transcript or reference images.

## Acknowledgements

[50kg/image-to-slice](https://github.com/50kg/image-to-slice) is a workflow reference. No upstream source code has been copied into this repository. Any future reuse must preserve applicable license notices.

## License and citation

A distribution license and citation metadata have not been selected.
