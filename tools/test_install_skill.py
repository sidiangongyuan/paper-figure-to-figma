from pathlib import Path
import subprocess, sys, tempfile, unittest, zipfile
from install_skill import NAME, build_skill, install, package

class InstallationTests(unittest.TestCase):
    def test_runtime_works_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);dest=root/'installed'/NAME
            install(dest)
            working=root/'unrelated';working.mkdir()
            r=dest/'runtime'
            subprocess.run([sys.executable,str(r/'tools/scene_to_svg.py'),str(r/'examples/minimal.scene.json'),str(working/'preview.svg')],cwd=working,check=True,capture_output=True)
            subprocess.run([sys.executable,str(r/'tools/bundle_figma.py'),str(r/'examples/minimal.scene.json'),str(working/'draw.js')],cwd=working,check=True,capture_output=True)
            self.assertIn('<text', (working/'preview.svg').read_text('utf-8'))
            self.assertIn('importFigureScene', (working/'draw.js').read_text('utf-8'))
            subprocess.run([sys.executable,str(r/'tools/icon_assets.py'),'prepare','--icon','lucide:snowflake','--output',str(working/'frozen.svg')],cwd=working,check=True,capture_output=True)
            self.assertIn('#33464d',(working/'frozen.svg').read_text('utf-8'))
            self.assertTrue((working/'frozen.source.json').is_file())
    def test_update_requires_opt_in_and_preserves_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'skills'/NAME;install(dest)
            (dest/'personal-note.txt').write_text('keep',encoding='utf-8')
            with self.assertRaises(FileExistsError):install(dest)
            _,backup=install(dest,update=True)
            self.assertEqual((backup/'personal-note.txt').read_text('utf-8'),'keep')
            self.assertTrue((dest/'runtime/tools/figma_import.js').exists())
            self.assertTrue((dest/'runtime/tools/ppt_native.py').exists())
            self.assertIn('runtime/prompts/05-powerpoint.md',(dest/'SKILL.md').read_text(encoding='utf-8'))
    def test_portable_zip_is_self_contained(self):
        with tempfile.TemporaryDirectory() as temp:
            path=package(Path(temp)/'skill.zip')
            with zipfile.ZipFile(path) as z:
                self.assertIsNone(z.testzip())
                names=set(z.namelist())
                self.assertIn(NAME+'/SKILL.md',names)
                self.assertIn(NAME+'/runtime/tools/scene_validate.js',names)
                self.assertIn(NAME+'/LICENSE',names)
                self.assertIn(NAME+'/runtime/assets/icons/lucide/LICENSE',names)
                self.assertIn(NAME+'/runtime/prompts/03-vector-assets.md',names)
                self.assertIn(NAME+'/runtime/prompts/04-source-routing.md',names)
                self.assertIn(NAME+'/runtime/tools/extract_pdf_assets.py',names)
                self.assertIn(NAME+'/runtime/tools/ppt_native.py',names)
                self.assertIn(NAME+'/runtime/prompts/05-powerpoint.md',names)
                self.assertFalse(any('figma-plugin/' in n for n in names))

if __name__=='__main__':unittest.main()
