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
  for (const n of scene.nodes.filter(n => n.type === "image")) if (typeof options.imageHashes?.[n.asset] !== "string" || !options.imageHashes[n.asset].trim()) throw new Error("缺少有效的已上传图片标识: " + n.asset);
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
