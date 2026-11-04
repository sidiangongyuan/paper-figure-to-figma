# Installation and Usage

## Requirements

- An AI assistant that supports image input, local skills, script execution and external tool calls. The Codex + connected Figma tools path is verified; other assistants need equivalent capabilities.
- A Figma account with edit access to the target Design file.
- Python 3.10+ for the bundled helper scripts. Pillow is used for image preparation, Pillow + VTracer for local tracing, and Pillow + PyMuPDF for PDF image extraction. These dependencies are optional and selected for the task; the assistant can check what is available.

## Install

Clone or [download](https://github.com/sidiangongyuan/paper-figure-to-figma/archive/refs/heads/main.zip) the repository, then run from its root (or ask the assistant to run it):

```bash
python tools/install_skill.py
```

The skill installs to `$CODEX_HOME/skills/paper-figure-to-figma`, or `~/.codex/skills/paper-figure-to-figma` when `CODEX_HOME` is not set. The installed copy is self-contained and works from any project.

| Option | Purpose |
| --- | --- |
| `--update` | Replace an existing installation. The old copy is backed up to a `skill-backups` folder next to the skills directory. |
| `--dest <skills-dir>/paper-figure-to-figma` | Install into another assistant's skill directory. |
| `--package <file.zip>` | Build a portable ZIP instead of installing. |

Without installing, you can open the repository in the assistant and ask it to read `.agents/skills/paper-figure-to-figma/SKILL.md`.

The skill becomes available on the next turn. If the assistant caches its skill list, start a new conversation.

## Connect Figma

Enable the Figma tool connection in the assistant and complete account authorization. The connection must be able to read, create and modify layers and export. Provide a Design file link you can edit; the skill discovers and calls the Figma tools itself.

If the connection is missing or lacks permission, the assistant names the specific problem and can prepare the local scene file first, then continue writing to the canvas once access is restored.

## Use

Attach the complete reference image and send:

```text
Use $paper-figure-to-figma to reconstruct this image in the linked Figma canvas.
Keep text and main structures editable, review the whole figure and details,
then share the editable Figma frame link.
Figma: <your Design file link>
Source (optional): <paper link, PDF or original asset location>
```

For fonts, colors, figure width or specific changes, compose the request with the [Prompt Builder](https://sidiangongyuan.github.io/paper-figure-to-figma/).

The default delivery is the Figma artwork. Ask for SVG, PNG or PDF explicitly when files are needed. Common icons are available offline; complex local tracing optionally needs Pillow and VTracer in the task environment.

With a supplied source, the assistant retrieves accessible matching originals, verifies the figure/version and reconstructs the relevant objects. Without a usable source, it rebuilds the screenshot's visible shapes, colors and compound artwork. Source information is optional; title-only discovery normally has a short time budget. Both routes review the whole figure and enlarged details. See [source routing](../prompts/04-source-routing.md) and the [V2 comparisons](../examples/agentthink-v2/README.md).

To revise later, send the same Figma link with your changes and name the elements that must stay unchanged.
