# Paper Figure to Figma

An early-stage workflow project for reconstructing AI-generated and existing research figures as editable vector artwork in Figma, with exports suitable for research papers.

**Status:** early scene-execution prototype. One full reference figure has been rebuilt in Figma and exported. The repository includes a scene validator, SVG renderer, and Figma script bundler. It does not yet include an automatic image-to-scene model, a packaged local Figma plugin, or a validated general fidelity benchmark.

## Goal

Start from a research-figure image, preserve its intended appearance as closely as practical, and produce a figure that can be edited in Figma and prepared for a paper. Visual fidelity, vector representation, useful editability, and scientific correctness will be evaluated separately.

The reference image is the required input. Its original generation prompt, figure caption, or text list is optional. Image-only reconstruction must work for existing figures whose creation prompts are unavailable. The image guides visual reconstruction; optional materials help interpretation. Unclear content and conflicts are reported for review before corrections. The kit supplies its own reconstruction instructions for the web-chat model.

Provide the full reference image. The planned workflow analyzes the global layout before reconstructing regions in a shared coordinate system, then checks the complete editable figure. Region-level pilots are internal validation steps; users do not need to crop the input or select panel (d).

## Project documents

- [Decision log](docs/decisions.md): confirmed requirements, open decisions, and the current interview step.
- [Reference project notes](docs/reference-project.md): relevant mechanisms and limits of Image To Slice.
- [Workflow proposal](docs/workflow-proposal.md): a draft kit for web-based visual-model conversations, Figma reconstruction, and review.
- [First full-figure pilot](docs/pilot-01.md): executed steps, structural checks, exports, and known differences.

## Getting started

The local scene tools need Python 3.10+ and use only the standard library. Run the synthetic example from the repository root:

```text
python tools/scene_to_svg.py examples/minimal.scene.json example.svg
python tools/bundle_figma.py examples/minimal.scene.json example.figma.js
python -m unittest discover -s tools -p "test_*.py" -v
```

These tools execute an authored scene; they do not extract a scene from an image. Run the generated script through Figma MCP `use_figma` after selecting a Design file. For raster assets, upload them using `upload_assets` and pass an asset-ID-to-image-hash JSON file with `--image-hashes`. Split large scenes with repeated `--panel` arguments, then use `--root-id` to append to the inspected target frame. Preserve Figma skill prerequisites when using MCP tools. Importing SVG manually does not establish that Figma text remains editable.

The intended workflow must work with existing web-chat visual-model subscriptions and must not require a VLM API key. The first version uses manual uploads, downloads, or copy-paste between web chat and reconstruction tools; the tools handle reconstruction and validation.

Reference inputs and generated outputs are kept in local-only directories by default. This repository does not contain the original chat transcript or reference images.

## Acknowledgements

[50kg/image-to-slice](https://github.com/50kg/image-to-slice) is a workflow reference. No upstream source code has been copied into this repository. Any future reuse must preserve applicable license notices.

## License and citation

A distribution license and citation metadata have not been selected.
