// Bundle with a validated scene and asset hashes, then run in use_figma.
// Entry point: await importFigureScene(scene, {imageHashes: {...}}).
// For a local Figma plugin, import raster bytes with createImage BEFORE
// calling this function. MCP use_figma must receive hashes from upload_assets.
async function importFigureScene(scene, options) {
  const page = figma.currentPage;
  const title = options.name || "Pilot 01 — Editable reconstruction";
  const prior = page.children.find(n => n.name === title);
  if (prior && !options.rootId) {
    return {existingRootId: prior.id, status: "exists; inspect before updating", createdNodeIds: []};
  }
  const available = await figma.listAvailableFontsAsync();
  const fontKeys = new Set(available.map(f => JSON.stringify(f.fontName)));
  const requested = [...new Map(scene.nodes.filter(n => n.type === "text").map(n => {
    const font = {family: n.family || "Times New Roman", style: n.weight || "Regular"};
    return [JSON.stringify(font), font];
  })).values()];
  for (const font of requested) {
    if (!fontKeys.has(JSON.stringify(font))) throw new Error("Font unavailable: " + JSON.stringify(font));
  }
  await Promise.all(requested.map(f => figma.loadFontAsync(f)));
  const rgb = hex => {
    const h = hex.replace("#", "");
    return {r:parseInt(h.slice(0,2),16)/255,g:parseInt(h.slice(2,4),16)/255,b:parseInt(h.slice(4,6),16)/255};
  };
  const paint = color => {
    if (!color || color === "none") return [];
    if (typeof color === "object") {
      if (color.type !== "linear") throw new Error("Unsupported gradient type");
      return [{type:"GRADIENT_LINEAR",gradientTransform:color.direction === "horizontal" ? [[1,0,0],[0,1,0]] : [[0,1,0],[-1,0,1]],
        gradientStops:color.stops.map(s=>({position:s.offset,color:{...rgb(s.color),a:s.opacity ?? 1}}))}];
    }
    return [{type:"SOLID",color:rgb(color)}];
  };
  // Validate every image reference before creating anything on canvas.
  for (const n of scene.nodes.filter(n => n.type === "image")) {
    if (!["input_rgb", "output_result"].includes(n.role)) throw new Error("Unapproved raster role: " + n.id);
    if (!options.imageHashes[n.asset]) throw new Error("Missing uploaded image: " + n.asset);
  }
  const created = [], nodeMap = {}, panels = {};
  const root = options.rootId ? await figma.getNodeByIdAsync(options.rootId) : figma.createFrame();
  if (!root || root.type !== "FRAME") throw new Error("Missing target frame");
  if (!options.rootId) {
    created.push(root.id); root.name=title; root.resize(scene.width,scene.height);
    root.x=Math.max(0,...page.children.filter(n=>n.id!==root.id).map(n=>n.x+n.width))+100;
    root.y=100; root.fills=paint(scene.background || "#ffffff"); root.clipsContent=false;
  }
  root.placeholder=true;
  const bounds = {canvas:[0,0,scene.width,scene.height],...(scene.panelBounds || {})};
  for (const n of scene.nodes) {
    const key = n.panel || "canvas";
    if (!panels[key]) {
      const panelName=key === "canvas" ? "Panel separators" : "Panel (" + key + ")";
      const existingPanel=root.children.find(child=>child.name===panelName);
      if (existingPanel) panels[key]=existingPanel;
      else {
      const b = bounds[key] || bounds.canvas;
      const f = figma.createFrame(); created.push(f.id);
      f.name = panelName;
      root.appendChild(f); f.resize(b[2],b[3]); f.x=b[0]; f.y=b[1];
      f.fills=[]; f.clipsContent=false; panels[key]=f;
      }
    }
    const parent=panels[key];
    const existingNode=parent.children.find(child=>child.name.startsWith(n.id+" · "));
    if (existingNode) {nodeMap[n.id]=existingNode.id; continue;}
    let node;
    if (n.type === "rect" || n.type === "image") {
      node=figma.createRectangle();
      node.resize(n.w,n.h);
      node.fills=n.type === "image" ? [{type:"IMAGE",imageHash:options.imageHashes[n.asset],scaleMode:"FILL"}] : paint(n.fill);
      node.strokes=paint(n.stroke); node.strokeWeight=n.sw || 1; node.strokeAlign="CENTER";
      node.cornerRadius=n.r || 0;
      if (n.dash) node.dashPattern=n.dash.split(/[ ,]+/).map(Number);
    } else if (n.type === "text") {
      node=figma.createText();
      node.fontName={family:n.family || "Times New Roman",style:n.weight || "Regular"};
      node.fontSize=n.size; node.lineHeight={unit:"PIXELS",value:n.lineHeight || n.size*1.12};
      node.fills=paint(n.color || "#000000");
      node.characters=n.text;
      node.textAlignHorizontal=(n.align || "center").toUpperCase();
      node.textAutoResize="HEIGHT"; node.resize(n.w,n.h);
    } else if (n.type === "svg") {
      node=figma.createNodeFromSvg(n.svg);
      node.resize(n.w,n.h);
      // Icons remain vector paths, never raster fills or flattened screenshots.
      for (const child of node.findAll(() => true)) created.push(child.id);
    } else throw new Error("Unsupported scene type: " + n.type);
    created.push(node.id); node.name=n.id+" · "+n.name;
    node.opacity=n.opacity ?? 1;
    parent.appendChild(node); node.x=n.x-parent.x; node.y=n.y-parent.y;
    nodeMap[n.id]=node.id;
  }
  root.placeholder=false;
  figma.viewport.scrollAndZoomIntoView([root]);
  const all=root.findAll(() => true);
  const textNodes=all.filter(n => n.type === "TEXT");
  const bitmapNodes=all.filter(n => "fills" in n && Array.isArray(n.fills) && n.fills.some(p => p.type === "IMAGE"));
  const allowed=new Set(options.allowedRasterIds || scene.nodes.filter(n=>n.type==="image").map(n=>n.id));
  const unexpected=bitmapNodes.filter(n => !allowed.has(n.name.split(" · ")[0]));
  return {rootNodeId:root.id, createdNodeIds:[...new Set(created)], mutatedNodeIds:options.rootId?[root.id]:[], nodeMap,
    bounds:{width:root.width,height:root.height},
    audit:{texts:textNodes.length,bitmapNodes:bitmapNodes.length,unexpectedBitmaps:unexpected.map(n=>n.id),
      vectorPaths:all.filter(n=>n.type==="VECTOR").length,
      missingFonts:figma.hasMissingFont},status:"created"};
}
