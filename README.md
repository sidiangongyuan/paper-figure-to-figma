<div align="center">

<a href="https://github.com/sidiangongyuan/paper-figure-to-figma">
  <img src="assets/wordmark.svg" alt="Paper Figure to Figma" width="420">
</a>

### Rebuild research figures with high fidelity. Keep every step editable.

[![License: MIT](https://img.shields.io/badge/license-MIT-236d4c?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-236d4c?style=flat-square)](CHANGELOG.md)
[![GitHub stars](https://img.shields.io/github/stars/sidiangongyuan/paper-figure-to-figma?style=flat-square&logo=github&color=236d4c)](https://github.com/sidiangongyuan/paper-figure-to-figma/stargazers)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Codex-1f2328?style=flat-square)](.agents/skills/paper-figure-to-figma/SKILL.md)
[![Figma](https://img.shields.io/badge/Figma-native%20layers-F24E1E?style=flat-square&logo=figma&logoColor=white)](https://www.figma.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](docs/DEVELOPMENT.md)

[![Prompt Builder](https://img.shields.io/badge/Prompt%20Builder-Open-236d4c?style=for-the-badge)](https://sidiangongyuan.github.io/paper-figure-to-figma/)
[![Offline Demo](https://img.shields.io/badge/Offline%20Demo-Try%20it-236d4c?style=for-the-badge)](#-demo)

**English** · [简体中文](README.zh-CN.md)

[Quick Start](#-quick-start) • [How it works](#-how-it-works) • [Examples](#-examples) • [Demo](#-demo) • [Updates](#recent-updates) • [FAQ](#-faq)

<br>

<a href="examples/agentthink/README.md"><img src="assets/agentthink-reconstruction.png" alt="Reference, screenshot reconstruction and source-assisted reconstruction" width="100%"></a>

<sub>Reference · From a screenshot · With original source assets · <a href="examples/agentthink/README.md">Example and files</a> · <a href="assets/agentthink-reconstruction-details.png">Enlarged details</a></sub>

</div>

<br>

**Paper Figure to Figma** is an agent skill that turns an image of a research figure into native, editable Figma artwork. Give your AI assistant the figure and a Figma file: it redraws every label, shape and connection as real layers, compares the result with the reference at whole-figure and detail level, fixes what differs, and delivers an editable Figma frame. File exports are available on request.

Provide a screenshot, or add a paper link, PDF or original asset source. The assistant retrieves accessible matching originals when available and continues from the screenshot when no usable source exists.

## Recent updates

**0.2.0 · November 4, 2026** — [Full changelog](CHANGELOG.md)

- **Optional source recovery:** provide a paper link, PDF or project source to retrieve and verify matching original assets.
- **Improved screenshot reconstruction:** preserve compound icon shapes and colors, repair noisy contours, and review every region of the figure.
- **Updated examples:** AgentThink and Aurora reconstructions with whole-figure and enlarged-detail comparisons for both input routes. [Aurora case study](examples/aurora/README.md)
- **Delivery change:** the default result is an editable Figma frame; request SVG/PDF files when needed.

To upgrade an existing installation, run from your repository folder:

```bash
git pull --ff-only
python tools/install_skill.py --update
```

The previous installation is backed up automatically. ZIP users can download the updated repository and run the same installer with `--update`.

## ✨ Features

- **Native, editable layers** — labels stay text, shapes and arrows stay vectors. Only input/output photos are kept as image layers.
- **Details that usually get lost** — gradients, local text backings, transparency, dashed strokes, Bézier curves and stacking order.
- **Built-in review loop** — checks the whole figure, then enlarged details and editability, and revises only the affected elements.
- **Revise without starting over** — follow-up requests update the existing Figma frame and leave the elements you protect untouched.
- **Paper-ready typography** — Times New Roman body text and a clear size hierarchy by default; override any of it.
- **No extra API key** — runs inside your assistant with its Figma connection. No VLM API key or original generation prompt needed.
- **Export when needed** — Figma artwork by default; SVG, PDF and reusable `.scene.json` files on request.
- **Two reconstruction routes** — source-assisted recovery with version and content checks, or a complete reconstruction from the supplied screenshot.
- **Appearance-aware artwork** — preserve silhouette, color and recognizable parts through matching SVGs, geometric reconstruction or cleaned local tracing.

## 🚀 Quick Start

**Requirements**

- An AI assistant that can view images, load local skills, run scripts and call external tools (verified with Codex).
- A Figma connection in that assistant with edit access to the target Design file.
- Python 3.10+. Image preparation, tracing and PDF extraction use optional task-specific dependencies.

**1. Install the skill**

```bash
git clone https://github.com/sidiangongyuan/paper-figure-to-figma.git
cd paper-figure-to-figma
python tools/install_skill.py
```

This installs to `$CODEX_HOME/skills/paper-figure-to-figma` (default `~/.codex/skills/paper-figure-to-figma`). Use `--update` to upgrade an existing install, or `--dest <skills-dir>/paper-figure-to-figma` for another assistant. To skip installation, open the repository in your assistant and ask it to read `.agents/skills/paper-figure-to-figma/SKILL.md`.

**2. Connect Figma**

Enable the Figma tool connection in your assistant and authorize your account.

**3. Rebuild a figure**

Attach the complete reference image and send:

```text
Use $paper-figure-to-figma to reconstruct this image in the linked Figma canvas,
review the whole figure and details, then share the editable frame link.
Figma: <your Design file link>
Source (optional): <paper link, PDF or original asset location>
```

Need specific fonts, colors or edits? Compose the request with the [Prompt Builder](https://sidiangongyuan.github.io/paper-figure-to-figma/).

Full installation and connection guide: [docs/CODEX_QUICKSTART.md](docs/CODEX_QUICKSTART.md)

## 🔄 How it works

```mermaid
flowchart LR
    A[Figure + optional source] --> B{Matching source available?}
    B -->|Yes| C[Retrieve and inspect original assets]
    B -->|No| D[Inspect screenshot features]
    C --> E[Rebuild text, geometry and local contours]
    D --> E
    E --> F[Editable Figma artwork]
    F --> G[Compare whole figure and details]
    G -->|Correct differences| F
    G --> H[Deliver Figma frame]
```

**Source-assisted reconstruction:** retrieve accessible assets from a supplied paper, PDF or project source; verify they match the reference, then extract and reconstruct the relevant objects. An extracted bitmap still needs vector reconstruction.

**Screenshot reconstruction:** preserve visible shapes, colors and component relationships. Rebuild regular parts geometrically, trace irregular contours where useful, and repair noisy results. The method covers the whole figure.

Source information is optional. A title-only lookup is normally limited to about 90 seconds; inaccessible or unmatched sources fall back to the supplied image. Both routes review actual Figma results at whole-figure and enlarged-detail scales. Content and connection errors are fixed first, then readability, then appearance. [Workflow details](prompts/04-source-routing.md)

<details>
<summary><b>What the review checks</b></summary>

<br>

| Review | What to check | Result |
| --- | --- | --- |
| Whole figure | Missing content, panel arrangement, relative sizes, grouping and cross-panel arrow endpoints | Structural differences located |
| Enlarged details | Text accuracy and fit, spacing, curves, gradients, backings, repeated elements and layer order | Region, observed difference and correction |
| Editability | Editable text, independent vector elements, useful groups and protected content | Result can be revised without disturbing protected elements |

Full instructions: [prompts/02-review.md](prompts/02-review.md)

</details>

## 🎨 Examples

### AgentThink

Rebuild the text, modules, illustrations and connections in a screenshot as editable layers. A matching paper or original asset source can provide additional detail.

![Reference and screenshot reconstruction details](assets/agentthink-v2-focus.png)

<details>
<summary><b>Compare details from both reconstruction routes</b></summary>

![Reference, screenshot reconstruction and source-assisted details](assets/agentthink-reconstruction-details.png)

The comparison covers training illustrations, maps and vehicles, frozen/trainable symbols, evaluation icons and character contours.

</details>

[Example files and attribution](examples/agentthink/README.md) · [Version history comparison](examples/agentthink-v2/README.md)

<table>
  <tr>
    <th width="50%">AgentThink</th>
    <th width="50%">PlanWAM</th>
  </tr>
  <tr>
    <td><a href="examples/agentthink/README.md"><img src="assets/agentthink-comparison.png" alt="AgentThink reference and reconstruction"></a></td>
    <td><a href="examples/planwam/README.md"><img src="assets/planwam-comparison.png" alt="PlanWAM reference and reconstruction"></a></td>
  </tr>
  <tr>
    <td>Data generation, two-stage training, inference and evaluation pipeline.<br>Editable text, illustrations and connections</td>
    <td>Four-panel comparison of world-model planning approaches.<br><b>43</b> text layers · <b>334</b> vector objects · <b>8</b> gradients</td>
  </tr>
  <tr>
    <td><a href="https://arxiv.org/abs/2505.15298">Paper</a> · <a href="examples/agentthink/reference.png">Reference</a> · <a href="examples/agentthink/reconstruction.svg">SVG</a> · <a href="examples/agentthink/agentthink.scene.json">Scene</a></td>
    <td><a href="https://arxiv.org/abs/2610.11382">Paper</a> · <a href="examples/planwam/reference.png">Reference</a> · <a href="examples/planwam/reconstruction.svg">SVG</a> · <a href="examples/planwam/planwam.scene.json">Scene</a></td>
  </tr>
</table>

<details>
<summary><b>Detail comparisons</b></summary>

<br>

**AgentThink** — model blocks, curved branches and reward layers

![AgentThink detail comparison](assets/agentthink-details.png)

**PlanWAM** — curved connections, gradients and text backings

![PlanWAM detail comparison](assets/planwam-details.png)

</details>

### Aurora

The same time-series figure rebuilt from a screenshot and from its matching paper PDF. Compare the curved labels, series strokes, domain illustrations and modality symbols across all three images.

![Aurora reference, screenshot reconstruction and source-assisted reconstruction](assets/aurora-reconstruction.png)

<details>
<summary><b>Compare Aurora details</b></summary>

![Aurora enlarged detail comparisons](assets/aurora-reconstruction-details.png)

</details>

Source: Wu et al., *[Aurora: Towards Universal Generative Multimodal Time Series Forecasting](https://arxiv.org/abs/2509.22295)*, Figure 1, PDF page 2 (arXiv v6). Both results use editable text and vectors, with no image layers. Body text uses Times New Roman.

[Case study and citation](examples/aurora/README.md) · [Screenshot result](examples/aurora/screenshot.png) · [Source-assisted result](examples/aurora/source-assisted.png)

Reference figures belong to their original authors; see each example's notes for sources and approximations.

## 🎮 Demo

Download the repository and open **`demo/index.html`** in a browser — no install, works offline. Drag the divider to compare the reference with the reconstruction, edit text, fills and curves, then download the edited SVG.

![Comparing the reference and editing the SVG in the offline demo](assets/workflow.gif)

The demo uses a pre-built PlanWAM reconstruction to show the editable result; it does not run the AI reconstruction. [Demo controls](docs/SHOWCASE.md)

## 🧭 Roadmap

- [x] Agent skill with connected Figma drawing, review and export
- [x] PlanWAM and AgentThink examples with editable files and visual comparisons
- [x] ~~Aurora screenshot and source-assisted reconstructions with whole-figure and detail comparisons~~
- [x] Prompt Builder and offline demo
- [x] ~~Source-assisted retrieval, PDF image extraction and screenshot reconstruction~~
- [x] ~~Complete AgentThink redraw with whole-figure and multi-region detail comparisons~~
- [x] ~~Offline SVG catalog with colored and outline assets, provenance and licenses~~
- [ ] Improve low-resolution character contours, small accessories and background cleanup
- [ ] Extract reusable native vector and text objects from source PDFs
- [ ] Check font size, line width and spacing at the final paper dimensions
- [ ] Better selective updates that preserve manual Figma edits
- [ ] Better mathematical notation and formula reconstruction
- [ ] Style transfer for colors, typography and appearance while keeping content and structure
- [ ] Editable import/export with PowerPoint, draw.io and other drawing tools
- [ ] More examples and reproducible fidelity evaluations
- [ ] Compatibility testing across more assistants and operating systems

## 🚧 Limitations

- **Not pixel-identical.** Fidelity is judged through the whole-figure and detail review, not a universal accuracy score.
- **Small illustrations are approximations.** Library substitutions and local tracing can differ from the reference; unreadable source text is flagged rather than guessed.
- **Photo crops follow the reference resolution.** Use original dataset images for final layouts when available.
- **Full reimports can overwrite manual edits** to managed layers. Duplicate hand-edited artwork before a full rebuild.
- **Verified with Codex** and its Figma connection; other assistants and operating systems are not yet fully tested.
- **Check readability at the final paper size** once the physical dimensions are known.

## ❓ FAQ

<details>
<summary><b>Do I need an API key or the original generation prompt?</b></summary>

No. The skill runs inside your AI assistant and works from the image alone. A paper link, PDF or original source is optional and can help recover clearer assets.

</details>

<details>
<summary><b>Which AI assistants are supported?</b></summary>

It is verified with Codex. Other assistants need image input, local skill and script execution, and external tool calls; install with `--dest` pointing to their skill directory.

</details>

<details>
<summary><b>Do I need a Figma plugin?</b></summary>

No custom plugin is required. The skill uses the Figma tools connected to your assistant and needs edit access to the target Design file.

</details>

<details>
<summary><b>What happens if Figma is not connected?</b></summary>

The skill prepares the scene file and SVG locally, tells you which step is missing — no connection, expired authorization, read-only access or no file access — and continues writing to Figma once it is fixed.

</details>

<details>
<summary><b>Can I keep editing after the first version?</b></summary>

Yes. Edit directly in Figma, or send the assistant the same Figma link with your changes and list the elements that must stay unchanged.

</details>

## 🤝 Contributing

Issues, ideas and new examples are welcome.

- **Bug or unexpected result** — open an issue with the reference image (if shareable), your request and the assistant you used.
- **New example** — include the source paper, a reference image you may redistribute, the `.scene.json` and the exported SVG.
- **Code changes** — run the checks in [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) before opening a pull request.

## 🙏 Acknowledgements

**This open-source project acknowledges and links to the [LINUX DO community](https://linux.do/).** Thank you to the community for sharing ideas and practical experience with AI and design workflows.

The workflow draws on [Image To Slice](https://github.com/50kg/image-to-slice) and the [Linux.do discussion on AI and design workflows](https://linux.do/t/topic/2314994/53). Local-tracing guidance also draws on [ScanSci SVG](https://github.com/Rimagination/scansci-svg); icon sources and licenses are recorded in the [asset catalog](assets/icons/catalog.json).

## 📄 License

Code is released under the [MIT License](LICENSE). Reference figures, paper content and figure-derived example assets retain their original rights; see the source attribution in each example. Bundled icons retain the source licenses recorded in the [asset catalog](assets/icons/catalog.json).
