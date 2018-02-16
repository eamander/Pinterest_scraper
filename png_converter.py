from PIL import Image
import matplotlib.pyplot as plt
import os


def png_convert(src):
    images = [image for image in os.listdir(src) if image[-4:] == '.png']
    for image in images:
        im = Image.open(os.path.join(src, image))
        im = im.convert("RGB")
        new_path = os.path.join(src, image[:-4]+'.jpg')
        if not os.path.exists(new_path):
            im.save(new_path)


def bad_jpg_remover(src):
    images = [image for image in os.listdir(src) if image[-4:] == '.jpg']
    for image in images:
        im = plt.imread(os.path.join(src, image), format='jpeg')
        if im.shape[-1] == 4:
            os.unlink(os.path.join(src, image))
