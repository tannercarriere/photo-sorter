import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import image_loader
from ImageManager.im import setup_directory

PATH_IMAGES        = 'test\\data\\images_found'
PATH_EMPTY         = 'test\\data\\no_images_found'
PATH_MIXED         = 'test\\data\\mixed_files'
PATH_ONE_IMAGE     = 'test\\data\\one_image_folder'
ALLOWED_EXTENSIONS = ['.gif', '.jpeg', '.jpg', '.png', '.webp']

class TestGUIFunctionClass:
    loader = image_loader.ImageLoader(PATH_IMAGES)
    
    def test_init(self):
        assert self.loader._cur_image
        assert self.loader._base_path.endswith(PATH_IMAGES)

    def test_extensions(self):
        self.loader.set_current_directory(*setup_directory(PATH_MIXED))
        status = image_loader.CONTINUE_FOLDER
        while status == image_loader.CONTINUE_FOLDER:
            assert os.path.splitext(self.loader._cur_image)[1] in ALLOWED_EXTENSIONS
            status = self.loader.next_callback()

    def test_change_empty_directory(self):
        self.loader.set_current_directory(*setup_directory(PATH_EMPTY))
        assert self.loader._cur_image is None

    def test_end_of_directory(self):
        self.loader.set_current_directory(*setup_directory(PATH_ONE_IMAGE))
        status = self.loader.next_callback()
        assert self.loader._cur_image is not None
        assert status == image_loader.END_OF_FOLDER
