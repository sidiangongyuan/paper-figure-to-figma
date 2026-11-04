// Offline interactive preview of the actual reviewed Figma export.
const $=id=>document.getElementById(id);
let scene=structuredClone(SHOWCASE.scene),selected='d-0368',timers=[],toastTimer,playing=false;
const originalFigure=$('drawing').innerHTML;
const initialView='0 0 1452 514';
const getSvg=()=>$('drawing').querySelector('svg');
const modelNode=id=>scene.nodes.find(n=>n.id===id);
const viewNode=id=>$('drawing').querySelector('[data-figure-node="'+id+'"]');
const captions=['完整参考图','文字、模块与连线图层','原图与重建对照','编辑与下载'];
function toast(message){clearTimeout(toastTimer);$('toast').textContent=message;$('toast').hidden=false;toastTimer=setTimeout(()=>$('toast').hidden=true,3500);}
function stopReplay(){timers.forEach(clearTimeout);timers=[];playing=false;$('studio').classList.remove('is-playing');$('replay').innerHTML='<span aria-hidden="true">▷</span> 播放流程';$('replay').setAttribute('aria-label','播放流程回放');}
function markStep(index){document.querySelectorAll('[data-step]').forEach(b=>{const active=Number(b.dataset.step)===index;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});$('canvas-caption').textContent=captions[index];}
function setView(mode){$('studio').dataset.mode=mode;document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===mode)));$('comparison-control').hidden=mode!=='compare';$('selection-box').hidden=mode!=='edit';if(mode!=='edit')resetView();if(mode==='original'||mode==='layers')$('reference-layer').style.clipPath='inset(0)';else if(mode==='compare')setComparison($('comparison').value);if(mode==='edit')drawSelection();}
function setStage(index){markStep(index);setView(['original','layers','compare','edit'][index]);if(index===2)setComparison(46);if(index===3)selectLayer(selected,{interrupt:false});}
function resetView(){getSvg().setAttribute('viewBox',initialView);$('selection-overlay').setAttribute('viewBox',initialView);$('reset-view').hidden=true;}
function zoomTo(node){
  const width=Math.max(480,node.w+210),height=width/(1452/514),cx=node.x+node.w/2,cy=node.y+node.h/2;
  const x=Math.max(0,Math.min(1452-width,cx-width/2)),y=Math.max(0,Math.min(514-height,cy-height/2));
  const view=[x,y,width,height].join(' ');getSvg().setAttribute('viewBox',view);$('selection-overlay').setAttribute('viewBox',view);$('reset-view').hidden=false;
}
function drawSelection(){
  const element=viewNode(selected),box=$('selection-box');if(!element)return;
  const b=element.getBBox(),rootInverse=getSvg().getCTM().inverse(),matrix=element.getCTM();
  const points=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y])=>new DOMPoint(x,y).matrixTransform(matrix).matrixTransform(rootInverse));
  const x=Math.min(...points.map(p=>p.x)),y=Math.min(...points.map(p=>p.y));
  box.setAttribute('x',x-4);box.setAttribute('y',y-4);box.setAttribute('width',Math.max(8,Math.max(...points.map(p=>p.x))-x)+8);box.setAttribute('height',Math.max(8,Math.max(...points.map(p=>p.y))-y)+8);box.hidden=$('studio').dataset.mode!=='edit';
}
function selectLayer(id,{interrupt=true,zoom=true}={}){
  const node=modelNode(id);if(!node||!viewNode(id)||node.type==='image')return;
  if(interrupt)stopReplay();selected=id;setView('edit');markStep(3);
  document.querySelectorAll('[data-select]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.select===id)));
  $('text-fields').hidden=node.type!=='text';$('color-fields').hidden=node.type!=='rect';$('curve-fields').hidden=id!=='d-0279';
  if(node.type==='text')$('label-text').value=node.text.replaceAll('\n',' ');
  if(node.type==='rect'){
    const fill=typeof node.fill==='object'?node.fill.stops[0].color:/^#[a-f0-9]{6}$/i.test(node.fill||'')?node.fill:'#ffffff';
    $('fill-color').value=fill;$('color-value').textContent=fill.toUpperCase();
    $('color-fields').querySelector('label').textContent=typeof node.fill==='object'?'渐变起始颜色':'填充颜色';
  }
  if(zoom)zoomTo(node);drawSelection();$('canvas-hint').textContent='当前选择：'+(node.type==='text'?'文字':node.type==='rect'?'填色':'矢量路径')+' · '+node.name.replaceAll(' / ',' ');
}
function setComparison(value){const n=Math.max(0,Math.min(100,Number(value)));$('comparison').value=n;$('reference-layer').style.clipPath='inset(0 '+(100-n)+'% 0 0)';$('divider').style.left=n+'%';}
function applyText(value){
  const node=modelNode(selected),element=viewNode(selected);if(!node||node.type!=='text'||!element)return;
  node.text=value;
  const spans=element.querySelectorAll('tspan');
  if(spans.length){spans[0].textContent=value;for(const extra of [...spans].slice(1))extra.remove();}
  else element.textContent=value;
  $('label-text').value=value;drawSelection();
}
function applyColor(value){
  const node=modelNode(selected),element=viewNode(selected);if(!node||node.type!=='rect')return;
  if(typeof node.fill==='object'){
    node.fill.stops[0].color=value;
    const paint=element.getAttribute('fill')||element.querySelector('[fill]')?.getAttribute('fill')||'';
    const id=paint.match(/url\(#([^)]*)\)/)?.[1];
    const gradient=id?getSvg().querySelector('[id="'+id+'"]'):null;
    if(gradient?.querySelector('stop'))gradient.querySelector('stop').setAttribute('stop-color',value);
  }else{node.fill=value;element.setAttribute('fill',value);}
  $('color-value').textContent=value.toUpperCase();
}
function bendPath(path,amount){return path.replace(/C\s*([-+.\deE]+)[ ,]+([-+.\deE]+)[ ,]+([-+.\deE]+)[ ,]+([-+.\deE]+)[ ,]+([-+.\deE]+)[ ,]+([-+.\deE]+)/,(_,x1,y1,x2,y2,x,y)=>'C'+[x1,Number(y1)+amount,x2,Number(y2)+amount,x,y].join(' '));}
let curveBaseline=null;
function changeCurve(amount){
  const node=modelNode('d-0279'),target=viewNode('d-0279');
  if(!curveBaseline){const path=[...target.querySelectorAll('path')].find(p=>/[CQ]/.test(p.getAttribute('d')||''));curveBaseline={native:path?.getAttribute('d'),source:node.svg};}
  if(!curveBaseline.native)return;
  const path=[...target.querySelectorAll('path')].find(p=>/[CQ]/.test(p.getAttribute('d')||''));path.setAttribute('d',bendPath(curveBaseline.native,Number(amount)));
  const xml=new DOMParser().parseFromString(curveBaseline.source,'image/svg+xml');const sourcePath=[...xml.querySelectorAll('path')].find(p=>/C/.test(p.getAttribute('d')||''));
  if(sourcePath){const view=xml.documentElement.getAttribute('viewBox').split(/[ ,]+/).map(Number),scale=node.h/view[3];sourcePath.setAttribute('d',bendPath(sourcePath.getAttribute('d'),Number(amount)/scale));node.svg=new XMLSerializer().serializeToString(xml.documentElement);}
  drawSelection();
}
function download(content,type,name){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}
function exportSvg(){const svg=getSvg().cloneNode(true);svg.setAttribute('viewBox',initialView);svg.setAttribute('width','1452');svg.setAttribute('height','514');for(const e of svg.querySelectorAll('[data-figure-node]')){e.removeAttribute('data-figure-node');e.removeAttribute('data-kind');}download(new XMLSerializer().serializeToString(svg),'image/svg+xml','planwam-editable.svg');toast('SVG 已下载。');}
function resetEdits(){stopReplay();scene=structuredClone(SHOWCASE.scene);$('drawing').innerHTML=originalFigure;curveBaseline=null;$('curve-bend').value=0;selected='d-0368';selectLayer(selected,{zoom:false});resetView();toast('已恢复 PlanWAM 示例。');}
function replay(){
  if(playing){stopReplay();return;}
  resetEdits();$('toast').hidden=true;playing=true;$('studio').classList.add('is-playing');$('replay').innerHTML='<span aria-hidden="true">Ⅱ</span> 暂停回放';$('replay').setAttribute('aria-label','暂停流程回放');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduced){setStage(3);stopReplay();return;}
  setStage(0);timers.push(setTimeout(()=>setStage(1),1800));timers.push(setTimeout(()=>setStage(2),3600));
  for(let i=0;i<=12;i++)timers.push(setTimeout(()=>setComparison(12+i*6),3800+i*80));
  timers.push(setTimeout(()=>setStage(3),5500));
  const text='My planner';for(let i=0;i<=text.length;i++)timers.push(setTimeout(()=>applyText(text.slice(0,i)),6400+i*90));
  timers.push(setTimeout(()=>{stopReplay();$('canvas-caption').textContent='文字已修改，可下载 SVG。';},7800));
}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{stopReplay();setView(b.dataset.view);markStep(b.dataset.view==='original'?0:b.dataset.view==='compare'?2:3);if(b.dataset.view==='edit')selectLayer(selected);});
document.querySelectorAll('[data-step]').forEach(b=>b.onclick=()=>{stopReplay();setStage(Number(b.dataset.step));});
document.querySelectorAll('[data-select]').forEach(b=>b.onclick=()=>selectLayer(b.dataset.select));
$('comparison').oninput=e=>{stopReplay();setComparison(e.target.value);};
let dragging=false;
$('artboard').addEventListener('pointerdown',e=>{if($('studio').dataset.mode==='compare'){dragging=true;$('artboard').setPointerCapture(e.pointerId);slideAt(e.clientX);}});
$('artboard').addEventListener('pointermove',e=>{if(dragging)slideAt(e.clientX);});
$('artboard').addEventListener('pointerup',()=>dragging=false);
$('artboard').addEventListener('pointercancel',()=>dragging=false);
function slideAt(x){stopReplay();const r=$('artboard').getBoundingClientRect();setComparison((x-r.left)/r.width*100);}
$('drawing').onclick=e=>{if($('studio').dataset.mode==='edit'){const id=e.target.closest('[data-figure-node]')?.dataset.figureNode;if(id)selectLayer(id);}};
$('label-text').oninput=e=>{stopReplay();setView('edit');applyText(e.target.value);};
$('fill-color').oninput=e=>{stopReplay();applyColor(e.target.value);};
$('curve-bend').oninput=e=>{stopReplay();changeCurve(e.target.value);};
$('reset-view').onclick=()=>{resetView();drawSelection();};
$('reset-edits').onclick=resetEdits;
$('download-svg').onclick=exportSvg;
$('download-project').onclick=()=>{download(JSON.stringify(scene,null,2),'application/json','planwam.scene.json');toast('绘图文件已下载。');};
$('replay').onclick=replay;
$('hero-play').onclick=()=>{setTimeout(replay,450);};
$('copy-codex').onclick=async()=>{
  const text='使用 $paper-figure-to-figma 复现我上传的整张科研图，完成 Figma 绘制和预览复核，交付可编辑画板链接。';
  try{await navigator.clipboard.writeText(text);toast('指令已复制。');}
  catch(_){$('copy-text').value=text;$('copy-dialog').showModal();$('copy-text').select();}
};
window.addEventListener('resize',()=>{if($('studio').dataset.mode==='edit')drawSelection();});
setComparison(46);markStep(2);setView('compare');
