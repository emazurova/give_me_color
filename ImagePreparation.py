from PIL import Image

class ImagePreparation:

    def __init__(self, images_path):
        self.images_path = images_path
        self.images = self.open_images()

    def open_images(self):
        images = list()
        for path in self.images_path:
            images.append(Image.open(path))
        return images

    def make_rotation(self):
        for i, item in enumerate(self.images):
            if item.width < item.height:
                self.images[i] = item.transpose(Image.ROTATE_90)

    def correct_rescale(self):
        pass

