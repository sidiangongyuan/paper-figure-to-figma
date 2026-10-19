# Quick Start

[下载 ZIP](https://github.com/sidiangongyuan/paper-figure-to-figma/archive/refs/heads/main.zip)，解压后保留完整文件夹。

## 网页模型

准备 Figma 桌面版、支持看图的网页模型账号和完整参考图。

1. 在 Figma Design 文件中打开 **Plugins → Development → Import plugin from manifest…**，选择 `figma-plugin/manifest.json`。
2. 运行 **Paper Figure to Figma (local)**。
3. 点击 **加载 PlanWAM 示例 → 生成到 Figma**，测试文字和图形编辑。
4. 制作自己的图：在插件中选参考图、复制指令，发给网页模型。将返回的 `.json` 文件导入插件，对照修改后导出。

[详细步骤](docs/WEB_QUICKSTART.md)

## Codex

1. 在 Codex 中打开仓库文件夹，新建对话。
2. 上传完整参考图，发送：

```text
使用 $paper-figure-to-figma 复现这张整图，
完成 Figma 绘制、预览复核和导出。
```

首次使用按提示连接 Figma 账号。已有目标文件时附上 Design 链接。

[详细步骤](docs/CODEX_QUICKSTART.md)

## Demo

双击 `demo/index.html`，可离线对照、编辑并下载 SVG。

示例来源：[PlanWAM](https://arxiv.org/abs/2610.11382)，Figure 1。[样例文件](examples/planwam/README.md)。
