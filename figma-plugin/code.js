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

// Standard Plugin API, shared by the local plugin and MCP. MCP supplies hashes
// from upload_assets; the ordinary plugin creates hashes from local bytes.
async function importFigureScene(scene, options = {}) {
  validateFigureScene(scene);
  const page = figma.currentPage, title = options.name || scene.name || "Research figure";
  const marker = scene.projectId ? "[figure:" + scene.projectId + "] " : "";
  const matches = marker ? page.children.filter(n => n.name.startsWith(marker)) : [];
  if (!options.rootId && matches.length > 1) throw new Error("存在多个同项目画板，请明确选择更新对象");
  const prior = options.rootId ? await figma.getNodeByIdAsync(options.rootId) : matches[0];
  if (options.rootId && (!prior || prior.type !== "FRAME" || prior.parent !== page)) throw new Error("更新对象必须是当前页中的完整画板");
  if (prior && prior.type !== "FRAME") throw new Error("同名项目不是画板");
  const fonts = new Map(), addFont = font => fonts.set(JSON.stringify(font), font);
  for (const n of scene.nodes.filter(n => n.type === "text")) addFont({family:n.family || "Times New Roman",style:n.weight || "Regular"});
  if (prior) for (const t of prior.findAll(n => n.type === "TEXT")) {
    if (t.characters.length) for (const s of t.getStyledTextSegments(["fontName"])) addFont(s.fontName);
    else if (typeof t.fontName === "object") addFont(t.fontName);
  }
  const available = new Set((await figma.listAvailableFontsAsync()).map(f => JSON.stringify(f.fontName)));
  for (const [key] of fonts) if (!available.has(key)) throw new Error("字体不可用，请安装或明确替换: " + key);
  await Promise.all([...fonts.values()].map(f => figma.loadFontAsync(f)));
  for (const n of scene.nodes.filter(n => n.type === "image")) if (!options.imageHashes?.[n.asset]) throw new Error("缺少已上传图片: " + n.asset);
  const rgb = hex => ({r:parseInt(hex.slice(1,3),16)/255,g:parseInt(hex.slice(3,5),16)/255,b:parseInt(hex.slice(5,7),16)/255});
  const paint = c => {
    if (!c || c === "none") return [];
    if (typeof c === "string") return [{type:"SOLID",color:rgb(c)}];
    return [{type:"GRADIENT_LINEAR",gradientTransform:c.direction === "horizontal" ? [[1,0,0],[0,1,0]] : [[0,1,0],[-1,0,1]],
      gradientStops:c.stops.map(s => ({position:s.offset,color:{...rgb(s.color),a:s.opacity ?? 1}}))}];
  };
  let root;
  const nodeMap = {};
  try {
    // A failed import leaves the previous drawing intact.
    root = prior ? prior.clone() : figma.createFrame(); root.visible = false;
    root.name = marker + title; root.resize(scene.width,scene.height);
    root.fills = paint(scene.background || "#ffffff"); root.clipsContent = false;
    if (prior && !options.partial) {
      const keep = new Set(scene.nodes.map(n => n.id));
      for (const old of root.findAll(n => n.name.includes(" · "))) if (!keep.has(old.name.split(" · ")[0]) && !old.removed) old.remove();
    }
    if (!prior) { root.x = Math.max(0,...page.children.filter(n => n.id !== root.id).map(n => n.x + n.width)) + 100; root.y = 100; }
    const panels = {}, bounds = {canvas:[0,0,scene.width,scene.height],...(scene.panelBounds || {})};
    for (const n of scene.nodes) {
      const key = n.panel || "canvas", panelName = key === "canvas" ? "Panel separators" : "Panel (" + key + ")";
      if (!panels[key]) {
        let f = root.children.find(child => child.name === panelName && child.type === "FRAME");
        if (!f) { f = figma.createFrame(); root.appendChild(f); }
        const b = bounds[key] || bounds.canvas;
        f.name = panelName; f.resize(b[2],b[3]); f.x = b[0]; f.y = b[1]; f.fills = []; f.clipsContent = false; panels[key] = f;
      }
      const parent = panels[key];
      for (const old of root.findAll(child => child.name.startsWith(n.id + " · "))) old.remove();
      let node;
      if (n.type === "rect" || n.type === "image") {
        node = figma.createRectangle(); parent.appendChild(node); node.resize(n.w,n.h);
        node.fills = n.type === "image" ? [{type:"IMAGE",imageHash:options.imageHashes[n.asset],scaleMode:"FILL"}] : paint(n.fill);
        node.strokes = paint(n.stroke); node.strokeWeight = n.sw ?? 1; node.strokeAlign = "CENTER";
        node.cornerRadius = n.r || 0; node.dashPattern = n.dash ? n.dash.split(/[ ,]+/).map(Number) : [];
      } else if (n.type === "text") {
        node = figma.createText(); parent.appendChild(node);
        node.fontName = {family:n.family || "Times New Roman",style:n.weight || "Regular"};
        node.fontSize = n.size; node.lineHeight = {unit:"PIXELS",value:n.lineHeight || n.size * 1.12};
        node.fills = paint(n.color || "#000000"); node.characters = n.text;
        node.textAlignHorizontal = (n.align || "center").toUpperCase(); node.textAutoResize = "HEIGHT"; node.resize(n.w,n.h);
      } else {
        // Resizing an SVG frame alone does not scale its paths. Set its viewport first.
        const svg = n.svg.replace(/<svg\b([^>]*)>/, (_, attrs) => '<svg' + attrs.replace(/\s(?:width|height)\s*=\s*["'][^"']*["']/g, "") + ' width="' + n.w + '" height="' + n.h + '">');
        node = figma.createNodeFromSvg(svg); parent.appendChild(node);
      }
      node.name = n.id + " · " + (n.name || n.id); node.opacity = n.opacity ?? 1;
      node.x = n.x - parent.x; node.y = n.y - parent.y; nodeMap[n.id] = node.id;
    }
    const all = root.findAll(() => true);
    const allowed = new Set(options.allowedRasterIds || scene.nodes.filter(n => n.type === "image").map(n => n.id));
    const bitmaps = all.filter(n => "fills" in n && Array.isArray(n.fills) && n.fills.some(p => p.type === "IMAGE"));
    if (bitmaps.some(n => !allowed.has(n.name.split(" · ")[0]))) throw new Error("检测到允许范围以外的图片层；原画板已保留");
    const deletedNodeIds = prior ? [prior.id,...prior.findAll(() => true).map(n => n.id)] : [];
    root.visible = true;
    if (prior) prior.remove();
    const result = {rootNodeId:root.id,createdNodeIds:[root.id,...all.map(n => n.id)],deletedNodeIds,mutatedNodeIds:[],nodeMap,
      bounds:{width:root.width,height:root.height},audit:{texts:all.filter(n => n.type === "TEXT").length,bitmapNodes:bitmaps.length,unexpectedBitmaps:[],vectorPaths:all.filter(n => n.type === "VECTOR").length},status:prior ? "updated" : "created"};
    try { figma.viewport.scrollAndZoomIntoView([root]); } catch (_) { /* Drawing is complete. */ }
    return result;
  } catch (error) { if (root && !root.removed) root.remove(); throw error; }
}

