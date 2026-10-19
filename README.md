<div align="center">

<img src="assets/wordmark.svg" width="560" alt="Paper Figure to Figma">

**Your next paper figure, ready to keep editing.**

Rebuild research-figure references as editable text, vectors and connections in Figma.<br>
Bring a clear image and the visual model you already use.

[中文介绍](README.zh-CN.md) · [Start here](START_HERE.md) · [Try the demo](#see-it-in-action) · [Example files](examples/planwam/)

</div>

## See it in action

![PlanWAM reference-to-editable-figure workflow, with comparison and text editing](assets/workflow.gif)

The interactive preview lets you compare the full figure, change a label, adjust a module's fill, edit a gradient and bend a curve. Download the edited SVG or project and keep working.

**Open the interactive demo:** [download the ZIP](https://github.com/sidiangongyuan/paper-figure-to-figma/archive/refs/heads/main.zip), unzip it, then double-click **`demo/index.html`**. It runs offline, with everything included.

Figure source: **[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)**, Xu et al., 2026, Figure 1. The replay uses our reviewed Figma reconstruction. Body typography has been adjusted to Times New Roman, and car icons have been redrawn as vectors. [Inspect the example](examples/planwam/README.md).

## Keep every revision easy

| Edit | What stays editable |
| --- | --- |
| Refine the language | Text content, fonts and sizes |
| Adjust the layout | Separate modules, arrows and grouped vector icons |
| Match your paper's style | Fills, gradients, strokes, dashed lines and curves |
| Finish the figure | Figma artwork, portable project, SVG and PDF exports |

The included PlanWAM example contains **43 text layers, 334 vector objects and all four panels**. RGB inputs and outputs remain separate image layers. The full project and actual Figma SVG export are included.

## Your first figure

### With a web model

1. Download and unzip the repository. In **Figma Desktop → Plugins → Development → Import plugin from manifest…**, select `figma-plugin/manifest.json`.
2. Run **Paper Figure to Figma (local)**. Choose **体验 PlanWAM 示例 → 生成到 Figma** to explore the complete example.
3. For your own figure, choose the full image, copy the built-in instructions to your visual-model chat, then open the returned drawing file in the plugin. Compare, revise and export.

The plugin is already built. A web account that understands images and returns text or files is enough to start; no model API key or original image-generation prompt is needed. [Web guide →](docs/WEB_QUICKSTART.md)

### With Codex

1. Open this repository as a project in Codex.
2. Attach the complete reference image and send:

```text
Use $paper-figure-to-figma to reconstruct this full figure,
review the rendered result, and export the editable artwork.
```

The skill finds and invokes connected Figma tools itself. Supply an existing Design link if you have one. First-time account authorization is handled when needed. [Codex guide →](docs/CODEX_QUICKSTART.md)

## Explore the example

[Reference image](examples/planwam/reference.png) · [Editable SVG](examples/planwam/reconstruction.svg) · [Portable project](examples/planwam/planwam.scene.json) · [Walkthrough](docs/SHOWCASE.md)

![Paper Figure to Figma plugin with the complete PlanWAM example](assets/plugin-preview.png)

Body text defaults to Times New Roman with an editor size of at least16px. Check readability again at the final paper size. Exact icon shape and visual fidelity deserve a close comparison; the example notes retain its observed differences.

## Guides

- [中文快速开始](START_HERE.md)
- [Web-model setup and first run](docs/WEB_QUICKSTART.md)
- [Codex setup and first run](docs/CODEX_QUICKSTART.md)
- [Development and checks](docs/DEVELOPMENT.md)
- [Validation scope](docs/entrypoint-validation.md)

**Preview release.** The local development plugin is included; Community distribution is a future step. Native Figma rendering/export and browser interactions have been exercised. Installing the plugin through Figma Desktop remains a manual check. See the validation record for the exact scope.

## Credits

PlanWAM supplies the reference figure for this demonstration; its authors retain rights to their original material. The reconstruction and typography changes are identified alongside the example. No endorsement is implied.

Workflow reference: [50kg/image-to-slice](https://github.com/50kg/image-to-slice). Presentation inspiration: [AI Job Search](https://github.com/MadsLorentzen/ai-job-search) and [OpenCode](https://github.com/anomalyco/opencode). Their branding and source code have not been copied. [Design notes](docs/DESIGN_NOTES.md).

A distribution license for this project's own code has not yet been selected.
