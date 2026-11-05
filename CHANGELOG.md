# Changelog

[English update summary](README.md#recent-updates) · [中文更新摘要与升级方法](README.zh-CN.md#最近更新)

## 0.2.5 — 2026-11-05

### PowerPoint

- Added native PowerPoint output to the existing skill. Request PPTX to create editable text boxes, regular shapes and paths, with complex illustrations as separate SVG objects. Figma remains the default output.
- Added a Windows renderer using installed desktop PowerPoint and pywin32. It saves and reopens the deck, exports an actual PowerPoint preview, checks text-edit geometry and records results for visual review.
- Added explicit coordinate scaling, minimum font-size checks, rotated text and subscript/superscript runs. Existing presentations are preserved and output files are never overwritten.
- Packaged the PowerPoint workflow and renderer with the globally installed skill. Added PowerPoint to the Prompt Builder.

### Examples

- Added downloadable Aurora and P-GenRM PPTX files, clean reference/result comparisons and real PowerPoint object-selection screenshots.
- Documented native text/shape counts and independent SVG illustrations beside each example. Editable SVG objects do not imply lossless conversion to individual PowerPoint paths.
- Added P-GenRM paper attribution and BibTeX: *Personalized Generative Reward Model with Test-time User-based Scaling*, ICLR 2026 Oral. This example was reconstructed from the supplied screenshot; citation verification happened afterward.
- Added a PowerPoint support badge, refreshed both READMEs and marked the delivered PowerPoint work complete in the roadmap.

### Requirements and upgrade

PowerPoint generation and verification currently require Windows, installed desktop PowerPoint and `pywin32`. No Figma connection is needed for this route. Run `git pull --ff-only` and `python tools/install_skill.py --update` to upgrade; the previous skill installation is backed up automatically.

## Documentation update — 2026-11-04

- Added Aurora Figure 1 with independently completed screenshot and source-assisted reconstructions, actual Figma previews, whole-figure comparisons and four enlarged detail groups.
- Added paper authors, the exact source version/page/figure, BibTeX and reconstruction provenance beside the Aurora case study. Paper citations are kept with examples, separate from workflow acknowledgements.
- Updated all main AgentThink artwork and downloads to the current reconstruction. The first image compares the reference, screenshot reconstruction and reconstruction with original source assets.
- Simplified showcase labels around inputs and editable results. Earlier versions are retained only in history comparisons. PlanWAM artwork and demo remain unchanged.

## 0.2.0 — 2026-11-04

### Reconstruction

- Added source-assisted and screenshot reconstruction routes. Source information is optional; accessible originals are retrieved and checked against the reference. Title-only discovery has a short default time budget.
- Added PDF bitmap extraction with original pixel dimensions, transparency masks, page placements and provenance. PDF vector/text extraction remains on the roadmap.
- Changed icon selection to prioritize silhouette, palette and component relationships. Regular shapes use geometry; irregular contours use local tracing and repair. Complete redraws cover every region.
- Added optional palette reduction for tracing flat artwork and a 21-icon offline catalog with Lucide, Lobe Icons, Fluent and Noto samples and source licenses.
- Default delivery is editable Figma artwork. SVG/PDF files and other exports are produced when requested.

### Examples and documentation

- Added the complete AgentThink screenshot V2 and a separate source-assisted reconstruction, alongside the preserved V1.
- Added whole-figure comparisons, five detail groups and a focused compound-icon comparison using actual Figma previews.
- Updated both READMEs, installation guidance and the roadmap. Completed V2 items are checked off; low-resolution contour cleanup and native PDF object extraction remain planned.

### Validation

- 25 Python tests and 7 JavaScript tests pass, covering scene validation, Figma imports, SVG assets, tracing, PDF extraction and portable skill installation.
- Verified the PDF extraction helper against the AgentThink paper and checked relative documentation links and the packaged runtime.

### Upgrading

From an existing clone:

```bash
git pull --ff-only
python tools/install_skill.py --update
```

If installed from a ZIP, download the updated repository and run `python tools/install_skill.py --update` from that folder. The previous installation is backed up automatically. Existing Figma drawings are not changed by the skill upgrade.
