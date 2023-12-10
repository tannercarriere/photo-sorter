import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ImageManager.im import save_image, IMAGE_PATTERN

PATH_RENAME = 'test\\data\\rename_folder'
PATH_IMAGES = 'test\\data\\images_found'
PATH_MIXED = 'test\\data\\mixed_files'

class TestHelperFunctionClass:
    orig_name: str = 'rename_img.jpg'
    rename:    str = 'name'
    source:    str = 'source'
    def test_save_file(self):
        path: str = PATH_RENAME
        save_image(self.rename, self.source, path, cur_image=f'{path}\\{self.orig_name}')

        assert os.path.exists(f'{path}\\{self.rename}-{self.source}-{self.orig_name}')
        # Undo rename to allow for back to back tests
        os.rename(f'{path}\\{self.rename}-{self.source}-{self.orig_name}', f'{path}\\{self.orig_name}')

    def test_save_file_new_dir(self):
        orig_path: str = PATH_RENAME
        new_path:  str = 'test\\data\\new_path\\'

        save_image(self.rename, self.source, new_path, cur_image=f'{orig_path}\\{self.orig_name}')

        assert os.path.exists(f'{new_path}\\{self.rename}-{self.source}-{self.orig_name}')
        # Undo rename to allow for back to back tests
        os.rename(f'{new_path}\\{self.rename}-{self.source}-{self.orig_name}', f'{orig_path}\\{self.orig_name}')
        os.rmdir(f'{new_path}\\')

    def regex_helper(self, test_dict: dict[str, bool]) -> bool:
        for f_name in test_dict:
            if IMAGE_PATTERN.findall(f_name) and not test_dict[f_name]:
                return False
            if not IMAGE_PATTERN.findall(f_name) and test_dict[f_name]:
                return False
        return True
    
    def test_image_regex_lower_good(self):
        test_strings = {
            'test.png':True,
            'test.jpg':True,
            'test.jpeg':True,
            'test.gif':True,
            'test.webp':True
        }
        assert self.regex_helper(test_strings)

    def test_image_regex_caps_good(self):
        test_strings = {
            'test.PNG':True,
            'test.JPG':True,
            'test.JPEG':True,
            'test.GIF':True,
            'test.WEBP':True
        }
        assert self.regex_helper(test_strings)

    def test_image_regex_lower(self):
        test_strings = {
            'test.png':True,
            'test.jpg':True,
            'test.txt':False,
            'jpeg.txt':False,
            'png.txt':False,
            'jpg.txt':False,
            'gif.txt':False,
            'webp.txt':False,
            'text_description_of_png_files.txt':False,
            'list_of_png_files_found.csv':False,
            'compressed image.jpeg.zip':False,
            'misspelled_extension.jepg':False,
            'test.jpeg':True,
            'test.gif':True,
            'test.webp':True
        }
        assert self.regex_helper(test_strings)

    def test_image_regex_caps(self):
        test_strings = {
            'test.PNG':True,
            'test.JPG':True,
            'test.TXT':False,
            'jpeg.TXT':False,
            'png.TXT':False,
            'jpg.TXT':False,
            'gif.TXT':False,
            'webp.TXT':False,
            'text_description_of_PNG_files.TXT':False,
            'list_of_PNG_files_found.CSV':False,
            'compressed image.JPEG.ZIP':False,
            'misspelled_extension.JEPG':False,
            'test.JPEG':True,
            'test.GIF':True,
            'test.WEBP':True
        }
        assert self.regex_helper(test_strings)

    def test_image_regex_mixed_case(self):
        test_strings = {
            'teSt.PNG':True,
            'tEst.jPG':True,
            'tesT.tXT':False,
            'jPeg.TXT':False,
            'Png.TXT':False,
            'jpG.TXT':False,
            'gif.TXT':False,
            'webp.tXT':False,
            'TextDescriptionOfPngFiles.tXT':False,
            'list_of_pNg_files_found.cSV':False,
            'compressed image.jpeG.zIP':False,
            'misspelled_extension.jEPG':False,
            'misspelled_extension.jePg':False,
            'test.jPEG':True,
            'test.gIF':True,
            'test.wEBP':True
        }
        assert self.regex_helper(test_strings)

    def test_image_regex_paths(self):
        test_strings = {
            'some/relative/path/test.png':True,
            '/absolute/unix/path/test.jpg':True,
            'A:\\bsolute\\win\\path\\test.jpeg':True,
            'rel\\ative\\path\\test.gif':True,
            './with/dot/test.webp':True,
            '.\\with\\dot\\more\\slashes\\jpeg.txt':False,
            'png/jpg/gif/webp/png.txt':False,
            '//////////jpg.txt':False,
            '\\\\\\\\\\gif.txt':False,
            '/w/e/b/p.txt':False,
        }
        assert self.regex_helper(test_strings)