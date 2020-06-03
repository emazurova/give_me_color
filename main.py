from ColorsGetter import ColorsGetter
from ImagePreparation import ImagePreparation
from PIL import Image
import matplotlib.patches as patches
import matplotlib.pyplot as plt


def show_image_with_colors(image, colors, to_save=False, filename=None):

    HEIGHT_OF_COLOR_LINE = 80
    img_to_show = Image.new('RGB', (image.width, image.height + HEIGHT_OF_COLOR_LINE))
    img_to_show.paste(image, (0, 0))

    figure, ax = plt.subplots(1)
    plt.axis('off')
    w = image.width / len(colors)
    ax.imshow(img_to_show)

    for item in range(len(colors)):
        wid = w * item
        ax.add_patch(patches.Rectangle((wid, image.height), w, HEIGHT_OF_COLOR_LINE, edgecolor='none', facecolor=colors[item]))

    if to_save:
        plt.savefig(filename)


def main():
    filenames = [
        "test_images/st_1.jpg",
        "test_images/st_2.png",
        "test_images/st_3.jpg",
        "test_images/st_4.jpg",
        "test_images/st_5.jpg",
        "test_images/st_7.jpg",
    ]

    img_prep = ImagePreparation(filenames, (256, 256))
    try:
        img = img_prep.prepare()
    except ValueError as e:
        print("Error", e)
        return 1
    except FileNotFoundError as e:
        print("Error", e)
        return 2

    colors_getter = ColorsGetter(img)
    # kmeans = colors_getter.get_kmeans_colors(10)
    # average = colors_getter.get_average_color()
    most_freq = colors_getter.get_most_freq_colors(40)

    show_image_with_colors(img, most_freq, True, "out_images/most_freq1.png")
    return 0


if __name__ == '__main__':
    main()
