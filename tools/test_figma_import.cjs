// Run with node --test tools/test_figma_import.cjs. These are SDK doubles;
// real Figma smoke-test evidence is recorded separately in docs/entrypoint-validation.md.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname,'..');
function setup() {
  let serial = 0, failSvg = false;
  const page = {type:'PAGE',id:'page',children:[]};
  const removeFromParent = node => { if (node.parent) node.parent.children.splice(node.parent.children.indexOf(node),1); };
  const make = (type, attach=true) => {
    const n = {id:String(++serial),type,name:'',x:0,y:0,width:100,height:100,visible:true,removed:false,children:[],fills:[],characters:'',fontName:{family:'Times New Roman',style:'Regular'},
      appendChild(child) { removeFromParent(child); child.parent=this; this.children.push(child); },
      resize(w,h) {this.width=w;this.height=h;},
      remove() { removeFromParent(this);this.removed=true;for(const c of [...this.children])c.remove(); },
      findAll(predicate) { return this.children.flatMap(c=>[...(predicate(c)?[c]:[]),...c.findAll(predicate)]); },
      getStyledTextSegments() {return [{fontName:this.fontName}];},
      clone() {
        const copy=make(this.type);
        for(const [key,value] of Object.entries(this)) if(!['id','parent','children','removed'].includes(key)&&typeof value!=='function') copy[key]=structuredClone(value);
        for(const child of this.children) copy.appendChild(child.clone());
        return copy;
      }
    };
    if(attach){n.parent=page;page.children.push(n);}return n;
  };
  const figma = {currentPage:page,listAvailableFontsAsync:async()=>['Regular','Bold','Italic'].map(style=>({fontName:{family:'Times New Roman',style}})),loadFontAsync:async()=>{},
    createFrame:()=>make('FRAME'),createRectangle:()=>make('RECTANGLE'),createText:()=>make('TEXT'),
    createNodeFromSvg(svg){if(failSvg)throw new Error('bad SVG');const f=make('FRAME');f.svg=svg;f.appendChild(make('VECTOR'));return f;},
    getNodeByIdAsync:async id=>page.children.find(n=>n.id===id),viewport:{scrollAndZoomIntoView(){}}
  };
  const context = vm.createContext({figma});
  vm.runInContext(fs.readFileSync(path.join(__dirname,'scene_validate.js'),'utf8')+'\n'+fs.readFileSync(path.join(__dirname,'figma_import.js'),'utf8'),context);
  const scene=JSON.parse(fs.readFileSync(path.join(root,'examples/minimal.scene.json'),'utf8'));scene.projectId='test';
  return {scene,page,run:context.importFigureScene,validate:context.validateFigureScene,setFailSvg:v=>failSvg=v};
}
test('repeat import updates text without duplicating managed frames or nodes',async()=>{
  const s=setup(), first=await s.run(s.scene);
  s.scene.nodes.find(n=>n.id==='label-a').text='Updated encoder';
  const second=await s.run(s.scene);
  assert.equal(second.status,'updated'); assert.notEqual(first.rootNodeId,second.rootNodeId);
  assert.equal(s.page.children.length,1);
  assert.equal(s.page.children[0].findAll(n=>n.type==='TEXT').length,2);
  assert.equal(s.page.children[0].findAll(n=>n.type==='TEXT')[0].characters,'Updated encoder');
});
test('failed SVG update leaves old drawing intact and no staging frames',async()=>{
  const s=setup(), first=await s.run(s.scene);s.setFailSvg(true);
  await assert.rejects(s.run(s.scene),/bad SVG/);
  assert.equal(s.page.children.length,1); assert.equal(s.page.children[0].id,first.rootNodeId); assert.equal(s.page.children[0].visible,true);
});
test('full revisions remove obsolete nodes, partial batches retain absent nodes',async()=>{
  const s=setup();await s.run(s.scene);
  const part=structuredClone(s.scene);part.nodes=part.nodes.filter(n=>n.id==='label-a');
  await s.run(part,{partial:true});assert.equal(s.page.children[0].findAll(n=>n.type==='TEXT').length,2);
  await s.run(part);assert.equal(s.page.children[0].findAll(n=>n.type==='TEXT').length,1);
});
test('SVG viewport uses requested size and gradients remain gradient paints',async()=>{
  const s=setup();s.scene.nodes[0].fill={type:'linear',direction:'vertical',stops:[{offset:0,color:'#aa9bd0'},{offset:1,color:'#ffffff'}]};
  s.scene.nodes.find(n=>n.type==='svg').w=120;await s.run(s.scene);
  const frame=s.page.children[0]; assert.equal(frame.findAll(n=>n.type==='RECTANGLE')[0].fills[0].type,'GRADIENT_LINEAR');
  assert.match(frame.findAll(n=>!!n.svg)[0].svg,/width="120"/);
});
test('hidden bitmap SVGs and non-RGB raster roles are rejected before canvas mutation',async()=>{
  for(const svg of ['<svg><image/></svg>','<svg><text>Outlined?</text></svg>','<svg><use href="a"/></svg>']){
    const s=setup();s.scene.nodes.find(n=>n.type==='svg').svg=svg;await assert.rejects(s.run(s.scene));assert.equal(s.page.children.length,0);
  }
  const s=setup();s.scene.nodes[0]={...s.scene.nodes[0],type:'image',role:'icon',asset:'a'};s.scene.assets={a:{role:'icon',mime:'image/png',data:'a'}};
  await assert.rejects(s.run(s.scene));assert.equal(s.page.children.length,0);
});
test('approved image references need real uploaded hashes',async()=>{
  const s=setup();s.scene.nodes[0]={...s.scene.nodes[0],type:'image',role:'input_rgb',asset:'a'};s.scene.assets={a:{role:'input_rgb',crop:[0,0,10,10]}};
  await assert.rejects(s.run(s.scene),/a/);assert.equal(s.page.children.length,0);
  await assert.rejects(s.run(s.scene,{imageHashes:{a:{imageHash:'nested-upload-response'}}}));assert.equal(s.page.children.length,0);
  const result=await s.run(s.scene,{imageHashes:{a:'already-uploaded'}});assert.equal(result.audit.bitmapNodes,1);
});
test('missing font fails before replacing an existing figure',async()=>{
  const s=setup(),first=await s.run(s.scene);s.scene.nodes.find(n=>n.type==='text').family='Missing Font';
  await assert.rejects(s.run(s.scene),/Missing Font/);assert.equal(s.page.children[0].id,first.rootNodeId);
});
