from ColorsGetter import ColorsGetter
from ImagePreparation import ImagePreparation
if __name__ == '__main__':
    filenames = [
        "/home/liza/Downloads/st_1.jpg",
        "/home/liza/Downloads/st_2.png",
        "/home/liza/Downloads/st_3.jpg",
        "/home/liza/Downloads/st_4.jpg",
        "/home/liza/Downloads/st_5.jpg",
        "/home/liza/Downloads/st_6.jpeg",
    ]

    img_prep = ImagePreparation(filenames, (256,256))
    img = img_prep.prepare()

    colors_getter = ColorsGetter(img)

    kmeans = colors_getter.get_kmeans_colors(10)
    # average = colors_getter.get_average_color()
    # most_freq = colors_getter.get_most_freq_colors(40)

    img_prep.show_image_with_colors(img, kmeans, True, "st_kmeans.png")

