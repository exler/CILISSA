import numpy as np
from matplotlib.pyplot import plt

from cilissa.images import Image


def show_pixel_count_histogram(image: Image) -> None:
    """
    Displays grayscale/RGB pixel count histogram of the given image.

    Requires the `matplotlib` package to be installed.
    """

    plt.figure()
    title = image.name
    xlim = 0

    if image.channels_num == 1:
        title += " - grayscale histogram"
        xlim = 1

        histogram, bin_edges = np.histogram(image.im, bins=256, range=(0, 1))
        plt.plot(bin_edges[0:-1], histogram)
    elif image.channels_num == 3:
        title += " - RGB histogram"
        xlim = 256

        colors = ("red", "green", "blue")
        for channel_id, color in enumerate(colors):
            histogram, bin_edges = np.histogram(image.im[:, :, channel_id], bins=256, range=(0, 256))
            plt.plot(bin_edges[0:-1], histogram, color=color)
    else:
        raise ValueError(f"Cannot display histogram of image with {image.channels_num} channels")

    plt.title(title)
    plt.xlim([0, xlim])
    plt.xlabel("Color value")
    plt.ylabel("Pixel count")
    plt.show()
