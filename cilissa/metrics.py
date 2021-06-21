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
    """

    NAME = "mse"

    @staticmethod
    def analyze(image_pair: ImagePair) -> np.float64:
        base_image, test_image = image_pair.as_floats()
        return np.mean((base_image - test_image) ** 2, dtype=np.float64)


class PSNR(Metric):
    """
    Peak signal-to-noise ratio (PSNR)

    Ratio between the maximum possible power of a signal and
    the power of corrupting noise that affects the fidelity of its representation.

    PSNR is most easily defined via the mean squared error (MSE).
    """

    NAME = "psnr"

    @staticmethod
    def analyze(image_pair: ImagePair) -> np.float64:
        pass


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
