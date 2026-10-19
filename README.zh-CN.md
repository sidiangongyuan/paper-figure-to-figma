# Paper Figure to Figma

将科研参考图重建为 Figma 中可编辑的文字、形状、箭头和矢量图标，导出 SVG 或 PDF。

[English](README.md) · [Quick Start](START_HERE.md) · [Demo](#demo)

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

## Demo

双击 **`demo/index.html`**。可离线对照原图、修改文字、配色和曲线，下载修改后的 SVG。

![原图对照与 SVG 编辑](assets/workflow.gif)

[参考图](examples/planwam/reference.png) · [可编辑 SVG](examples/planwam/reconstruction.svg) · [绘图文件](examples/planwam/planwam.scene.json) · [样例说明](examples/planwam/README.md)

图片来源：**[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)**，Xu et al., 2026，Figure 1。重建版正文采用 Times New Roman，小车图标为矢量重绘。原始内容归其作者所有。

## 文档

[Quick Start](START_HERE.md) · [Demo 操作](docs/SHOWCASE.md) · [开发文档](docs/DEVELOPMENT.md)

工作流参考：[Image To Slice](https://github.com/50kg/image-to-slice)。代码许可待确定。
