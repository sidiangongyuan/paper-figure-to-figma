import copy
import unittest
import xml.etree.ElementTree as ET

from scene_to_svg import render_scene, validate_scene


class SceneContractTests(unittest.TestCase):
    def setUp(self):
        self.scene={'version':1,'name':'test','width':100,'height':50,'assets':{},'nodes':[
            {'id':'label','type':'text','name':'editable text','x':5,'y':5,'w':90,'h':20,
             'text':'A < B & C','size':12},
        ]}

    def test_text_stays_editable_and_xml_escaped(self):
        root=ET.fromstring(render_scene(self.scene))
        text=root.find('.//{http://www.w3.org/2000/svg}text')
        self.assertEqual(''.join(text.itertext()),'A < B & C')

    def test_icon_cannot_hide_bitmap(self):
        for tag in ('image','feImage','foreignObject','script'):
            with self.subTest(tag=tag):
                scene=copy.deepcopy(self.scene)
                scene['nodes'][0].update(type='svg',svg=f'<svg><{tag}/></svg>')
                with self.assertRaises(ValueError):
                    validate_scene(scene)

    def test_raster_roles_are_enforced(self):
        self.scene['assets']['photo']={'mime':'image/png','data':'','role':'input_rgb'}
        self.scene['nodes'][0].update(type='image',asset='photo',role='icon')
        with self.assertRaises(ValueError):
            validate_scene(self.scene)
        self.scene['nodes'][0]['role']='input_rgb'
        self.assertEqual(validate_scene(self.scene)['rasterRoles'],{'input_rgb':1})

    def test_duplicate_ids_are_rejected(self):
        self.scene['nodes'].append(copy.deepcopy(self.scene['nodes'][0]))
        with self.assertRaises(ValueError):
            validate_scene(self.scene)


if __name__=='__main__':
    unittest.main()
