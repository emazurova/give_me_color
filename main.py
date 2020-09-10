from ColorsGetter import ColorsGetter
from ImagePreparation import ImagePreparation
from PIL import Image
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from requests import get
from json import loads


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

    plt.show()

def main():

    API_URL = "https://pixabay.com/api/"
    headers_for_request = {
        "key": "16863975-8967b07d322888d58dc248d44",
        "image_type": "photo",
        "q": ""
    }

    filenames = list()
    print("Enter the word to get its color. Exit like in VIM")
    query = input()
    while query != ":q":
        filenames.clear()
        headers_for_request["q"] = query
        resp = get(API_URL, params=headers_for_request)
        resp_json = loads(resp.text)

        if resp_json["total"] == 0:
            print("Bad request. Couldn't find anything")
        elif resp_json["total"] >= 6:
            for i, item in enumerate(resp_json["hits"]):
                if i < 6:
                    img = get(item["previewURL"])
                    filenames.append(img.content)
        else:
            print("less than 6 images")
            continue
        # filenames = [
        #     "test_images/st_1.jpg",
        #     "test_images/st_2.png",
        #     "test_images/st_3.jpg",
        #     "test_images/st_4.jpg",
        #     "test_images/st_5.jpg",
        #     "test_images/st_7.jpg",
        # ]

        img_prep = ImagePreparation(filenames, (128, 128))
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

        show_image_with_colors(img, most_freq, True, "out_images/{}.png".format(query))

        print("Enter the word to get its color. Exit like in VIM")
        query = input()
    print("Buyyyyy")
    return 0


if __name__ == '__main__':
    main()
