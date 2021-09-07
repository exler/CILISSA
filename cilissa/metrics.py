from typing import Optional, Union

import numpy as np
from scipy.ndimage import gaussian_filter

from cilissa.helpers import crop_array, sliding_window
from cilissa.images import ImagePair
from cilissa.operations import Metric
from cilissa.utils import get_operation_subclasses


class MSE(Metric):
    """
    Mean squared error (MSE)

    Average squared difference between the estimated values and the actual value.

    References:
        - https://en.wikipedia.org/wiki/Mean_squared_error
    """

    name = "mse"

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()
        result = np.mean(np.square((im1 - im2)), dtype=np.float64)
        return result


class PSNR(Metric):
    """
    Peak signal-to-noise ratio (PSNR)

    Ratio between the maximum possible power of a signal and
    the power of corrupting noise that affects the fidelity of its representation.

    References:
        - https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    """

    name = "psnr"

    def analyze(self, image_pair: ImagePair) -> float:
        # dmax - maximum possible pixel value of the image
        dmax = image_pair[0].im.max()

        err = MSE().analyze(image_pair)
        if err == 0:
            result = np.inf
        else:
            result = 20 * np.log10(dmax) - 10 * np.log10(err)
        return result


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

    name = "ssim"

    def __init__(
        self,
        channels_num: Optional[int] = None,
        sigma: float = 1.5,
        truncate: float = 3.5,
        K1: float = 0.01,
        K2: float = 0.03,
    ) -> None:
        # Number of channels in image
        self.channels_num = channels_num

        # Small constants 0 <= K1, K2 <= 1
        self.K1 = K1
        self.K2 = K2
        if self.K1 < 0:
            raise ValueError("K1 must be positive!")
        if self.K2 < 0:
            raise ValueError("K2 must be positive!")

        # Standard deviation for weighting function, 0 < sigma
        self.sigma = sigma
        if self.sigma < 0:
            raise ValueError("Sigma must be positive!")

        # Truncate the Gaussian filter at this many standard deviations, 0 < truncate
        self.truncate = truncate
        if self.truncate < 0:
            raise ValueError("Truncate must be positive!")

    def mssim_single_channel(self, im1: np.ndarray, im2: np.ndarray) -> Union[float, np.float64]:
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

        # Avoid edge effects by ignoring filter radius around edges
        # Pad equal to radius as in scipy gaussian_filter
        # https://github.com/scipy/scipy/blob/v1.7.0/scipy/ndimage/filters.py#L258
        pad = int(self.truncate * self.sigma + 0.5)

        return crop_array(S, pad).mean()

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()

        ch_num = self.channels_num or image_pair[0].channels_num

        # Create an empty array to hold results from each channel
        ssim_results = np.empty(ch_num)
        for ch in range(ch_num):
            ch_result = self.mssim_single_channel(im1[:, :, ch], im2[:, :, ch])
            ssim_results[ch] = ch_result

        mssim = ssim_results.mean()
        return mssim


class UIQI(Metric):
    """
    Universal Image Quality Index (UIQI)

    Combines loss of correlation, luminance distortion and contrast distortion.
    Predecessor of SSIM metric.

    References:
        - https://ece.uwaterloo.ca/~z70wang/publications/quality_2c.pdf
    """

    name = "uiqi"

    def __init__(self, block_size: int = 8) -> None:
        self.block_size = block_size

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()

        quality_map = []
        for window_im1, window_im2 in zip(
            sliding_window(im1, window_size=(8, 8)), sliding_window(im2, window_size=(8, 8))
        ):
            if window_im1.shape[0] != self.block_size or window_im1.shape[1] != self.block_size:
                continue

            for i in range(image_pair[0].channels_num):
                im1_band = window_im1[:, :, i]
                im2_band = window_im2[:, :, i]
                im1_band_mean = np.mean(im1_band)
                im2_band_mean = np.mean(im2_band)
                im1_band_variance = np.var(im1_band)
                im2_band_variance = np.var(im2_band)
                im12_band_variance = np.mean((im1_band - im1_band_mean) * (im2_band - im2_band_mean))

                numerator = 4 * im12_band_variance * im1_band_mean * im2_band_mean
                denominator = (im1_band_variance + im2_band_variance) * (im1_band_mean ** 2 + im2_band_mean ** 2)

                if denominator != 0.0:
                    quality = numerator / denominator
                    quality_map.append(quality)

        if not np.any(quality_map):
            raise ValueError(f"Block size {self.block_size} is too big for image with shape {window_im1.shape[0:2]}")

        return np.mean(quality_map)


all_metrics = get_operation_subclasses(Metric)  # type: ignore
