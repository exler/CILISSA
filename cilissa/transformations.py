from typing import Optional, Tuple, Union

import cv2
import numpy as np

from cilissa.images import Image
from cilissa.operations import Transformation


class Blur(Transformation):
    """
    Blurs an image.

    Args:
        gaussian (bool): If True, uses a Gaussian filter to blur the image.
            If False, uses normalized box filter.
        kernel_size (Tuple[int, int]): Gaussian/blurring kernel size.
            Elements in tuple can differ but they both must be positive and odd.
            If using Gaussian filter they can be zero's and then they are computed from sigma.
        sigma (float): Gaussian kernel standard deviation in X direction.
            Used only with Gaussian filter.

    References:
        - https://docs.opencv.org/4.5.2/d4/d86/group__imgproc__filter.html#ga8c45db9afe636703801b0b2e440fce37
        - https://docs.opencv.org/4.5.2/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1

    """

    def __init__(self, gaussian: bool = True, kernel_size: Tuple[int, int] = (0, 0), sigma: float = 1.0) -> None:
        self.gaussian = gaussian

        self.kernel_size = kernel_size
        self.sigma = sigma

    def transform(self, image: Image) -> Image:
        im = image.as_int()

        if self.gaussian:
            new_im = cv2.GaussianBlur(im, self.kernel_size, self.sigma)
        else:
            new_im = cv2.blur(im, self.kernel_size)

        return Image(new_im)


class Sharpen(Transformation):
    """
    Sharpens an image using an unsharp mask.

    Args:
        amount (float): Amount of sharpening applied.
        threshold (int): Threshold for the low-constrast mask.
            Pixels for which the difference between the input and blurred images is less than threshold
            will remain unchanged.
        kwargs (Any): Arguments passed as kwargs will be passed to the blur transformation.

    References:
        - https://en.wikipedia.org/wiki/Unsharp_masking
    """

    def __init__(self, amount: float = 1.5, kernel_size: Tuple[int, int] = (0, 0), sigma: float = 1.0) -> None:
        # Parameters for blur
        self.kernel_size = kernel_size
        self.sigma = sigma

        # Parameters for unsharp mask
        self.amount = amount

    def transform(self, image: Image) -> Image:
        im = image.as_int()

        new_im = cv2.GaussianBlur(im, self.kernel_size, self.sigma)
        new_im = cv2.addWeighted(im, self.amount, new_im, -self.amount + 1, 0)

        return Image(new_im)


class Linear(Transformation):
    """
    Changes brightness of the image with a simple linear transformation.

    g(x) = a * f(x) + b, where `a` controls contrast and `b` controls brightness

    Brightness refers to the overall lightness or darkness of the image.
    Increasing the brightness every pixel in the frame gets lighter.

    Contrast is the difference in brightness between objects in the image.
    Increasing the contrast makes light areas lighter and dark area in the frame becomes much darker.

    Args:
        contrast (int/float/None): Value by which to change the contrast.
            1 and None is the original image.
            A float from interval (0, 1) reduces the contrast. Values above 1 increase the contrast.
        brightness (int/float/None): Value by which to change the brightness.
            0 and None is the original image.
            Negative values reduce the brightness. Positive values increase the brightness.

    References:
        - https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
    """

    def __init__(
        self, contrast: Optional[Union[float, int]] = None, brightness: Optional[Union[float, int]] = None
    ) -> None:
        self.contrast = contrast
        self.brightness = brightness

    def transform(self, image: Image) -> Image:
        im = image.as_int()

        # Apply linear transformation
        new_im = cv2.convertScaleAbs(im, alpha=self.contrast, beta=self.brightness)

        return Image(new_im)


class Translation(Transformation):
    """
    Shifts an image by given amount in pixels along X and/or Y axis.

    Uses an affine transformation to perform image translation.

    Args:
        x (int): Value (in px) to move the image along X-axis.
            Positive - right, negative - left.
        y (int): Value (in px) to move the image along Y-axis.
            Positive - down, negative - up.

    References:
        - https://en.wikipedia.org/wiki/Affine_transformation
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def transform(self, image: Image) -> Image:
        im = image.as_int()

        # Transformation matrix
        M = np.array([[1, 0, self.x], [0, 1, self.y]], dtype=np.float32)
        new_im = cv2.warpAffine(im, M, (im.shape[1], im.shape[0]))

        return Image(new_im)


class Equalization(Transformation):
    """
    Constrast adjustment using histogram equalization.

    CV2 equalization is limited to 8-bit images so we use the NumPy CDF function.

    References:
        - https://en.wikipedia.org/wiki/Histogram_equalization
        - https://web.archive.org/web/20151219221513/http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html # noqa
    """

    def __init__(self, nbins: int = 256) -> None:
        # Number of bins for image histogram
        self.number_of_bins = nbins

    def transform(self, image: Image) -> Image:
        im = image.as_int()

        # Get normalized histogram - probability density function of each gray level
        image_histogram, bins = np.histogram(im.flatten(), self.number_of_bins, density=True)
        cdf = image_histogram.cumsum()
        cdf = 255 * cdf / cdf[-1]

        # Use linear interpolation of cdf to find new pixel values
        image_equalized = np.interp(im.flatten(), bins[:-1], cdf)
        new_im = image_equalized.reshape(im.shape).astype(np.uint8, casting="unsafe")

        return Image(new_im)
