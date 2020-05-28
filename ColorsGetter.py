from sklearn.cluster import KMeans
from ImagePreparation import ImagePreparation


class ColorsGetter:
    def __init__(self, image):
        self.image = image
        self.height, self.width = self.image.size
        self.data = image.getdata()
        self.colors = ImagePreparation.normalize(image.getcolors(self.height * self.width), True)

    def get_kmeans_colors(self, clusters_count):
        return ImagePreparation.normalize(KMeans(n_clusters=clusters_count).fit(self.data).cluster_centers_, False)

    def get_average_color(self):
        length = len(self.colors)

        r_total = 1./length
        g_total = 1./length
        b_total = 1./length

        for item in self.colors:
            r_total += item[0]
            g_total += item[1]
            b_total += item[2]

        return [(r_total, g_total, b_total)]

    def get_most_freq_colors(self, colors_count = 256):
        if colors_count > 256:
            yield ValueError("Colors must be in range [1;256]")
        quantized = self.image.quantize(colors=colors_count)
        convert_rgb = quantized.convert('RGB')
        colors = convert_rgb.getcolors()
        color_str = sorted(colors, reverse=True)

        final_list = []
        for i in color_str:
            final_list.append(i[1]/255)
        return final_list
