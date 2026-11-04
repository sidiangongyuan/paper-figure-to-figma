"""Bundle an authored scene for Figma MCP use_figma (50,000-character cap)."""
import argparse
import json
from pathlib import Path

from scene_to_svg import validate_scene


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--image-hashes',type=Path,help='JSON object mapping asset IDs to hashes returned by upload_assets')
    parser.add_argument('--panel',action='append',help='Include only this panel; repeat for several panels')
    parser.add_argument('--node-range',help='Zero-based START:END slice after panel filtering; end is exclusive')
    parser.add_argument('--root-id',help='Append to this existing frame after inspecting it')
    parser.add_argument('--name',default='Research figure — Editable reconstruction')
    args=parser.parse_args()
    scene=json.loads(args.scene.read_text(encoding='utf-8'))
    validate_scene(scene)
    # Provenance stays in the portable scene; it is not needed by the canvas importer.
    scene.pop('assetSources', None)
    scene.pop('revisionNotes', None)
    for node in scene['nodes']:
        node.pop('iconSource', None)
    options={'name':args.name,'imageHashes':json.loads(args.image_hashes.read_text(encoding='utf-8')) if args.image_hashes else {},
             'allowedRasterIds':[n['id'] for n in scene['nodes'] if n['type']=='image']}
    if not isinstance(options['imageHashes'],dict):
        parser.error('Image hash mapping must be a JSON object')
    if args.root_id:
        options['rootId']=args.root_id
    # Keep descriptors for the common validator, without putting image bytes in MCP code.
    scene['assets']={key:{'role':asset['role'],'mime':asset.get('mime','image/png'),'data':''}
                     for key,asset in scene.get('assets',{}).items()}
    if args.panel:
        scene['nodes']=[n for n in scene['nodes'] if n.get('panel','canvas') in args.panel]
        if not scene['nodes']:
            parser.error('Selected panels contain no nodes')
    if args.node_range:
        try:
            start,end=(int(v) for v in args.node_range.split(':'))
            if start<0 or end<=start:
                raise ValueError()
        except ValueError:
            parser.error('--node-range must be START:END with 0 <= START < END')
        scene['nodes']=scene['nodes'][start:end]
        if not scene['nodes']:
            parser.error('Selected node range contains no nodes')
    if args.panel or args.node_range:
        options['partial']=True
        included={n['id'] for n in scene['nodes']}
        features=[]
        for feature in scene.get('visualFeatures',[]):
            indices=[i for i,key in enumerate(feature['nodeIds']) if key in included
                     and (feature['kind']!='translucent_backplate' or feature['labelIds'][i] in included)]
            if indices:
                filtered={**feature,'nodeIds':[feature['nodeIds'][i] for i in indices]}
                if 'labelIds' in feature:
                    filtered['labelIds']=[feature['labelIds'][i] for i in indices]
                features.append(filtered)
        scene['visualFeatures']=features
    for n in scene['nodes']:
        if n['type']=='image' and n['asset'] not in options['imageHashes']:
            parser.error('Missing uploaded image hash: '+n['asset'])
        if n['type']=='image' and (not isinstance(options['imageHashes'][n['asset']],str) or not options['imageHashes'][n['asset']].strip()):
            parser.error('Image hash must be a non-empty string for asset: '+n['asset']+'. Extract the imageHash field from the upload response.')
    code=Path(__file__).with_name('scene_validate.js').read_text(encoding='utf-8')+'\n'
    code+=Path(__file__).with_name('figma_import.js').read_text(encoding='utf-8')
    code+='\nreturn await importFigureScene('+json.dumps(scene,ensure_ascii=False,separators=(',',':'))+','+json.dumps(options,ensure_ascii=False)+');\n'
    if len(code)>50000:
        parser.error(f'Bundle has {len(code)} characters. Split with --panel or --node-range START:END, then append using the latest --root-id.')
    args.output.write_text(code,encoding='utf-8')
    print(json.dumps({'characters':len(code),'nodes':len(scene['nodes']),'output':str(args.output)}))


if __name__=='__main__':
    main()
