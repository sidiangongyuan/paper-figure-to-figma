# Installation and Usage

## Requirements

- An AI assistant that supports image input, local skills, script execution and external tool calls. The Codex + connected Figma tools path is verified; other assistants need equivalent capabilities.
- A Figma account with edit access to the target Design file.
- Python 3.10+ for the bundled helper scripts. Pillow is needed only for cropping photo regions from the reference image. You can ask the assistant to check these dependencies.

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
then export SVG and PDF.
Figma: <your Design file link>
```

For fonts, colors, figure width or specific changes, compose the request with the [Prompt Builder](https://sidiangongyuan.github.io/paper-figure-to-figma/).

To revise later, send the same Figma link with your changes and name the elements that must stay unchanged.
