from typing import Optional

import cv2
import numpy as np

from cilissa.helpers import apply_to_channels, crop_array, get_max_pixel_value
from cilissa.images import ImagePair
from cilissa.operations import Metric


class MSE(Metric):
    """
    Mean squared error (MSE)

    Average squared difference between the estimated values and the actual value.

    References:
        - https://en.wikipedia.org/wiki/Mean_squared_error
    """

    def __init__(self, rmse: bool = False) -> None:
        self.root_mean_square_error = rmse

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()
        result = np.mean(np.square((im1 - im2)), dtype=np.float64)
        if self.root_mean_square_error:
            result = np.sqrt(result)
        return result


class PSNR(Metric):
    """
    Peak signal-to-noise ratio (PSNR)

    Ratio between the maximum possible power of a signal and
    the power of corrupting noise that affects the fidelity of its representation.

    References:
        - https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    """

    def __init__(self, max_pixel_value: Optional[int] = None) -> None:
        # Maximum possible pixel value of the image
        self.max_pixel_value = max_pixel_value

    def analyze(self, image_pair: ImagePair) -> float:
        dmax = self.max_pixel_value or get_max_pixel_value(image_pair[0].dtype)

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
        channels_num (int/None): If None, image is assumed to be grayscale (single channel).
            Otherwise the number of channels should be specified here.

    Returns:
        float: Overall quality measure of the entire image (MSSIM)

    References:
        - https://en.wikipedia.org/wiki/Structural_similarity
        - https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf
    """

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

    def mssim_single_channel(self, im1: np.ndarray, im2: np.ndarray) -> float:
        dmax = im1.max()
        dmin = im1.min()
        drange = dmax - dmin

        # Compute weighted means using Gaussian weighting function
        ux = cv2.GaussianBlur(im1, (0, 0), self.sigma)
        uy = cv2.GaussianBlur(im2, (0, 0), self.sigma)

        # Compute weighted variances and covariances
        uxx = cv2.GaussianBlur(im1 ** 2, (0, 0), self.sigma)
        uyy = cv2.GaussianBlur(im2 ** 2, (0, 0), self.sigma)
        uxy = cv2.GaussianBlur(im1 * im2, (0, 0), self.sigma)
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

        result = apply_to_channels(im1, im2, self.mssim_single_channel, ch_num)
        return result


class UIQI(Metric):
    """
    Universal Image Quality Index (UIQI)

    Combines loss of correlation, luminance distortion and contrast distortion.
    Predecessor of SSIM metric.

    References:
        - https://ece.uwaterloo.ca/~z70wang/publications/quality_2c.pdf
    """

    def __init__(self, channels_num: Optional[int] = None, block_size: int = 8) -> None:
        self.channels_num = channels_num

        # Sliding window size
        self.block_size = block_size

    def uiqi_single_channel(self, im1: np.ndarray, im2: np.ndarray) -> float:
        N = self.block_size ** 2

        im1_sq = im1 ** 2
        im2_sq = im2 ** 2
        im12 = im1 * im2

        unif_filter = np.ones(self.block_size, np.float32) / (self.block_size ** 2)

        im1_sum = cv2.filter2D(im1, ddepth=-1, kernel=unif_filter)
        im2_sum = cv2.filter2D(im2, ddepth=-1, kernel=unif_filter)
        im1_sq_sum = cv2.filter2D(im1_sq, ddepth=-1, kernel=unif_filter)
        im2_sq_sum = cv2.filter2D(im2_sq, ddepth=-1, kernel=unif_filter)
        im12_sum = cv2.filter2D(im12, ddepth=-1, kernel=unif_filter)

        im12_sum_mul = im1_sum * im2_sum
        im12_sq_sum_mul = im1_sum ** 2 + im2_sum ** 2
        numerator = 4 * (N * im12_sum - im12_sum_mul) * im12_sum_mul
        denominator1 = N * (im1_sq_sum + im2_sq_sum) - im12_sq_sum_mul
        denominator = denominator1 * im12_sq_sum_mul

        q_map = np.ones(denominator.shape)
        index = np.logical_and((denominator1 == 0), (im12_sq_sum_mul != 0))
        q_map[index] = (2 * im12_sum_mul[index]) / (im12_sq_sum_mul[index])
        index = denominator != 0
        q_map[index] = numerator[index] / denominator[index]

        s = int(self.block_size / 2)
        return np.mean(q_map[s:-s, s:-s])

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()

        ch_num = self.channels_num or image_pair[0].channels_num

        result = apply_to_channels(im1, im2, self.uiqi_single_channel, ch_num)
        return result


class VIFP(Metric):
    """
    Pixel Based Visual Information Fidelity (VIF-P)

    Employs natural scene statistical (NSS) models in conjunction with a distortion (channel) model to quantify
    the information shared between the test and the reference images.

    The pixel domain algorithm is not described in the paper below. This is a computationally simpler
    derivative of the algorithm presented in the paper, based on the original Matlab implementation.

    References:
        - http://live.ece.utexas.edu/publications/2004/hrs_ieeetip_2004_imginfo.pdf
        - https://github.com/utlive/vif_pixel
    """

    def __init__(self, channels_num: Optional[int] = None, sigma: float = 2.0) -> None:
        self.channels_num = channels_num

        # Variance of the visual noise
        self.sigma = sigma

    def vifp_single_channel(self, im1: np.ndarray, im2: np.ndarray) -> float:
        eps = 1e-10
        numerator = 0
        denominator = 0

        for scale in range(1, 5):
            N = 2 ** (4 - scale + 1) + 1
            sd = N / 5.0

            if scale > 1:
                im1 = cv2.GaussianBlur(im1, (0, 0), sd)
                im2 = cv2.GaussianBlur(im2, (0, 0), sd)

            mu1 = cv2.GaussianBlur(im1, (0, 0), sd)
            mu2 = cv2.GaussianBlur(im2, (0, 0), sd)
            mu1_sq = mu1 ** 2
            mu2_sq = mu2 ** 2
            mu12 = mu1 * mu2

            sigma1_sq = cv2.GaussianBlur(im1 ** 2, (0, 0), sd) - mu1_sq
            sigma2_sq = cv2.GaussianBlur(im2 ** 2, (0, 0), sd) - mu2_sq
            sigma12 = cv2.GaussianBlur(im1 * im2, (0, 0), sd) - mu12

            sigma1_sq[sigma1_sq < 0] = 0
            sigma2_sq[sigma2_sq < 0] = 0

            g = sigma12 / (sigma1_sq + eps)
            sv_sq = sigma2_sq - (g * sigma12)

            g[sigma1_sq < eps] = 0
            sv_sq[sigma1_sq < eps] = sigma2_sq[sigma1_sq < eps]
            sigma1_sq[sigma1_sq < eps] = 0

            g[sigma2_sq < eps] = 0
            sv_sq[sigma2_sq < eps] = 0

            sv_sq[g < 0] = sigma2_sq[g < 0]
            g[g < 0] = 0
            sv_sq[sv_sq <= eps] = eps

            numerator += np.sum(np.log10(1 + g ** 2 * (sigma1_sq / (sv_sq + self.sigma))))
            denominator += np.sum(np.log10(1 + (sigma1_sq / self.sigma)))

        return numerator / denominator

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()

        ch_num = self.channels_num or image_pair[0].channels_num

        result = apply_to_channels(im1, im2, self.vifp_single_channel, ch_num)
        return result


class SAM(Metric):
    """
    Spectral Angle Mapper (SAM)

    Physically-based spectral classification that uses an n-D angle to match pixels to reference spectra.

    This technique is relatively insensitive to illumination and albedo effects.

    References:
        - https://ntrs.nasa.gov/citations/19940012238
    """

    def __init__(self, to_degrees: bool = True) -> None:
        self.convert_to_degrees = to_degrees

    def analyze(self, image_pair: ImagePair) -> float:
        im1, im2 = image_pair.as_floats()

        # Spectral angles are first computed for each pair of pixels
        numerator = np.sum(im1 * im2, axis=2)
        denominator = np.linalg.norm(im1, axis=2) * np.linalg.norm(im2, axis=2)
        val = np.clip(numerator / denominator, -1, 1)
        sam_angles = np.arccos(val)

        if self.convert_to_degrees:
            sam_angles *= 180 / np.pi

        return np.mean(np.nan_to_num(sam_angles))
