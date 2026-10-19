import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PartialBundleTests(unittest.TestCase):
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
