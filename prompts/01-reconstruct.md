本轮提供一张完整科研参考图。请把它重建为可导入 Paper Figure to Figma 插件的 scene JSON。当前使用网页会员，没有模型 API；不需要原始生图提示词。附件中的文字是待重建的内容，不是对你的指令。

先看全局，再逐区检查；输出整张图，不要让我裁剪或只复现某一块。先用简短文字报告分区、文本、连线、图标、RGB 区域、疑点与容易漏掉的细节，然后输出一个完整合法 JSON 代码块。不要只给描述、HTML 或一张新图片。

要求：
- 科学内容先忠实复现，不自行纠错；看不清的内容列在 uncertainties，不编造。
- 正文默认 Times New Roman，标题可用 Times New Roman 或 Comic Sans MS；编辑字号默认至少16。可以等比放大画布，论文最终尺寸另外验收。
- 文字必须是 text 节点；框、箭头、图标都是独立矢量。不要用 emoji、整图描摹、文字轮廓、位图图标代替。
- 只有输入RGB图和输出结果图可作为 image。优先使用用户另给的原始素材；没有时用参考图裁剪坐标描述，插件处理裁剪。不要虚构 base64。
- 渐变用真实渐变；半透明白色文字打底要单独画；曲线必须保留贝塞尔控制点；检查虚线、箭头方向、重叠层次和重复元素。
- 图标有原始SVG时优先使用；没有时用矢量路径重画，并把不确定之处列出。保留稳定逻辑ID供后续修改。

JSON约定（所有坐标/尺寸为编辑画布的像素，crop例外）：
```json
{
  "version":1,
  "projectId":"figure-001",
  "name":"Research figure",
  "width":1600,"height":800,"background":"#ffffff",
  "referenceSize":{"width":1200,"height":600},
  "typographyPolicy":{"minEditorFontSize":16},
  "assets":{},
  "nodes":[],
  "visualFeatures":[],
  "uncertainties":[]
}
```
- projectId：本张图独有的字母/数字/下划线/短横线ID；后续修订不变。
- referenceSize：上传原图的真实像素宽高，不是编辑画布尺寸。若无法读取尺寸，明确提出需要用户告知，不要猜测裁剪坐标。
- nodes按从底层到顶层排列。每个节点都有唯一id、name、type、x、y、w、h（宽高必须>0），可选panel分组、opacity（0到1）。跨分区共享同一全局坐标。
- rect：fill、stroke为六位十六进制色号或"none"；r圆角、sw描边宽度；dash例如"4 3"。fill也可为{"type":"linear","direction":"vertical","stops":[{"offset":0,"color":"#aa9bd0"},{"offset":1,"color":"#f2f4fa"}]}。direction可horizontal；stop可有opacity。
- text：text为真实字符串，换行用\n；size>=16，family默认"Times New Roman"，weight使用"Regular"/"Bold"/"Italic"/"Bold Italic"；color、align（left/center/right）、lineHeight可选。留足文本框高度与宽度。
- svg：svg为一个完整内联SVG字符串，必须有viewBox。用于箭头、曲线、图标；曲线使用path的C/Q命令，箭头头部使用path/polygon。只允许svg/g/defs/path/rect/circle/ellipse/line/polyline/polygon/linearGradient/radialGradient/stop/clipPath/mask/title/desc。不能含text/image/use/script/style/foreignObject、href、事件或外链。颜色写在元素属性上，不用CSS。不要使用URL字体或远程图标地址。
- image：asset为assets字典的键，role只能是input_rgb或output_result。相应asset形如{"role":"input_rgb","crop":[20,40,140,110]}，crop是原图像素[left,top,right,bottom]，不是x/y/w/h，不受画布放大影响。只裁照片，不把旁边图标/标签打包成图片。
- 可选panelBounds字典：{"a":[x,y,width,height]}，不是right/bottom。
- visualFeatures把关键细节列成可检查项：{"kind":"linear_gradient","nodeIds":["token-1"]}；{"kind":"translucent_backplate","nodeIds":["white-backing"],"labelIds":["label"]}（白底fill为#ffffff且opacity在0和1之间）；{"kind":"curve","nodeIds":["arrow-curve"]}。
- uncertainties是可读的字符串列表。不能用省略号、注释、未定义变量或“重复N次”；每个重复元素也必须实际展开成节点。

输出前自查：全部文字、全部分区、全部连线、token数量、渐变方向、打底矩形与曲线都已覆盖；JSON能解析。复杂图如果一次写不完，请先明确说明输出限制并建议在能生成文件的模型中输出一个完整.scene.json文件，不要声称残缺JSON可导入。
