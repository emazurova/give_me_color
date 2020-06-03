from PIL.Image import new, open, ROTATE_90


class ImagePreparation:
    def __init__(self, images_path, needed_size):
        self.images_path = images_path
        self.images = list()
        self.needed_size = needed_size

    def __del__(self):
        for item in self.images:
            item.close()

    def open_images(self):
        if len(self.images_path) == 0:
            raise ValueError("There are no images to open")

        for path in self.images_path:
            self.images.append(open(path))

    def make_rotation(self):
        for i, item in enumerate(self.images):
            if item.width < item.height:
                self.images[i] = item.transpose(ROTATE_90)

    def correct_rescale(self):
        min_height = self.images[0].height
        for item in self.images:
            item.thumbnail((self.needed_size[0], self.needed_size[1]))
            if item.height < min_height:
                min_height = item.height

        for index, item in enumerate(self.images):
            self.images[index] = item.crop((0, 0, self.needed_size[1], min_height))

    @staticmethod
    def concat_horizontally(images_to_concat):
        w = images_to_concat[0].width * len(images_to_concat)
        h = images_to_concat[0].height
        img = new('RGB', (w, h))

        for index, item in enumerate(images_to_concat):
            img.paste(item, (item.width * index, 0))

        return img

    @staticmethod
    def concat_vertically(images_to_concat):
        h = images_to_concat[0].height * len(images_to_concat)
        w = images_to_concat[0].width
        img = new('RGB', (w, h))

        for index, item in enumerate(images_to_concat):
            img.paste(item, (0, item.height * index))

        return img

    def prepare(self):
        self.open_images()
        self.make_rotation()
        self.correct_rescale()
        img_1 = self.concat_horizontally(self.images[:3])
        img_2 = self.concat_horizontally(self.images[3:])
        return self.concat_vertically([img_1, img_2])
