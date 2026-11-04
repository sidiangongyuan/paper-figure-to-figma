# Changelog

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

To update an installed skill, run `python tools/install_skill.py --update` from the updated repository. The previous installation is backed up automatically.
