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
