# Demo

## V2 comparisons

The [AgentThink V2 case](../examples/agentthink-v2/README.md) includes a complete screenshot redraw and a separate source-assisted reconstruction. Both are displayed alongside the reference and preserved V1, with actual Figma previews at matching scale.

- [V1/V2 overview](../assets/agentthink-v1-v2.png)
- [Four-way whole-figure comparison](../assets/agentthink-v2-routes.png)
- [Five groups of enlarged details](../assets/agentthink-v1-v2-details.png)
- [Compound icons and evaluation badges](../assets/agentthink-v2-focus.png)

Run `python tools/build_v2_showcase.py` to rebuild these sheets from the curated examples. Input conditions and attribution are recorded in the case notes.

## Offline editor

Download the repository and open **`demo/index.html`** in a browser. The demo works offline and uses a pre-built reconstruction of PlanWAM Figure 1.

![Comparing the reference and editing the SVG](../assets/workflow.gif)

## Controls

The demo interface is in Chinese; button labels are shown below with translations.

1. In the **拖动对照** (Compare) tab, drag the divider to compare the reference and the reconstruction.
2. In the **编辑图层** (Layers) panel, select the **Planner** text layer and type a new module name.
3. Select the **Planner** fill or **Future latent** and change its color.
4. Select **History contexts** and drag the curvature slider.
5. Click **下载当前 SVG** (Download SVG) or **下载绘图文件** (Download scene file) to save your edits; **恢复示例** (Reset) restores the original.

**▷ 播放流程** (Replay) walks through four stages: reference, layers, comparison and editing.

To edit in Figma, see [Installation and Usage](CODEX_QUICKSTART.md).

## Source

Figure 1 of **[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)**, Xu et al., 2026.

[Reference](../examples/planwam/reference.png) · [Editable SVG](../examples/planwam/reconstruction.svg) · [Scene file](../examples/planwam/planwam.scene.json) · [Example notes](../examples/planwam/README.md)
