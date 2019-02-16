from PIL import Image
import os

class Thumbs():
    def __init__(self, size=[120, 120]):
        self.size = size

    def run(self, input_img):
        name, type = os.path.splitext(input_img)
        output_img = name + '_thumb' + type
        im = Image.open(input_img)
        im.thumbnail(self.size)
        im.save(output_img)