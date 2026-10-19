import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PartialBundleTests(unittest.TestCase):
    def test_large_planwam_panel_can_be_transferred_without_geometry_changes(self):
        root=Path(__file__).resolve().parents[1]
        source=root/'examples/planwam/planwam.scene.json'
        scene=json.loads(source.read_text(encoding='utf-8'))
        expected=[n for n in scene['nodes'] if n.get('panel')=='d']
        with tempfile.TemporaryDirectory() as directory:
            mapping=Path(directory)/'hashes.json'
            mapping.write_text(json.dumps({key:'uploaded-test-hash' for key in scene['assets']}),encoding='utf-8')
            transferred=[]
            for start in range(0,len(expected),80):
                output=Path(directory)/f'part-{start}.js'
                result=subprocess.run([sys.executable,str(Path(__file__).with_name('bundle_figma.py')),str(source),str(output),'--panel','d','--node-range',f'{start}:{start+80}','--image-hashes',str(mapping),'--root-id','test-target'],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                code=output.read_text(encoding='utf-8')
                self.assertLessEqual(len(code),50000)
                call=code.rsplit('return await importFigureScene(',1)[1]
                part,_=json.JSONDecoder().raw_decode(call)
                transferred.extend(part['nodes'])
            self.assertEqual(transferred,expected)

    def test_upload_response_object_is_rejected_before_execution(self):
        scene={'version':1,'name':'rgb','width':20,'height':20,
               'assets':{'photo':{'role':'input_rgb','mime':'image/png','data':''}},
               'nodes':[{'id':'rgb','name':'RGB','type':'image','role':'input_rgb','asset':'photo','x':0,'y':0,'w':10,'h':10}]}
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'scene.json';mapping=Path(directory)/'hashes.json';output=Path(directory)/'bundle.js'
            source.write_text(json.dumps(scene),encoding='utf-8')
            mapping.write_text(json.dumps({'photo':{'imageHash':'nested-response'}}),encoding='utf-8')
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('bundle_figma.py')),str(source),str(output),'--image-hashes',str(mapping)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('non-empty string',result.stderr)
            self.assertFalse(output.exists())

    def test_panel_bundle_only_checks_features_in_its_panel(self):
        scene={'version':1,'name':'panel test','width':100,'height':100,'assets':{},'nodes':[
            {'id':'a','panel':'a','type':'rect','name':'A','x':0,'y':0,'w':10,'h':10,
             'fill':{'type':'linear','stops':[{'offset':0,'color':'#000000'},{'offset':1,'color':'#ffffff'}]}},
            {'id':'b','panel':'b','type':'rect','name':'B','x':20,'y':0,'w':10,'h':10,
             'fill':{'type':'linear','stops':[{'offset':0,'color':'#000000'},{'offset':1,'color':'#ffffff'}]}}
        ],'visualFeatures':[{'kind':'linear_gradient','nodeIds':['a','b']}]}
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'scene.json'
            output=Path(directory)/'bundle.js'
            source.write_text(json.dumps(scene),encoding='utf-8')
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('bundle_figma.py')),str(source),str(output),'--panel','a'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            call=output.read_text(encoding='utf-8').rsplit('return await importFigureScene(',1)[1]
            filtered,offset=json.JSONDecoder().raw_decode(call)
            options=json.loads(call[offset+1:].removesuffix(');\n'))
            self.assertEqual(filtered['visualFeatures'][0]['nodeIds'],['a'])
            self.assertTrue(options['partial'])


if __name__=='__main__':
    unittest.main()
