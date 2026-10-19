# 用 Codex，把参考图带进 Figma

## 第一次准备

1. 下载并解压仓库，在 Codex 中打开 **paper-figure-to-figma** 这个文件夹，并新建对话。
2. 准备完整参考图。可以是 AI 生成的图，也可以是已有科研图。
3. 已有目标 Figma Design 文件时，附上链接。首次使用按提示连接 Figma 账号。

## 上传图片，发送这一句

```text
使用 $paper-figure-to-figma 复现这张整图，
完成 Figma 绘制、预览复核和导出。
```

Skill 自行发现和调用已连接的 Figma 工具，也会自行加载绘图需要的操作指引。继续同一项目时复用原画板；新项目按工具能力创建独立文件。

不需要另外添加 `@Figma`。真正缺少连接或授权失效时，会明确提示需要处理的步骤，同时继续准备可导入的项目文件和 SVG。

## 先试附带样例

仓库已经准备好这次的 PlanWAM 完整样例，可以发送：

```text
使用 $paper-figure-to-figma，打开 examples/planwam/planwam.scene.json，
把完整样例写入 Figma，检查并导出预览。
```

图片来源：**[PlanWAM: Planning-Shaped Future Representations for End-to-End Autonomous Driving](https://arxiv.org/abs/2610.11382)**，Figure 1。样例中正文采用 Times New Roman，小车为矢量重绘。[完整说明](../examples/planwam/README.md)。

## 下次继续

提供上次保存的项目文件、原图和当前预览，指出需要修改的地方。Codex 会保留项目中的对应关系，更新画板并重新检查结果。输出默认保存在 `local-outputs/<project-id>/`，研究材料留在本地。

<details><summary>如果当前对话没有显示这个 Skill</summary>

发送：

```text
请读取本仓库 .agents/skills/paper-figure-to-figma/SKILL.md，
按其中流程完成我上传的整张科研图。
```

仓库 Skill 位于 `.agents/skills`，见 [OpenAI 官方说明](https://learn.chatgpt.com/docs/build-skills)。首次账号授权与文件权限仍由对应连接处理。

</details>

最终会交付实际创建的 Figma 画板、可移交项目文件、SVG、可用的 PDF 与预览，以及需要继续检查的差异。手工改过的画板先保留副本。放进论文后，按最终尺寸检查实际字号与可读性。
