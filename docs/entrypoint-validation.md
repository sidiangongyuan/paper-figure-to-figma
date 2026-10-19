# User-entrypoint validation

## Implemented entry points

- Prebuilt ordinary Figma Design development plugin: `figma-plugin/manifest.json`, `code.js`, `ui.html`. It makes no model/network requests. UI source and controller are also included; end users do not compile them.
- Portable Chinese web-model instructions include the full scene contract. The plugin inserts original image dimensions and a project ID when copying them.
- Repository skill: `.agents/skills/paper-figure-to-figma/SKILL.md`, plus Chinese first-run guides for web and Codex users.
- Local plugin and MCP bundles embed the same `scene_validate.js` and `figma_import.js`. Updates stage a hidden clone, check the result and replace the prior root only on success. Native node IDs change; logical scene IDs remain stable. Full-scene updates remove obsolete managed nodes; partial MCP batches retain absent nodes. Manual edits to managed nodes can be overwritten.
- The plugin resolves allowed RGB crops using original reference pixels, or accepts original-image replacements per asset. Saved resolved scenes include these assets for transfer. The local preparation tool resolves the same crop contract and creates files for MCP upload.

## Executed checks

- Python scene/render/crop tests and JS runtime tests cover editable text, gradients, required backing, curves, allowed raster roles, duplicate logical IDs, repeat updates, obsolete-node removal, partial imports, missing fonts, failed-update recovery and original-pixel crop coordinates.
- Skill frontmatter was checked with the installed skill validator. Prebuilt plugin sources were regenerated and compared with the build checker. Node parsed the built controller/runtime successfully.
- Real Figma Design test: the shared runtime created a synthetic two-module example with two Times New Roman 16 text nodes and two vector paths. Reimport updated a text label and a native gradient while leaving exactly one project frame. An invalid image update was rejected and the prior frame remained. Existing full research-figure pilot frames were preserved.
- Native `exportAsync` on that real frame returned a 1,498-byte SVG containing two text elements with `svgOutlineText:false`, and a 21,708-byte PDF beginning with `%PDF-`. A native PNG screenshot was visually checked. This tests the same export API used by the controller; the desktop-plugin download handoff remains separate.
- Browser UI smoke with a **mocked Figma parent transport** exercised first run, model-JSON validation errors, reference-image file selection, a 20×20 RGB crop, project JSON download, reopening that project without the reference, reimport, and the export download handoff. This proves the UI/asset/file path, not native desktop plugin execution.
- A project saved from the web UI was read by the local Python scene renderer, RGB preparation tool and MCP bundler to verify the common file contract. The bundler rejected a missing hash mapping and accepted an explicit fixture mapping; that fixture bundle was not executed as a real image upload.
- Automatic-routing update: the skill now explicitly discovers and invokes connected Figma tools without requiring a separate `@Figma` mention, and loads the prerequisite Figma guidance itself. A live read-only check invoked identity and `use_figma` tools in a turn without a new plugin mention, confirmed the established connection and read the existing test frame. It created or changed no canvas nodes. Skill validation passed. This verifies current tool availability, not fresh-session skill selection or the absent/expired-connection branches.

## Product showcase checks

- The full shipped PlanWAM scene was re-executed through the current shared renderer in an isolated Figma frame. All398 logical elements were present exactly once, with43 native text layers,21 permitted RGB layers, a minimum editor font size of16 and18 native gradient objects (including gradients inside SVG icons). The original pilot frames were preserved. A native screenshot was inspected.
- An oversized panel was transferred through ordered node ranges under the50,000-character tool limit. The bundler and skill document this route; tests check that the real panel is transmitted completely with its original geometry. Invalid nested upload responses are rejected before canvas mutation.
- The offline demo was opened directly from a local file. Browser checks exercised label, fill, gradient and Bézier edits; SVG and project downloads; original-view clipping; pause/replay; reduced motion; and a clipboard fallback. The edited398-element project passed the scene validator, and its SVG retained43 text elements. The desktop and390px mobile layouts were visually inspected with no horizontal overflow. Inline SVG2 image references were checked after fixing namespace handling.
- The three-step plugin UI loaded all398 PlanWAM example elements, saved its project and handled repeated imports and invalid data through a mocked Figma transport. This is separate from the live native-renderer test. Screenshots show the actual browser-rendered UI.
- The repository GIF records the actual offline preview interaction. It demonstrates completed stages and editing; it does not represent model-inference timing or native desktop-plugin execution.

## Remaining validation and limits

The local development plugin has not yet been installed and run through Figma Desktop in this environment. In particular, manifest installation/account-ID differences and native-plugin download behavior still require that manual smoke test. The synthetic real-Figma runtime test and the browser transport test are separate evidence; neither is presented as a complete desktop-plugin test.

A fresh Codex session's automatic discovery and invocation of the new repository skill has not been observed here. The guide includes an explicit “read this SKILL.md” fallback. Account-specific Figma connection permissions must also be checked in the user's session.

No fresh reconstruction of an arbitrary image by an external web membership was automated. The model must still produce a complete authored scene; long-output limits, ambiguous labels and complex icon fidelity remain model-dependent. The prior full-figure reconstruction is a pilot, not a general accuracy benchmark. Final paper-size readability needs the physical target size.
