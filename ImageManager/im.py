import os
from glob import iglob
import re

IMAGE_PATTERN = re.compile("(png|jpe?g|webp|gif)$", re.I)

def save_image(name:str, source:str, path:str, *, cur_image:str):
    ''' Saves image with new name of form name-source-original_name
    
    Arguments:
    name (str): base catigory for the image
    source (str): secondary catigory for the image
    path (str): path the image should be saved to
    cur_image (str): path to currently opened image
    '''
    if not cur_image:
        return ''

    if name:
        name = str(name) + '-'
    if source:
        source = str(source) + '-'
    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        path = str(path) + '\\'
    base_file_name = os.path.basename(cur_image)
    destination_file_name = f'{name}{source}{base_file_name}'

    os.rename(cur_image, f'{path}{destination_file_name}') 
    return base_file_name

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