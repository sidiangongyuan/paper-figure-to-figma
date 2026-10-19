# 一张图，从参考到继续编辑

![完整流程回放](../assets/workflow.gif)

下载仓库并解压，双击 **`demo/index.html`**，就能打开交互演示。页面已包含所需图片、图形与代码，可以离线使用。

## 在演示里试试

1. **拖动对照。** 原图与重建结果共享相同的显示尺寸。
2. **改一处文字。** 点右侧 Planner 文字层，输入自己的模块名。
3. **调一个颜色。** 选择模块底色或 Future latent 渐变，调整填色。
4. **动一段曲线。** 选择 History contexts，拖动弧度滑块。
5. **下载刚改好的文件。** SVG 保留可编辑文字，项目文件也会带上相应修改。

播放按钮会回放“参考图→建立图层→对照修订→继续编辑”四个阶段。可以暂停，也可以直接选择一个阶段。回放基于本轮已完成的重建结果，时长只用于演示。

页面中的编辑直接作用于实际 Figma 导出的 SVG，并同步到下载的绘图文件。浏览器内的选择与改色属于本地交互；Figma 中的后续编辑使用仓库附带插件或 Codex 连接。

## 实际样例

图片来源：**[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)**，Xu et al., 2026，Figure 1。

| 样例信息 | 数值 |
| --- | --- |
| 完整分区 | 4 |
| 可编辑文字 | 43 |
| 矢量对象 | 334 |
| RGB 图片层 | 21（复用2份素材） |
| 编辑画布 | 1452×513.33 |
| 最小编辑字号 | 16px |

[参考图](../examples/planwam/reference.png) · [实际 Figma SVG 导出](../examples/planwam/reconstruction.svg) · [完整绘图文件](../examples/planwam/planwam.scene.json)

正文已经调整为 Times New Roman，分支标题保留漫画风字体，小车采用矢量重绘。RGB 素材来自参考图中的裁剪，正式排版优先替换为原始数据集素材。字体、图标与精度说明保留在 [样例说明](../examples/planwam/README.md) 中。
