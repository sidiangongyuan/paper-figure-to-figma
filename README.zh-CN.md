# Paper Figure to Figma

将科研参考图重建为 Figma 中可编辑的文字、形状、箭头和矢量图标，导出 SVG 或 PDF。

[English](README.md) · [Quick Start](#quick-start) · [案例](#案例) · [Demo](#demo) · [Prompt 生成](https://sidiangongyuan.github.io/paper-figure-to-figma/)

[![AgentThink 原图与可编辑重建结果对比](assets/agentthink-comparison.png)](examples/agentthink/reconstruction.svg)

AgentThink 复杂案例包含 **59 个可编辑文字层**、**264 个矢量路径节点**，无位图填充。[打开 SVG](examples/agentthink/reconstruction.svg) · [绘图文件](examples/agentthink/agentthink.scene.json) · [来源与还原说明](examples/agentthink/README.md)

## Quick Start

[下载 ZIP](https://github.com/sidiangongyuan/paper-figure-to-figma/archive/refs/heads/main.zip) 并解压。插件和演示可直接使用。

### 网页模型 + Figma 插件

准备：Figma 桌面版，以及支持看图、输出文字或文件的网页模型账号。

1. 在 Figma Design 文件中打开 **Plugins → Development → Import plugin from manifest…**，选择 `figma-plugin/manifest.json`。
2. 运行 **Paper Figure to Figma (local)**，点击 **加载 PlanWAM 示例 → 生成到 Figma**，试用附带样例。
3. 制作自己的图：在插件中选择完整参考图，将图片和复制的绘图指令一起发给网页模型。
4. 导入模型返回的 `.json` 文件，对照修改后导出 SVG 或 PDF。

[安装与使用详情](docs/WEB_QUICKSTART.md)

### Codex

1. 在 Codex 中打开解压后的仓库文件夹，新建对话。
2. 上传完整参考图，发送：

```text
使用 $paper-figure-to-figma 复现这张整图，
完成 Figma 绘制、预览复核和导出。
```

Skill 自动调用已连接的 Figma 工具。首次使用按提示连接账号；修改已有文件时附上 Design 链接。

[Codex 安装与使用详情](docs/CODEX_QUICKSTART.md)

### Prompt

打开 [web/index.html](web/index.html)，选择模板并补充个性化要求。复制 Prompt，连同完整参考图发给 Codex。[使用与 GitHub Pages 部署](docs/PROMPT_PAGE.md)。

## 案例

### AgentThink

完整覆盖数据生成、两阶段训练、推理与评估。复杂小插画与品牌符号为矢量近似重绘，原图小卡片中部分占位文字无法辨清。

![AgentThink 的模型模块、曲线分支和奖励层细节对比](assets/agentthink-details.png)

[参考图](examples/agentthink/reference.png) · [可编辑 SVG](examples/agentthink/reconstruction.svg) · [绘图文件](examples/agentthink/agentthink.scene.json) · [论文](https://arxiv.org/abs/2505.15298) · [样例说明](examples/agentthink/README.md)

### PlanWAM

[![PlanWAM 原图与可编辑重建结果对比](assets/planwam-comparison.png)](examples/planwam/reconstruction.svg)

PlanWAM 样例包含 **43 个可编辑文字层**、**334 个矢量对象**和 **8 处渐变**。输入、输出 RGB 图像保留为独立图片层。[打开 SVG](examples/planwam/reconstruction.svg) · [绘图文件](examples/planwam/planwam.scene.json)

放大对照曲线、渐变和局部文字底板。重建版正文采用 Times New Roman，小车图标为矢量近似重绘。

![原图与重建结果的曲线、渐变、文字底板细节对比](assets/planwam-details.png)

[参考图](examples/planwam/reference.png) · [可编辑 SVG](examples/planwam/reconstruction.svg) · [绘图文件](examples/planwam/planwam.scene.json) · [样例说明](examples/planwam/README.md)

来源：[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)，Figure 1。原始图片内容归其作者所有。论文中的可读性需按最终尺寸检查。

## Demo

下载后打开 **`demo/index.html`**。拖动分界线对照原图，修改文字、填色与曲线，下载编辑后的 SVG。支持离线使用。

![慢速演示原图对照与 SVG 编辑](assets/workflow.gif)

这段 13 秒循环展示仓库附带的浏览器演示，开头与结束保留停顿。[操作说明](docs/SHOWCASE.md)

## 文档

[Quick Start](START_HERE.md) · [Demo 操作](docs/SHOWCASE.md) · [开发文档](docs/DEVELOPMENT.md)

工作流参考：[Image To Slice](https://github.com/50kg/image-to-slice)。代码许可待确定。
