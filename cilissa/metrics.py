from abc import ABC, abstractmethod

import numpy as np

from cilissa.images import ImagePair


class Metric(ABC):
    """
    Base class for creating new metrics to use in the program.

    All metrics must implement the `analyze` method.
    """

    NAME: str = ""

    @classmethod
    def get_metric_name(cls) -> str:
        return cls.NAME

    @staticmethod
    @abstractmethod
    def analyze(image_pair: ImagePair) -> np.float64:
        raise NotImplementedError("Metrics must implement the `analyze` method")


class MSE(Metric):
    """
    Mean squared error (MSE)

    Average squared difference between the estimated values and the actual value.

    References:
        - https://en.wikipedia.org/wiki/Mean_squared_error
    """

    NAME = "mse"

    @staticmethod
    def analyze(image_pair: ImagePair) -> np.float64:
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

    @staticmethod
    def analyze(image_pair: ImagePair) -> np.float64:
        if not image_pair.matching_dtype:
            # TODO: Move to real logging
            print("Input images have mismatched data types. Using base image's pixel value.")

        # dmax - maximum possible pixel value of the image
        dmax = image_pair.base.max

        err = MSE.analyze(image_pair)
        return 20 * np.log10(dmax) - 10 * np.log10(err)


class SSIM(Metric):
    """
    Structural similarity index measure (SSIM)

    The SSIM Index quality assessment index is based on the computation of three terms,
    namely the luminance term, the contrast term and the structural term.
    The overall index is a multiplicative combination of the three terms.
    """

    NAME = "ssim"

    @staticmethod
    def analyze(image_pair: ImagePair) -> np.float64:
        pass
