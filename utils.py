import re
from io import  BytesIO

import requests
from PIL import Image
from resizeimage import resizeimage


def resize_image(image_url, size):
    sizes = [int(i) for i in size.lower().split('x')]

    fd = requests.get(image_url)
    image_file = BytesIO(fd.content)
    with Image.open(image_file) as image:
        cover = resizeimage.resize_cover(image, sizes,
                                         validate=False)
        cover.save('output.png', image.format)


def check_width_height_syntax(syntax):
    """
    Helper function to check if it follows width x height syntax or not
    """
    if syntax:
        pattern = re.compile(r'([0-9]+x[0-9]+)')
        if pattern.search(syntax.lower()):
            return True
    return False
