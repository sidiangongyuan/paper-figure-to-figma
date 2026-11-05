# Native PowerPoint figures

Use for explicit PPT/PowerPoint output. The current local execution route requires Windows, installed PowerPoint and Python with pywin32. Check these capabilities before authoring. Do not claim equivalent verification on another platform. Keep the existing Figma route unchanged.

## Reconstruction

Use the supplied image and optional permitted source, the same content/appearance checks and the same independently reconstructed vector illustrations. A screenshot-only request excludes source lookup. Rebuild the whole figure, including small text backings, branches, repeated objects and annotations.

- Deliver a new `.pptx` containing native text boxes, native regular shapes and independently editable vector connections. Keep complex illustrations as separate SVG objects. An entire-figure SVG followed by PowerPoint's Convert to Shape is not the text/layout path.
- Keep the figure's aspect ratio. Make the slide large enough for legible editor text; do not force a scientific figure into a widescreen slide. Set an explicit `ppt.pointsPerUnit` to map scene coordinates, dimensions, font sizes and strokes together to PowerPoint points (default 1). Actual text and subscript sizes must meet `ppt.minFontSize` (default 16 points); lower it only for an explicit user choice.
- Disable automatic font shrinking. Set text-box margins, width, height, line spacing, rotation and anchor deliberately; verify stored dimensions after text formatting. Use explicit line breaks when matching a dense source. Preserve scientific wording and use editable subscript/superscript runs where needed.
- Regular geometry and connections should be native. For a simple flat SVG path intended as native geometry, use `pptNative: true`; the local renderer supports absolute M/L/C/Z path commands with a single fill/stroke style. Closed outlines and open strokes need explicit closure. Split mixed-color regular geometry into separate nodes. Other SVGs remain independent vector graphic objects. Unsupported native geometry must be corrected rather than silently flattened.
- Optional text `angle` rotates around `center:[x,y]`; `runs` can specify zero-based `start`, `length`, `baseline` (-1 to 1) and `size` in scene units. These PPT additions do not imply that older Figma renderers understand them.

## Execute and review

Run `python tools/ppt_native.py scene.json output.pptx` (resolve `tools/` under the installed skill's `runtime/` when installed). It creates a fresh local deck, preserves other open files, exports a PowerPoint preview, checks text edit geometry and saves an execution report beside the result. Never stop at code when local execution is available. Use the returned preview path for visual inspection.

Compare the actual PowerPoint render against the full reference and enlarged regions. Inspect text fit, curved/rotated labels, arrow endpoints, dash patterns, layering and SVG appearance. Check native text and shape counts, save/reopen behavior, and editing a label without changing its geometry. A successful file write or XML check alone is insufficient. Dense intended groups and rotated text can produce bounding-box overlap warnings; verify the rendered geometry before deciding whether these are defects.

Repair locally and rerender affected areas. Deliver the reviewed PPTX and a preview. State which objects remain SVG and any material approximations; SVG illustrations are not guaranteed to decompose faithfully into editable paths. Do not automatically modify unrelated presentations, synchronize GitHub or claim that a single successful example establishes universal compatibility.
