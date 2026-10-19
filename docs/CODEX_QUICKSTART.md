# Codex

## 安装

1. [下载 ZIP](https://github.com/sidiangongyuan/paper-figure-to-figma/archive/refs/heads/main.zip) 并解压。
2. 在 Codex 中打开仓库文件夹，新建对话。仓库已包含所需 Skill。
3. 按提示连接 Figma 账号。修改已有文件时附上 Design 链接。

## 使用

上传完整参考图，发送：

```text
使用 $paper-figure-to-figma 复现这张整图，
完成 Figma 绘制、预览复核和导出。
```

Skill 自动调用已连接的 Figma 工具。连接暂不可用时，先生成可导入的绘图文件和 SVG。

<details><summary>对话中找不到 Skill 时</summary>

发送：

```text
请读取本仓库 .agents/skills/paper-figure-to-figma/SKILL.md，
按其中流程完成我上传的整张科研图。
```

</details>

## 样例

```text
使用 $paper-figure-to-figma，打开 examples/planwam/planwam.scene.json，
把完整样例写入 Figma，检查并导出预览。
```

示例来源：[PlanWAM](https://arxiv.org/abs/2610.11382)，Figure 1。[样例文件](../examples/planwam/README.md)。

## 继续修改

提供上次保存的项目文件、原图和当前预览，说明修改要求。手动编辑过的 Figma 画板请先复制备份。

结果包括 Figma 画板、绘图文件、SVG 和预览；Figma 连接可用时导出 PDF。按论文最终尺寸检查字号、线宽和可读性。
