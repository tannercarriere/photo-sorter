import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import image_loader

# Seperate file as instantiating the image_loader class multiple times in the
# same file causes weird issues I can't find a fix for

def test_init_no_directory():
    item = image_loader.ImageLoader('')
    assert not item._cur_image
    assert not item._base_path
    assert not item._save_path
    del item