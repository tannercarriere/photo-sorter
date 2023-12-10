import os
from glob import iglob
import re

IMAGE_PATTERN = re.compile("(png|jpe?g|webp|gif)$", re.I)

def save_image(name:str, source:str, path:str, *, cur_image:str):
    if name:
        name = str(name) + '-'
    if source:
        source = str(source) + '-'
    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        path = str(path) + '\\'
    file_name = f'{name}{source}{os.path.basename(cur_image)}'

    os.rename(cur_image, f'{path}{file_name}') 
    return file_name

def setup_directory(path):
    images = iglob(f'{path}\\*')
    chk_image = None
    try:
        chk_image = images.__next__()
        while not IMAGE_PATTERN.findall(chk_image):
            chk_image = images.__next__()
    except StopIteration:
        images, chk_image = None, None
    return images, chk_image