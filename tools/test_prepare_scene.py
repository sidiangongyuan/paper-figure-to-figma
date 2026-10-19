import base64
import copy
import io
from pathlib import Path
import tempfile
import unittest

from prepare_scene import prepare

try:
    from PIL import Image
except ImportError:
    Image = None


@unittest.skipIf(Image is None,'Pillow is optional; required only for crop resolution tests')
class CropPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.reference=self.root/'reference.png'
        Image.new('RGB',(30,20),'red').save(self.reference)
        self.scene={'version':1,'name':'crop','width':300,'height':200,
                    'referenceSize':{'width':30,'height':20},
                    'assets':{'../unsafe-id':{'role':'input_rgb','crop':[2,3,12,11]}},
                    'nodes':[{'id':'rgb','name':'RGB','type':'image','role':'input_rgb','asset':'../unsafe-id','x':0,'y':0,'w':100,'h':80}]}

    def tearDown(self):
        self.temp.cleanup()

    def test_original_pixel_crop_is_not_scaled_by_editor_canvas(self):
        manifest=prepare(self.scene,self.root/'out',self.reference)
        image=Image.open(io.BytesIO(base64.b64decode(self.scene['assets']['../unsafe-id']['data'])))
        self.assertEqual(image.size,(10,8))
        self.assertEqual(Path(manifest['../unsafe-id']).name,'asset-000.png')
        self.assertTrue((self.root/'out/scene.resolved.json').exists())

    def test_wrong_reference_dimensions_and_out_of_bounds_crop_fail(self):
        scene=copy.deepcopy(self.scene)
        scene['referenceSize']['width']=300
        with self.assertRaisesRegex(ValueError,'referenceSize'):
            prepare(scene,self.root/'wrong-size',self.reference)
        self.scene['assets']['../unsafe-id']['crop']=[2,3,31,11]
        with self.assertRaisesRegex(ValueError,'bounds'):
            prepare(self.scene,self.root/'wrong-crop',self.reference)

    def test_resolved_project_can_be_reused_without_reference(self):
        prepare(self.scene,self.root/'first',self.reference)
        manifest=prepare(self.scene,self.root/'second')
        with Image.open(manifest['../unsafe-id']) as image:
            self.assertEqual(image.size,(10,8))


if __name__=='__main__':
    unittest.main()
