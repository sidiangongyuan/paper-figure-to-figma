# Reference project: Image To Slice

Reviewed: 2026-10-19. Source: [50kg/image-to-slice README](https://github.com/50kg/image-to-slice#readme). These are README-level observations, not a completed source-code audit.

## Observed mechanisms

- Analyze a flat image into structured elements and reusable assets.
- Preserve coordinates and allow manual correction before import.
- Offer a manual JSON path for creating Figma layers without model API calls.
- Use generated HTML/CSS and DOM capture on an AI-assisted import path.
- Retain some complex content as raster assets, including fallbacks for difficult visual effects.

## Implications for this project

Potentially useful patterns include an inspectable intermediate representation, explicit coordinates, a correction step, and visual comparison before acceptance.

Editable layered output does not establish that an entire figure is vector artwork. Reconstruction of research figures needs separate acceptance criteria for appearance, vector coverage, semantic editing, and scientific correctness.

These are design hypotheses; the implementation route remains open until representative figures and editing requirements are agreed.

## Prior discussion

The supplied conversation preview establishes interest in adapting this workflow to research figures. Its assistant answers were not available as readable text and are not treated as verified technical evidence here.
