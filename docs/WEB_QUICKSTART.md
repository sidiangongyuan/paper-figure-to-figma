# 网页模型

准备：Figma 桌面版、支持看图与文字或文件输出的网页模型账号、完整参考图。可补充原始 RGB 图片、SVG 图标和准确文字清单。

## 安装

1. [下载 ZIP](https://github.com/sidiangongyuan/paper-figure-to-figma/archive/refs/heads/main.zip) 并解压，保留完整文件夹。
2. 在 **Figma 桌面版** 打开一个可编辑的 **Design** 文件。
3. 打开 **Plugins → Development → Import plugin from manifest…**，选择 `figma-plugin/manifest.json`。
4. 在 **Plugins → Development** 运行 **Paper Figure to Figma (local)**。

![插件安装步骤](../assets/install-guide.svg)

<details><summary>Figma 要求创建插件标识时</summary>

通过 **Plugins → Development → New plugin → Figma design → Custom UI** 创建本地插件。将仓库 `figma-plugin/` 中的 `code.js` 和 `ui.html` 复制到新插件目录，保留 Figma 生成的清单及标识，确认清单中的 `main` 和 `ui` 分别指向这两个文件。

[Figma 官方安装说明](https://developers.figma.com/docs/plugins/plugin-quickstart-guide/)

</details>

## 试用样例

点击 **加载 PlanWAM 示例 → 生成到 Figma**。选中文字、模块或箭头即可编辑。

![插件界面](../assets/plugin-preview.png)

示例来源：[PlanWAM](https://arxiv.org/abs/2610.11382)，Figure 1。[样例文件与重建差异](../examples/planwam/README.md)。

## 使用

1. **准备图片：** 在插件第1步选择完整参考图，点击 **复制绘图指令**，将原图和指令一起发给网页模型。
2. **导入结果：** 在第2步打开模型返回的 `.json` 文件。模型返回纯文字时，展开 **粘贴绘图内容**，粘贴完整内容。点击 **生成到 Figma**。
3. **对照修改：** 在第3步下载预览、保存项目，将原图、预览、项目和复核指令发给模型。导入修订后的完整文件。
4. **导出：** 下载 SVG 或 PDF，按论文最终尺寸检查字号、线宽和可读性。

输入和结果图片可在 **替换输入与结果图片** 中换成原始素材。

## 继续修改

保存项目文件，下次重新打开。重新导入会更新同项目画板，手动编辑过的画板请先复制备份。项目文件保存模型生成的内容；Figma 中的手动修改保存在 Figma 文件及实际 SVG/PDF 导出中。

## 常见问题

- **绘图文件错误：** 将修复详情、复核指令和原文件交给模型，导入修订后的完整文件。
- **图片位置错误：** 重新选择同一张原始参考图，让模型修正尺寸与裁剪坐标。
- **缺少字体：** 安装所需字体，或让模型替换为已安装字体。
- **模型输出不完整：** 使用文件输出，或将已有文件交给 Codex 继续处理。
