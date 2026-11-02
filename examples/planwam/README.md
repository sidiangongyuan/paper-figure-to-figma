# PlanWAM · Figure 1

Reconstruction of Figure 1 from **[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)**, Jinchang Xu et al., 2026. [Project page](https://jinchan9.github.io/PlanWAM_project_page/).

[Reference](reference.png) · [Editable SVG](reconstruction.svg) · [Scene file](planwam.scene.json)

| File | Purpose |
| --- | --- |
| `reference.png` | Complete Figure 1 reference image |
| `reconstruction.svg` | Editable SVG exported from the actual Figma frame, with text and vectors preserved |
| `planwam.scene.json` | Complete scene file, including the required RGB crops; give it to the skill to rebuild the figure in Figma |
| `showcase.json` | Layer and font statistics derived from the scene file |

The reconstruction contains 43 editable text layers, 334 independent vector objects and 21 RGB image layers. The RGB layers reuse two image assets. The editing canvas is 1452 × 513.33 with a minimum font size of 16.

![The complete example in an actual Figma frame](../../assets/figma-result.png)

Body text uses Times New Roman; branch titles keep the comic-style font. The car icons are vector redraws. Input and output images are cropped from the low-resolution reference; use the original dataset images for final layouts. Compare the whole figure and details with the reference, and check readability at the final paper size.

The [offline demo](../../docs/SHOWCASE.md) lets you change labels, module fills, gradient start colors and curve paths; downloaded SVG and scene files include those edits. Continued editing in Figma goes through the connected assistant and the skill.

Original figure content belongs to the paper's authors. This example demonstrates figure reconstruction rather than the authors' original editable artwork.
