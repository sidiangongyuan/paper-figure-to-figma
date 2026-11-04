import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from icon_assets import prepare, search, normalize_svg, catalog
from scene_to_svg import validate_scene

class IconAssetTests(unittest.TestCase):
    def test_all_bundled_assets_are_self_contained_vectors(self):
        for item in catalog()['icons']:
            with self.subTest(icon=item['id']):
                svg,info=prepare(item['id'])
                scene={'version':1,'width':100,'height':100,'nodes':[{'id':'asset','name':'Asset','type':'svg','x':0,'y':0,'w':24,'h':24,'svg':svg}]}
                validate_scene(scene)
                self.assertIn('sourceSha256',info)

    def test_semantic_lookup_and_prepared_source_fit_scene(self):
        self.assertIn('lucide:snowflake',[i['id'] for i in search('frozen')])
        svg,info=prepare('lucide:snowflake',color='#347baa')
        self.assertIn('#347baa',svg);self.assertNotIn('currentColor',svg)
        scene={'version':1,'width':100,'height':100,'nodes':[{'id':'frozen','name':'Frozen','type':'svg','x':0,'y':0,'w':32,'h':32,'svg':svg}]}
        self.assertEqual(validate_scene(scene)['types'],{'svg':1})
        self.assertIn('revision',info);self.assertIn('license',info)

    def test_forbidden_content_is_rejected(self):
        for child in ['<image href="data:image/png;base64,AA=="/>','<text>hidden label</text>',
                      '<script/>','<path onclick="alert(1)"/>','<path fill="url(https://example.com/a)"/>']:
            with self.subTest(child=child),self.assertRaises(ValueError):
                normalize_svg('<svg viewBox="0 0 24 24">'+child+'</svg>')

    def test_palette_and_internal_gradient_survive(self):
        src='<svg viewBox="0 0 24 24"><defs><linearGradient id="g"><stop stop-color="#ff0000"/></linearGradient></defs><path style="fill:url(#g);stroke:currentColor" d="M0 0H24V24Z"/></svg>'
        svg=normalize_svg(src,'#123456');r=ET.fromstring(svg)
        self.assertIn('#ff0000',svg);self.assertIn('#123456',svg);self.assertNotIn('style=',svg)
        ids={n.get('id') for n in r.iter() if n.get('id')};p=list(r)[1]
        self.assertIn(p.get('fill')[5:-1],ids)

    def test_bad_viewbox_and_missing_references_fail(self):
        for src in ['<svg viewBox="0 0 nan 24"/>','<svg viewBox="0 0 24 -2"/>',
                    '<svg viewBox="0 0 24 24"><path fill="url(#missing)"/></svg>']:
            with self.assertRaises(ValueError):normalize_svg(src)

if __name__=='__main__':unittest.main()
