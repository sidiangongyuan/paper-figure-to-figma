# Vector assets

Use this guide when a figure contains icons or complex local illustrations. Keep the reference's scientific meaning and the user's requested fidelity. A figure without these objects needs no asset workflow.

## Choose a representation

1. Follow [source routing](04-source-routing.md) when source information is available or the screenshot is unclear. Inspect matching user-provided vectors, retrieved originals or accessible Figma components before choosing a substitute.
2. Compare silhouette, palette, filled/outlined appearance, proportions and component relationships. Search a suitable public library when it can preserve those features. Permission for a semantic equivalent still requires a visually coordinated result; it does not authorize removing recognizable parts.
3. Build regular geometry directly, including the regular parts of compound icons. Keep lettering as native text over a separate backing. A clipboard with a green check overlay, for example, needs both recognizable parts if those are visible in the reference.
4. Trace distinctive organic contours locally, then clean and group them. Repair regular subparts with geometry if the trace is ragged. Compare the actual rendering at normal and enlarged scales before accepting the object. Resolution limits remain after tracing.

Use a small, coherent selection of libraries within a figure. Recolor monochrome symbols to the figure palette; retain meaningful colors in multicolor artwork. Preserve aspect ratio and optical balance inside each allotted box. Source availability and visual quality both matter: downloading an SVG does not prove it is the right icon.

## Public sources

Prefer official repositories with anonymous SVG downloads and explicit asset licenses. [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) provides colored Flat artwork under MIT; [Noto Emoji](https://github.com/googlefonts/noto-emoji) provides colored SVG artwork under its artwork license (Apache 2.0 in the checked `2D/svg` directory); [Twemoji](https://github.com/jdecked/twemoji) graphics use CC BY 4.0 and require attribution. [Lucide](https://github.com/lucide-icons/lucide) suits outline references; [Lobe Icons](https://github.com/lobehub/lobe-icons) supplies brand artwork. Check the actual file/license and preserve provenance. Per-author catalogs such as Iconfont may require login or have individual terms; treat them as optional discovery sources rather than guaranteed free anonymous downloads. Do not require a Figma community plugin.

## Bundled icons and provided SVGs

The runtime includes a small offline catalog with source URLs, pinned revisions, hashes and original licenses. Search by meaning; inspect candidates before inserting them:

```text
python tools/icon_assets.py search frozen
python tools/icon_assets.py prepare --icon lucide:snowflake --color "#347baa" --output local-outputs/frozen.svg
python tools/icon_assets.py prepare --icon fluent:fire --output local-outputs/fire.svg
python tools/icon_assets.py prepare --icon noto:snowflake --output local-outputs/colored-snowflake.svg
python tools/icon_assets.py prepare --svg local-inputs/object.svg --source SOURCE_URL --license LICENSE_NAME --output local-outputs/object.svg
```

Resolve these tool paths relative to the repository root, or `runtime/` beside an installed SKILL.md. Run from the working project, writing all outputs there. `--online` can retrieve an additional named icon from a catalog provider's pinned official repository; it requires network access. A failed lookup should lead to another suitable source, a supplied SVG or local tracing, rather than repeated identical retries. No model API key or Figma community-plugin installation is required for this path.

Bundled colored samples include Fluent and Noto snowflakes/flames. These are candidates for visual matching, not default replacements for every Frozen/Trainable label. Additional Fluent/Noto assets use the official source links above and `--svg`; automatic named-provider lookup currently covers the providers listed in the catalog's `providers` section.

The preparer resolves `currentColor`, converts supported inline presentation styles to attributes, preserves the viewBox and rejects raster content, text, scripts and external dependencies. Explicit palette colors remain intact. `--stroke-width` adjusts existing stroke-width attributes in the icon's own viewBox units; review its appearance at the final node size. Insert the prepared SVG into a scene `svg` node, and retain the `.source.json` provenance for attribution and later revisions.

## Complex local tracing

Use the current reference, with a crop enclosing the complete object. Keep text and unrelated arrows outside the crop. Pillow and VTracer are optional task-environment dependencies; do not install them globally without authorization.

```text
python tools/trace_icon.py local-inputs/reference.png local-outputs/object.svg --crop LEFT TOP RIGHT BOTTOM
```

Adjust `--scale`, `--filter-speckle`, `--color-precision`, `--layer-difference` and `--path-precision` only in response to observed defects. `--remove-flat-background` may remove a uniform traced backing; check that it does not remove intentional object fill. Inspect holes, thin details, residual background, edge halos and joined shapes. Use continuous geometry for smooth regions and split semantic parts when they need independent edits. Tracing never justifies baked-in label text or embedding the crop as an image.

For flat-colored artwork with many interpolation shades, optional `--palette-colors 16` (or another visually justified size) quantizes the local input before tracing. Compare the result: a palette that erases meaningful colors, detail or shading must be increased or disabled. Palette reduction and enlargement are not detail recovery.

For oversized path data, use an available SVG optimizer (such as SVGO) before lowering visual detail. Re-run vector preparation afterward and compare the optimized rendering with the accepted candidate. A single SVG that exceeds the execution limit cannot be fixed by batching unrelated nodes; optimize its path representation or divide it into meaningful subparts. Do not silently replace it with a bitmap.

## Figma and review

Discover tools actually available in the host. When accessible Figma libraries contain a suitable component, inspect and import it using their supported tools. Do not assume arbitrary installed community plugins can be launched through MCP. Prepared self-contained SVGs can be imported through the existing scene bundle as editable vector nodes. Keep a portable vector equivalent when the delivery requires a scene file.

Review the real Figma export against the reference, including small-symbol readability at the intended display size. Verify that every inserted asset is vector, has the expected grouping and keeps relevant color/edit behavior. Mark source approximations and unresolved details explicitly; if a method produces a worse result, retain the last accepted candidate or switch method. Keep scientific text and connections independent of icon geometry.

For version comparisons, save the exact baseline before edits, state which workflow changes are included, and render both versions at the same scale. Describe concrete differences rather than claiming a universal fidelity percentage.
