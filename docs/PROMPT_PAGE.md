# Prompt

打开 [web/index.html](../web/index.html)，选择模板，按需调整字体、配色或论文图宽，填写具体修改。复制 Prompt，连同完整参考图发给已安装 Skill 的 Codex。

默认指令仅一行；修改选项后追加本次要求。[Skill 安装与使用](CODEX_QUICKSTART.md)。

## 本地使用

下载仓库并解压，直接用浏览器打开 `web/index.html`。页面可离线使用。

## GitHub Pages

1. 将网页及 `.github/workflows/pages.yml` 提交到仓库的 `main` 分支。
2. 在仓库 **Settings → Pages → Source** 选择 **GitHub Actions**。
3. 在 **Actions → Publish prompt page → Run workflow** 中选择 `main` 并运行。
4. 部署完成后，从该次运行的部署记录打开网站。

工作流只发布 `web/` 文件夹。每次更新后，手动运行一次工作流即可发布。

GitHub Free 支持从公开仓库部署 Pages；私有仓库需要支持该功能的付费套餐。也可以将 `web/` 内的三个文件复制到独立公开仓库的根目录，在 Pages 中选择从 `main` 分支的根目录部署。

[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) · [自定义部署工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
