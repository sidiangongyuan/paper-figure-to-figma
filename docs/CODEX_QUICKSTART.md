# Skill 安装与使用

## 准备

使用支持图片输入、本地技能、脚本执行和外部工具调用的 AI 助手。当前已验证 Codex 与已连接的 Figma 工具路径；其他助手需具备等价能力。Figma 账号需对目标 Design 文件有编辑权限。

Skill 自带辅助脚本，运行环境需要 Python 3.10+；涉及 RGB 图片裁剪时需要 Pillow。可让助手检查这些依赖。

## 安装

下载并解压仓库。在仓库目录运行，或让助手执行：

```text
python tools/install_skill.py
```

默认安装到 `$CODEX_HOME/skills/paper-figure-to-figma`；未设置该变量时使用 `~/.codex/skills/paper-figure-to-figma`。安装包包含运行文件，可以在其他项目中使用。

更新已有安装：

```text
python tools/install_skill.py --update
```

旧安装自动备份到技能目录外的 `skill-backups` 文件夹。其他助手可用 `--dest <技能目录>/paper-figure-to-figma` 指定安装位置。

也可直接在助手中打开仓库并读取 `.agents/skills/paper-figure-to-figma/SKILL.md`。安装后在下一轮调用 Skill；如果助手缓存了技能列表，重新打开对话。

## 连接 Figma

在助手中启用 Figma 工具连接，按提示完成账号授权。连接需要支持读取、创建或修改图层及导出。提供具有编辑权限的 Figma Design 链接；Skill 会发现并调用工具。

若连接缺失或权限不足，助手会指出具体问题，并可先准备本地绘图文件。连接恢复后继续写入目标画布。

## 使用

上传完整参考图，发送：

```text
使用 $paper-figure-to-figma，将附图重建到以下 Figma 画布。
保持文字和主体结构可编辑，检查整图与局部细节后导出 SVG 和 PDF。
Figma 地址：填写你的 Design 链接
```

需要个性化要求时，可使用 [Prompt 页面](../web/index.html)。继续修改时提供原 Figma 链接和修改要求，并指出需要保持不变的元素。

[官方 Skill 说明](https://learn.chatgpt.com/docs/build-skills) · [验证范围](entrypoint-validation.md)
