# Validation scope

## v0.1.0 preview

The supported release workflow is a skill-capable vision assistant using an authorized Figma tool connection. The repository includes a self-contained installer and portable ZIP builder.

## Evidence

- Python and JavaScript checks cover editable text, gradients, backings, curves, RGB crop coordinates, partial updates and failed-update recovery.
- Fresh-install tests execute the packaged renderer and Figma bundler from an unrelated directory, check package contents and verify update backups.
- A fresh self-contained installation was explicitly invoked from an unrelated directory in a live Figma test on 2026-11-02. It created a native frame with two editable text nodes, two vector paths and no bitmaps; changed a label; and exported a visually reviewed screenshot and SVG retaining text nodes. The temporary frame was removed afterward. Existing artwork's position, dimensions and descendant count remained unchanged.
- PlanWAM and AgentThink were reconstructed in actual Figma Design files. The included SVGs and previews are native exports; their example notes record approximation limits.
- AgentThink contains 59 editable text layers, 264 vector path nodes and no bitmap fills. Its native SVG text was compared with the scene, and its PDF render was visually reviewed.
- The offline demo supports comparison, editing and downloads. Its GIF shows real browser interaction.

## Limits

Connection authorization and write permissions depend on the user's assistant and Figma account. The fresh-install live test used an existing authorized connection; first-time account authorization and automatic skill discovery were not tested. Other assistant hosts and operating systems are not all verified. Reconstruction quality depends on the source image and model; unresolved labels and approximated illustrations must be disclosed. Final paper-size readability requires the intended physical dimensions.

Tests and node counts support execution correctness; visual fidelity is assessed through the whole-figure and detail review workflow, without a universal accuracy percentage.
