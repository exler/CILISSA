from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from scipy.ndimage import gaussian_filter

from cilissa.helpers import crop_array
from cilissa.images import Image, ImagePair


class Metric(ABC):
    """
    Base class for creating new metrics to use in the program.

    All metrics must implement the `analyze` method.
    """

    NAME: str = ""

    @classmethod
    def get_metric_name(cls) -> str:
        return cls.NAME

    @abstractmethod
    def analyze(self, image_pair: ImagePair) -> np.float64:
        raise NotImplementedError("Metrics must implement the `analyze` method")


class MSE(Metric):
    """
    Mean squared error (MSE)

    Average squared difference between the estimated values and the actual value.

    References:
        - https://en.wikipedia.org/wiki/Mean_squared_error
    """

    NAME = "mse"

    def analyze(self, image_pair: ImagePair) -> np.float64:
        base_image, test_image = image_pair.as_floats()
        return np.mean(np.square((base_image - test_image)), dtype=np.float64)


class PSNR(Metric):
    """
    Peak signal-to-noise ratio (PSNR)

    Ratio between the maximum possible power of a signal and
    the power of corrupting noise that affects the fidelity of its representation.

    References:
        - https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    """

    NAME = "psnr"

    def analyze(self, image_pair: ImagePair) -> np.float64:
        if not image_pair.matching_dtype:
            # TODO: Move to real logging
            print("Input images have mismatched data types. Using base image's pixel value.")

        # dmax - maximum possible pixel value of the image
        dmax = image_pair.base.max

        err = MSE().analyze(image_pair)
        return 20 * np.log10(dmax) - 10 * np.log10(err)


class SSIM(Metric):
    """
    Structural similarity index measure (SSIM)

    The SSIM Index quality assessment index is based on the computation of three terms,
    namely the luminance term, the contrast term and the structural term.
    The overall index is a multiplicative combination of the three terms.

    Args:
        - channels_num (int/None):
        If None, image is assumed to be grayscale (single channel).
        Otherwise the number of channels should be specified here.

    Returns:
        mssim (float) - Overall quality measure of the entire image (MSSIM)

    References:
        - https://en.wikipedia.org/wiki/Structural_similarity
        - https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf
    """

    NAME = "ssim"

    def __init__(self, channels_num: int = 1, **kwargs: Any) -> None:
        self.channels_num = channels_num

        # Small constants 0 <= K1, K2 <= 1
        self.K1 = kwargs.pop("K1", 0.01)
        self.K2 = kwargs.pop("K2", 0.03)
        if self.K1 < 0:
            raise ValueError("K1 must be positive!")
        if self.K2 < 0:
            raise ValueError("K2 must be positive!")

        # Standard deviation for weighting function, 0 < sigma
        self.sigma = kwargs.pop("sigma", 1.5)
        if self.sigma < 0:
            raise ValueError("Sigma must be positive!")

        # Truncate the Gaussian filter at this many standard deviations, 0 < truncate
        self.truncate = kwargs.pop("truncate", 3.5)
        if self.truncate < 0:
            raise ValueError("Truncate must be positive!")

    def mssim_single_channel(self, im1: np.ndarray, im2: np.ndarray) -> np.ndarray:
        dmax = im1.max()
        dmin = im1.min()
        drange = dmax - dmin

        filter_args = {"truncate": self.truncate, "sigma": self.sigma}

        # Compute weighted means using Gaussian weighting function
        ux = gaussian_filter(im1, **filter_args)
        uy = gaussian_filter(im2, **filter_args)

        # Compute weighted variances and covariances
        uxx = gaussian_filter(im1 ** 2, **filter_args)
        uyy = gaussian_filter(im2 ** 2, **filter_args)
        uxy = gaussian_filter(im1 * im2, **filter_args)
        vx = uxx - ux * ux
        vy = uyy - uy * uy
        vxy = uxy - ux * uy

        # Constants to avoid instability when ux**2 + uy**2 are close to zero (formula 7)
        L = drange
        C1 = (self.K1 * L) ** 2
        C2 = (self.K2 * L) ** 2

        # Final form of the SSIM index (formula 13, page 605)
        A1, A2, B1, B2 = (2 * ux * uy + C1, 2 * vxy + C2, ux ** 2 + uy ** 2 + C1, vx + vy + C2)
        D = B1 * B2
        S = (A1 * A2) / D

        return S.mean()

    def analyze(self, image_pair: ImagePair) -> np.float64:
        if not image_pair.matching_dtype:
            # TODO: Move to real logging
            print("Input images have mismatched data types. Using base image's pixel value.")

        base_image, test_image = image_pair.as_floats()

        # Create an empty array to hold results from each channel
        ssim_results = np.empty(self.channels_num)
        for ch in range(self.channels_num):
            ch_result = self.mssim_single_channel(base_image[:, :, ch], test_image[:, :, ch])
            ssim_results[ch] = ch_result

        mssim = ssim_results.mean()
        return mssim
