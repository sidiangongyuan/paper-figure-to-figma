import copy
import unittest
import xml.etree.ElementTree as ET

from scene_to_svg import render_scene, validate_scene


class SceneContractTests(unittest.TestCase):
    def setUp(self):
        self.scene={'version':1,'name':'test','width':100,'height':50,'assets':{},'nodes':[
            {'id':'label','type':'text','name':'editable text','x':5,'y':5,'w':90,'h':20,
             'text':'A < B & C','size':16},
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

    def test_gradient_and_translucent_backing_survive_export(self):
        self.scene['nodes'][0].update(type='rect',opacity=.625,fill={
            'type':'linear','direction':'vertical','stops':[
                {'offset':0,'color':'#aa9ed1'},{'offset':1,'color':'#f1f2f9'}]})
        root=ET.fromstring(render_scene(self.scene))
        ns={'s':'http://www.w3.org/2000/svg'}
        grad=root.find('.//s:linearGradient',ns)
        self.assertEqual(grad.get('y2'),'1')
        self.assertEqual([s.get('stop-color') for s in grad],['#aa9ed1','#f1f2f9'])
        rect=root.find('.//s:rect[@id="label"]',ns)
        self.assertEqual(rect.get('opacity'),'0.625')

    def test_svg_curve_and_viewbox_scale_are_preserved(self):
        self.scene['nodes'][0].update(type='svg',w=20,h=20,svg='<svg viewBox="0 0 10 10"><path d="M0 0 C2 8 8 2 10 10"/></svg>')
        root=ET.fromstring(render_scene(self.scene))
        ns={'s':'http://www.w3.org/2000/svg'}
        curve=root.find('.//s:path',ns)
        self.assertIn('C2 8',curve.get('d'))
        group=root.find('.//s:g[@id="label"]',ns)
        self.assertIn('scale(2.0 2.0)',group.get('transform'))

    def test_editor_font_minimum_is_separate_policy(self):
        self.scene['typographyPolicy']={'minEditorFontSize':16}
        self.scene['nodes'][0]['size']=12
        with self.assertRaises(ValueError):
            validate_scene(self.scene)
        self.scene['nodes'][0]['size']=16
        validate_scene(self.scene)

    def test_required_backplate_cannot_be_omitted(self):
        self.scene['visualFeatures']=[{'kind':'translucent_backplate','nodeIds':['backing'],'labelIds':['label']}]
        with self.assertRaises(ValueError):
            validate_scene(self.scene)
        self.scene['nodes'].insert(0,{'id':'backing','type':'rect','name':'label backing','x':5,'y':5,'w':90,'h':20,'fill':'#ffffff','opacity':.625})
        validate_scene(self.scene)
        self.scene['nodes'].reverse()
        with self.assertRaises(ValueError):
            validate_scene(self.scene)

    def test_unresolved_crop_validates_but_cannot_be_exported_as_fake_image(self):
        self.scene['assets']['rgb']={'role':'input_rgb','crop':[1,2,11,12]}
        self.scene['nodes'][0].update(type='image',asset='rgb',role='input_rgb')
        validate_scene(self.scene)
        with self.assertRaisesRegex(ValueError,'prepare_scene'):
            render_scene(self.scene)


if __name__=='__main__':
    unittest.main()