// Source for code.js. Rebuild with tools/build_plugin.py after changes.
figma.showUI(__html__, {width:520,height:740,themeColors:true});
let activeRootId = null, busy = false;
figma.ui.onmessage = async message => {
  if (busy) return figma.ui.postMessage({type:"error",message:"正在处理上一步，请稍候"});
  busy = true;
  try {
    if (message.type === "import") {
      const scene = message.scene;
      validateFigureScene(scene);
      const hashes = {};
      for (const [id,a] of Object.entries(scene.assets || {})) {
        if (scene.nodes.some(n => n.type === "image" && n.asset === id)) {
          if (!a.data) throw new Error("请先在插件中选择参考图，或为素材选择原始RGB文件: " + id);
          hashes[id] = figma.createImage(figma.base64Decode(a.data)).hash;
        }
      }
      const selected = figma.currentPage.selection;
      const selectedTarget = selected.length === 1 && selected[0].type === "FRAME" && selected[0].parent === figma.currentPage && selected[0].name.startsWith("[figure:" + scene.projectId + "] ") ? selected[0].id : undefined;
      const result = await importFigureScene(scene,{imageHashes:hashes,rootId:selectedTarget});
      activeRootId = result.rootNodeId;
      figma.currentPage.selection = [await figma.getNodeByIdAsync(activeRootId)];
      figma.ui.postMessage({type:"imported",result});
    } else if (message.type === "export") {
      const selected = figma.currentPage.selection;
      const root = activeRootId ? await figma.getNodeByIdAsync(activeRootId) : selected.length === 1 ? selected[0] : null;
      if (!root || root.type !== "FRAME" || !root.name.startsWith("[figure:")) throw new Error("请先生成画板，或选择本工具生成的完整画板");
      const kind = message.format;
      if (!["png","svg","outlined-svg","pdf"].includes(kind)) throw new Error("不支持的导出格式");
      const settings = kind === "png" ? {format:"PNG",constraint:{type:"SCALE",value:2}} : kind === "pdf" ? {format:"PDF"} : {format:"SVG",svgOutlineText:kind === "outlined-svg",svgIdAttribute:true};
      const bytes = await root.exportAsync(settings);
      figma.ui.postMessage({type:"exported",format:kind,base64:figma.base64Encode(bytes)});
    }
  } catch (error) {
    figma.ui.postMessage({type:"error",message:error.message || String(error)});
  } finally { busy = false; }
};
