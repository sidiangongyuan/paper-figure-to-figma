// Shared contract for the ordinary plugin, its UI, and MCP bundles.
function validateFigureScene(scene) {
  const fail = message => { throw new Error(message); };
  const finite = v => typeof v === "number" && Number.isFinite(v);
  const color = v => typeof v === "string" && /^#[0-9a-f]{6}$/i.test(v);
  const fill = v => {
    if (v == null || v === "none" || color(v)) return;
    if (!v || v.type !== "linear" || !["vertical","horizontal"].includes(v.direction || "vertical") || !Array.isArray(v.stops) || v.stops.length < 2) fail("填色必须是六位色号或线性渐变");
    let previous = -1;
    for (const s of v.stops) {
      if (!finite(s.offset) || s.offset < previous || s.offset < 0 || s.offset > 1 || !color(s.color) || !finite(s.opacity ?? 1) || (s.opacity ?? 1) < 0 || (s.opacity ?? 1) > 1) fail("渐变色标无效");
      previous = s.offset;
    }
  };
  if (!scene || scene.version !== 1 || !finite(scene.width) || !finite(scene.height) || scene.width <= 0 || scene.height <= 0 || !Array.isArray(scene.nodes) || !scene.nodes.length) fail("需要 version:1、正数画布宽高和非空 nodes 列表");
  if (scene.background != null && !color(scene.background)) fail("画布背景必须是六位色号");
  if (scene.projectId != null && !/^[a-zA-Z0-9_-]{1,80}$/.test(scene.projectId)) fail("projectId 只能包含字母、数字、下划线或短横线");
  const minimum = scene.typographyPolicy?.minEditorFontSize ?? 16;
  if (!finite(minimum) || minimum <= 0) fail("minEditorFontSize 必须是正数");
  const ids = new Map(), panels = new Set(), counts = {};
  for (const [i, n] of scene.nodes.entries()) {
    if (!n || typeof n.id !== "string" || !n.id || n.id.includes(" · ") || ids.has(n.id)) fail("节点 ID 为空、重复或包含保留分隔符: " + n?.id);
    ids.set(n.id,i);
    if (!["rect","text","svg","image"].includes(n.type)) fail("不支持的节点类型: " + n.type);
    if (!["x","y","w","h"].every(k => finite(n[k])) || n.w <= 0 || n.h <= 0) fail("节点坐标或尺寸无效: " + n.id);
    if (!finite(n.opacity ?? 1) || (n.opacity ?? 1) < 0 || (n.opacity ?? 1) > 1) fail("透明度无效: " + n.id);
    panels.add(n.panel || "canvas"); counts[n.type] = (counts[n.type] || 0) + 1;
    if (n.type === "rect" || n.type === "image") {
      fill(n.stroke);
      if (!finite(n.sw ?? 1) || (n.sw ?? 1) < 0 || !finite(n.r ?? 0) || (n.r ?? 0) < 0) fail("描边或圆角无效: " + n.id);
      if (n.dash && (typeof n.dash !== "string" || !n.dash.split(/[ ,]+/).every(v => finite(Number(v)) && Number(v) > 0))) fail("虚线参数无效: " + n.id);
    }
    if (n.type === "rect") fill(n.fill);
    if (n.type === "text") {
      if (typeof n.text !== "string" || !finite(n.size) || n.size < minimum - .001) fail("文字必须可编辑，编辑字号至少 " + minimum + ": " + n.id);
      if (n.color && !color(n.color)) fail("文字色号无效: " + n.id);
      if (n.align && !["left","center","right"].includes(n.align)) fail("文字对齐方式无效: " + n.id);
      if (n.lineHeight != null && (!finite(n.lineHeight) || n.lineHeight <= 0)) fail("行高无效: " + n.id);
    }
    if (n.type === "svg") {
      const tags = new Set(["svg","g","defs","path","rect","circle","ellipse","line","polyline","polygon","linearGradient","radialGradient","stop","clipPath","mask","title","desc"]);
      if (typeof n.svg !== "string" || !/^\s*<svg[\s>]/.test(n.svg) || /<!|<\?|\bhref\s*=|\bon[a-z]+\s*=|\bstyle\s*=|url\(\s*[^#]/i.test(n.svg)) fail("图标只能包含内联矢量，不能包含图片、文字或外部资源: " + n.id);
      for (const match of n.svg.matchAll(/<\/?([\w:-]+)/g)) if (!tags.has(match[1])) fail("SVG 中不支持的元素 " + match[1] + ": " + n.id);
    }
    if (n.type === "image") {
      const a = scene.assets?.[n.asset];
      if (!["input_rgb","output_result"].includes(n.role) || !a || a.role !== n.role) fail("只有输入 RGB 和输出结果可使用图片: " + n.id);
      if (a.data != null) { if (!["image/png","image/jpeg"].includes(a.mime) || typeof a.data !== "string") fail("图片必须是 PNG/JPEG base64: " + n.asset); }
      else if (!Array.isArray(a.crop) || a.crop.length !== 4 || !a.crop.every(finite) || a.crop[0] < 0 || a.crop[1] < 0 || a.crop[2] <= a.crop[0] || a.crop[3] <= a.crop[1]) fail("图片需要 data 或原始像素 crop:[left,top,right,bottom]: " + n.asset);
    }
  }
  for (const [key,b] of Object.entries(scene.panelBounds || {})) if (!Array.isArray(b) || b.length !== 4 || !b.every(finite) || b[2] <= 0 || b[3] <= 0) fail("分区边界无效: " + key);
  for (const f of scene.visualFeatures || []) for (const [i,id] of (f.nodeIds || []).entries()) {
    const n = scene.nodes[ids.get(id)];
    if (!n) fail("缺少标记的视觉细节: " + id);
    if (f.kind === "linear_gradient") { if (n.type !== "rect" || n.fill?.type !== "linear") fail("渐变被简化: " + id); }
    else if (f.kind === "translucent_backplate") {
      const label = f.labelIds?.[i];
      if (n.type !== "rect" || n.fill !== "#ffffff" || !(n.opacity > 0 && n.opacity < 1) || !ids.has(label) || ids.get(id) >= ids.get(label)) fail("半透明白色打底缺失或层级错误: " + id);
    } else if (f.kind === "curve") { if (n.type !== "svg" || !/\bd\s*=\s*["'][^"']*[CQcq]/.test(n.svg)) fail("曲线被简化: " + id); }
    else fail("未知视觉细节类型: " + f.kind);
  }
  return {nodes:scene.nodes.length,types:counts,panels:panels.size};
}
