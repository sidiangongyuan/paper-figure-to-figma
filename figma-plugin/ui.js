const $ = id => document.getElementById(id);
let referenceImage = null, busy = false, lastError = "";
const replacements = new Map();
const draftId = "figure-" + Date.now().toString(36);
function status(message, kind = "") { $("status").textContent = message; $("status").className = "status " + kind; }
function showPage(name) {
  document.querySelectorAll('[data-panel]').forEach(el => el.hidden = el.dataset.panel !== name);
  document.querySelectorAll('[data-page]').forEach(el => { if (el.dataset.page === name) el.setAttribute('aria-current','step'); else el.removeAttribute('aria-current'); });
  window.scrollTo({top:0,behavior:'instant'});
}
function projectInfo(scene) {
  const texts=scene.nodes.filter(n=>n.type==='text').length;
  $("project-info").hidden=false;$("project-name").textContent=scene.name || "绘图文件已就绪";
  $("project-summary").textContent=texts+" 处文字可直接编辑 · 完整图层已准备好";
}
function setBusy(value) { busy = value; document.querySelectorAll("button,input,textarea").forEach(el => el.disabled = value); }
function fail(error) {
  lastError = error.message || String(error);
  let message=lastError;
  if (/referenceSize|crop|裁剪|原图尺寸/.test(message)) message="图片位置与原图尺寸对不上。请重新选择原图，或把修复详情交给模型调整。";
  else if (/字体|Font/i.test(message)) message="绘图使用的字体暂不可用。请安装该字体，或让模型替换为已安装字体。";
  else if (/JSON|version|nodes|projectId|SVG|填色|节点|色标|透明度|minEditorFontSize/.test(message)) message="绘图文件需要调整。复制复核指令，把修复详情和原文件一起交给模型，再打开更新后的文件。";
  $("error-detail").textContent=lastError;$("error-details").hidden=false;$("error-details").open=false;
  status(message,"error");
}
function readScene() {
  let source = $("scene").value.trim();
  if (source.startsWith("```")) source = source.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "");
  let scene;
  try { scene = JSON.parse(source); } catch (_) { throw new Error("绘图内容不完整。请复制模型返回的完整 JSON，或选择下载的绘图文件。"); }
  if (!scene.projectId) scene.projectId = draftId;
  validateFigureScene(scene);
  return scene;
}
function promptText() {
  const dimensions = referenceImage ? "\n本次参考图真实像素：" + referenceImage.naturalWidth + " × " + referenceImage.naturalHeight + "。" : "";
  return PACK.build + "\n本次 projectId 请使用：" + draftId + "。" + dimensions;
}
async function copy(text) {
  $("prompt").value = text;
  try { await navigator.clipboard.writeText(text); status("指令已复制。请在网页模型中上传附件并发送。"); }
  catch (_) { showPage('prepare');$("prompt").closest("details").open = true; $("prompt").focus(); $("prompt").select(); status("请在已选中的指令上按 Ctrl+C（Mac 为 Cmd+C）复制。"); }
}
async function loadImage(file) {
  const data = await new Promise((resolve,reject) => { const r = new FileReader(); r.onload = () => resolve(r.result); r.onerror = () => reject(new Error("无法读取图片")); r.readAsDataURL(file); });
  return await new Promise((resolve,reject) => { const img = new Image(); img.onload = () => resolve(img); img.onerror = () => reject(new Error("图片无法解码，请改用 PNG 或 JPG")); img.src = data; });
}
function encode(image, crop) {
  const b = crop || [0,0,image.naturalWidth,image.naturalHeight];
  if (b[0] < 0 || b[1] < 0 || b[2] > image.naturalWidth || b[3] > image.naturalHeight || b[2] <= b[0] || b[3] <= b[1]) throw new Error("图片裁剪范围越界，请让模型修正 crop 坐标");
  const canvas = document.createElement("canvas"); canvas.width = Math.max(1,Math.round(b[2]-b[0])); canvas.height = Math.max(1,Math.round(b[3]-b[1]));
  canvas.getContext("2d").drawImage(image,b[0],b[1],b[2]-b[0],b[3]-b[1],0,0,canvas.width,canvas.height);
  return canvas.toDataURL("image/png").split(",")[1];
}
async function resolveAssets(scene) {
  const used = new Set(scene.nodes.filter(n => n.type === "image").map(n => n.asset));
  for (const id of used) {
    const asset = scene.assets[id];
    if (replacements.has(id)) { asset.data = encode(replacements.get(id)); asset.mime = "image/png"; }
    else if (!asset.data) {
      if (!referenceImage) throw new Error("请先选择原始参考图，或为素材「" + id + "」选择原始 RGB 文件");
      const expected = scene.referenceSize;
      if (!expected || expected.width !== referenceImage.naturalWidth || expected.height !== referenceImage.naturalHeight) throw new Error("referenceSize 与所选原图尺寸不一致。请让模型按原始尺寸修正裁剪坐标，不能直接按画布缩放。");
      asset.data = encode(referenceImage,asset.crop); asset.mime = "image/png";
    }
  }
  validateFigureScene(scene);
  return scene;
}
function renderAssets(scene) {
  $("assets").replaceChildren();
  const used=new Set(scene.nodes.filter(n => n.type === "image").map(n => n.asset));
  $("asset-details").hidden=!used.size;
  for (const id of used) {
    const row = document.createElement("div"); row.className = "asset";
    const label = document.createElement("label"); label.textContent = (scene.assets[id].role==='input_rgb'?'输入图片':'结果图片') + " · 可选：换成原始素材";
    const input = document.createElement("input"); input.type = "file"; input.accept = "image/png,image/jpeg,image/webp";
    input.onchange = async () => { try { if (input.files[0]) { replacements.set(id,await loadImage(input.files[0])); status("已选素材「" + id + "」，下次导入和保存项目时应用。"); } } catch (e) { fail(e); } };
    row.append(label,input); $("assets").append(row);
  }
}
function download(bytes, mime, filename) {
  const url = URL.createObjectURL(new Blob([bytes],{type:mime}));
  const a = document.createElement("a"); a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url),1500);
}
$("prompt").value = promptText();
$("example-preview").src=PACK.referenceImage;
document.querySelectorAll('[data-page]').forEach(button=>button.onclick=()=>showPage(button.dataset.page));
document.querySelectorAll('[data-next]').forEach(button=>button.onclick=()=>showPage(button.dataset.next));
$("reference").onchange = async () => {
  try {
    const file = $("reference").files[0]; if (!file) return;
    const img = await loadImage(file); referenceImage = img;
    $("reference-preview").src = img.src; $("reference-preview").hidden = false;
    $("reference-info").textContent = file.name + " · " + img.naturalWidth + " × " + img.naturalHeight;
    $("prompt").value = promptText(); status("参考图已就绪。请把同一张原图和重建指令发给网页模型。");
  } catch (e) { fail(e); }
};
$("copy-build").onclick = () => copy(promptText());
$("copy-review").onclick = () => copy(PACK.review + (lastError ? "\n插件报告的错误：\n" + lastError : ""));
$("example").onclick = () => {
  replacements.clear(); const example = structuredClone(PACK.example); example.projectId = "planwam-example";
  $("scene").value = JSON.stringify(example,null,2); renderAssets(example); projectInfo(example); lastError = "";$("error-details").hidden=true;
  showPage('build');status("PlanWAM 示例已准备好。点击「生成到 Figma」，查看完整四分区与可编辑图层。","success");
};
$("scene-file").onchange = async () => {
  try { const file = $("scene-file").files[0]; if (file) { $("scene").value = await file.text(); replacements.clear(); const scene = readScene(); renderAssets(scene); projectInfo(scene);$("error-details").hidden=true;status("绘图文件已打开，可以生成到 Figma。"); } } catch (e) { fail(e); }
};
$("validate").onclick = () => {
  try { const scene = readScene(); validateFigureScene(scene); renderAssets(scene); projectInfo(scene);lastError = "";$("error-details").hidden=true;status("绘图文件已准备好。生成后，请把实际效果与原图放在一起检查。", "success"); } catch (e) { fail(e); }
};
$("import").onclick = async () => {
  if (busy) return;
  try { const scene = await resolveAssets(readScene()); renderAssets(scene); setBusy(true); status("正在加载字体和生成可编辑图层…"); parent.postMessage({pluginMessage:{type:"import",scene}},"*"); }
  catch (e) { setBusy(false); fail(e); }
};
$("save").onclick = async () => {
  try { const scene = await resolveAssets(readScene()); download(JSON.stringify(scene,null,2),"application/json",scene.projectId+".scene.json"); status("项目文件已准备下载，含已处理的 RGB 素材，可用于网页 / Codex 继续修改。"); } catch (e) { fail(e); }
};
document.querySelectorAll("[data-export]").forEach(button => button.onclick = () => {
  if (busy) return; setBusy(true); status("正在从 Figma 导出…"); parent.postMessage({pluginMessage:{type:"export",format:button.dataset.export}},"*");
});
window.onmessage = event => {
  if (event.source !== parent) return;
  const m = event.data?.pluginMessage; if (!m) return;
  setBusy(false);
  if (m.type === "error") return fail(new Error(m.message));
  if (m.type === "imported") {
    lastError = ""; const a = m.result.audit;$("error-details").hidden=true;showPage('finish');
    status((m.result.status === "updated" ? "画板已更新。" : "画板已生成。") + " " + a.texts + " 处文字可直接编辑，模块与连线已分别保留。\n下载预览，与原图逐处对照。", "success");
  } else if (m.type === "exported") {
    const raw = atob(m.base64), bytes = Uint8Array.from(raw,c => c.charCodeAt(0));
    const ext = m.format.includes("svg") ? "svg" : m.format;
    const mime = ext === "svg" ? "image/svg+xml" : ext === "png" ? "image/png" : "application/pdf";
    download(bytes,mime,"figure-"+m.format+"."+ext); status("导出已准备下载。请检查全图、局部细节和最终论文尺寸。");
  }
};
