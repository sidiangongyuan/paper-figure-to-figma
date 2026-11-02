# Quick Start

准备支持看图、本地 Skill/脚本及工具调用的 AI 助手，并授权连接可写的 Figma Design 文件。

1. 下载并解压仓库，在助手中打开该文件夹。
2. 让助手读取 `.agents/skills/paper-figure-to-figma/SKILL.md`。如需跨项目使用，让助手运行 `python tools/install_skill.py` 完成安装。
3. 上传完整参考图，附上 Figma 画布链接，发送：

```text
使用 $paper-figure-to-figma，把附图重建为可编辑 Figma 图。
对照检查整图与局部细节，修正后导出 SVG 和 PDF。
```

助手负责绘制、复核与导出；Figma 首次授权由用户在助手中完成。

[安装与连接](docs/CODEX_QUICKSTART.md) · [工作流](README.zh-CN.md#工作流) · [案例](README.zh-CN.md#案例)
