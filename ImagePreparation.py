from PIL.Image import new, open, ROTATE_90
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class ImagePreparation:
    def __init__(self, images_path, needed_size):
        self.images_path = images_path
        self.images = self.open_images()
        self.needed_size = needed_size

    def __del__(self):
        for item in self.images:
            item.close()

    def open_images(self):
        images = list()
        for path in self.images_path:
            images.append(open(path))
        return images

    def make_rotation(self):
        for i, item in enumerate(self.images):
            if item.width < item.height:
                self.images[i] = item.transpose(ROTATE_90)

    def correct_rescale(self):
        min_width = self.images[0].width
        for item in self.images:
            item.thumbnail((self.needed_size[0], self.needed_size[1]))
            if item.width < min_width:
                min_width = item.width

        print("MIN WIDTH",min_width)
        for index, item in enumerate(self.images):
            self.images[index] = item.crop((0, 0, min_width, self.needed_size[1]))

    @staticmethod
    def concat_horizontally(images_to_concat):
        w = images_to_concat[0].width * len(images_to_concat)
        h = images_to_concat[0].height

        img = new('RGB', (w, h))

        for index, item in enumerate(images_to_concat):
            img.paste(item, (item.width * index, 0))

        filepath = "hor{}.{}".format(images_to_concat[0].width,"png")
        img.save(filepath)
        return img


    @staticmethod
    def concat_vertically(images_to_concat):
        h = images_to_concat[0].height * len(images_to_concat)
        w = images_to_concat[0].width
        img = new('RGB', (w, h))
        for index, item in enumerate(images_to_concat):
            img.paste(item, (0, item.height * index))
        img.save("ver.png")
        return img

    @staticmethod
    def normalize(to_normalize, is_tuple):
        normalized_colors = list()
        if is_tuple:
            for item in to_normalize:
                normalized_colors.append(list([x / 255 for x in item[1]]))
        else:
            for item in to_normalize:
                normalized_colors.append(list([x / 255 for x in item]))
        return normalized_colors

    def prepare(self):
        self.make_rotation()
        self.correct_rescale()
        img_1 = self.concat_horizontally(self.images[:3])
        img_2 = self.concat_horizontally(self.images[3:])
        return self.concat_vertically([img_1, img_2])

    @staticmethod
    def show_image_with_colors(image, colors, to_save=False, filename=None):
        img_to_show = new('RGB', (image.width, image.height + 80))
        img_to_show.paste(image, (0, 0))

        figure, ax = plt.subplots(1)
        plt.axis('off')
        w = image.width / len(colors)
        ax.imshow(img_to_show)

        for item in range(len(colors)):
            wid = w * item
            ax.add_patch(patches.Rectangle((wid, image.height), w, 80, edgecolor='none', facecolor=colors[item]))

        if to_save:
            plt.savefig(filename)