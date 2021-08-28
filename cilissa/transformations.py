from typing import Any, Optional, Tuple, Union

import cv2
import numpy as np

from cilissa.images import Image
from cilissa.operations import Transformation
from cilissa.utils import get_operation_subclasses


class Blur(Transformation):
    """
    Blurs an image.

    Args:
        - gaussian (bool):
        If True, uses a Gaussian filter to blur the image.
        If False, uses normalized box filter.
        - kernel_size (Tuple[int, int]):
        Gaussian/blurring kernel size. Elements in tuple can differ but they both must be positive and odd.
        If using Gaussian filter they can be zero's and then they are computed from sigma.
        - sigma (float):
        Gaussian kernel standard deviation in X direction. Used only with Gaussian filter.

    References:
        - https://docs.opencv.org/4.5.2/d4/d86/group__imgproc__filter.html#ga8c45db9afe636703801b0b2e440fce37
        - https://docs.opencv.org/4.5.2/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1

    """

    name = "blur"

    def __init__(
        self,
        gaussian: bool = True,
        kernel_size: Tuple[int, int] = (5, 5),
        sigma: float = 1.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

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
        - amount (float):
        Amount of sharpening applied.
        - threshold (int):
        Threshold for the low-constrast mask.
        Pixels for which the difference between the input and blurred images is less than threshold
        will remain unchanged.
        - kwargs (Any):
        Arguments passed as kwargs will be passed to the blur transformation.

    References:
        - https://en.wikipedia.org/wiki/Unsharp_masking
    """

    name = "sharpen"

    def __init__(
        self,
        amount: float = 1.5,
        threshold: int = 10,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        # Parameters for blur
        self.blur_params = {}

        kernel_size = kwargs.pop("kernel_size", None)
        if kernel_size:
            self.blur_params["kernel_size"] = kernel_size

        sigma = kwargs.pop("sigma", None)
        if sigma:
            self.blur_params["sigma"] = sigma

        # Parameters for unsharp mask
        self.amount = amount
        self.threshold = threshold

    def transform(self, image: Image) -> Image:
        im = image.as_int()
        im_copy = image.copy()

        blurred = Blur(gaussian=True, **self.blur_params).transform(im_copy).as_int()

        new_im = im * (1 + self.amount) + blurred * (-self.amount)
        new_im = np.maximum(new_im, np.zeros(new_im.shape))
        new_im = np.minimum(new_im, 255 * np.ones(new_im.shape))
        new_im = new_im.round().astype(np.uint8)
        if self.threshold > 0:
            low_contrast_mask = np.absolute(im - blurred) < self.threshold
            np.copyto(new_im, im, where=low_contrast_mask)

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
        - contrast (int/float/None):
        Value by which to change the contrast. 1 and None is the original image.
        A float from interval (0, 1) reduces the contrast. Values above 1 increase the contrast.
        - brightness (int/float/None):
        Value by which to change the brightness. 0 and None is the original image.
        Negative values reduce the brightness. Positive values increase the brightness.

    References:
        - https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
    """

    name = "linear"

    def __init__(
        self,
        contrast: Optional[Union[int, float]] = None,
        brightness: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

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
        - x (int): Value (in px) to move the image along X-axis.
        Positive - right, negative - left.
        - y (int): Value (in px) to move the image along Y-axis.
        Positive - down, negative - up.

    References:
        - https://en.wikipedia.org/wiki/Affine_transformation
    """

    name = "translation"

    def __init__(self, x: int = 0, y: int = 0, **kwargs: Any) -> None:
        super().__init__(**kwargs)

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

    Transforms the image into YCbCr color space and then performs equalization.

    References:
        - https://en.wikipedia.org/wiki/Histogram_equalization
        - https://en.wikipedia.org/wiki/YCbCr
        - https://www.programmersought.com/article/55274250088/
    """

    name = "equalization"

    def transform(self, image: Image) -> Image:
        im = image.as_int()

        # Transform to YCbCr color space
        new_im = cv2.cvtColor(im, cv2.COLOR_RGB2YCrCb)

        # Equalize histogram
        new_im[:, :, 0] = cv2.equalizeHist(new_im[:, :, 0])

        # Transform back to RGB color space
        new_im = cv2.cvtColor(new_im, cv2.COLOR_YCrCb2RGB)

        return Image(new_im)


all_transformations = get_operation_subclasses(Transformation)  # type: ignore
