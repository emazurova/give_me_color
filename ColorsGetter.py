from sklearn.cluster import KMeans


class ColorsGetter:
    def __init__(self, image):
        self.image = image
        self.width, self.height = self.image.size
        self.data = self.normalize_colors(image.getdata())

    @staticmethod
    def normalize_colors(init_colors):
        normalized_colors = list()
        for item in init_colors:
            normalized_colors.append(list([x / 255 for x in item]))
        return normalized_colors

    def get_kmeans_colors(self, clusters_count):
        return KMeans(n_clusters=clusters_count).fit(self.data).cluster_centers_

    def get_average_color(self):
        length = len(self.data)

        r_total = 0
        g_total = 0
        b_total = 0

        for item in self.data:
            r_total += item[0]
            g_total += item[1]
            b_total += item[2]

        return [(r_total/length, g_total/length, b_total/length)]

    def get_most_freq_colors(self, colors_count=256):
        if colors_count > 256:
            raise ValueError("Colors must be in range [1;256]")
        quantized = self.image.quantize(colors=colors_count)
        convert_rgb = quantized.convert('RGB')
        colors = convert_rgb.getcolors()
        color_str = sorted(colors, reverse=True)

        final_colors_list = []
        for i in color_str:
            final_colors_list.append(i[1])
        return self.normalize_colors(final_colors_list)
