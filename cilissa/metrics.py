from abc import ABC, abstractmethod

import numpy as np

from cilissa.images import ImagePair


class Metric(ABC):
    """
    Base class for creating new metrics to use in the program.

    All metrics must implement the `analyze` method.
    """

    name: str = ""

    def __init__(self, image_pair: ImagePair) -> None:
        self._image_pair = image_pair

    def get_metric_name(self) -> str:
        return self.name

    @abstractmethod
    def analyze(self) -> np.float64:
        raise NotImplementedError("Metrics must implement the `analyze` method")


class MSE(Metric):
    """
    Mean squared error (MSE)

    Average squared difference between the estimated values and the actual value.
    """

    name = "mse"

    def analyze(self) -> np.float64:
        base_image, test_image = self._image_pair.as_floats()
        return np.mean((base_image - test_image) ** 2, dtype=np.float64)


class PSNR(Metric):
    """
    Peak signal-to-noise ratio (PSNR)

    Ratio between the maximum possible power of a signal and
    the power of corrupting noise that affects the fidelity of its representation.

    PSNR is most easily defined via the mean squared error (MSE).
    """

    name = "psnr"


class SSIM(Metric):
    """
    Structural similarity index measure (SSIM)

    The SSIM Index quality assessment index is based on the computation of three terms,
    namely the luminance term, the contrast term and the structural term.
    The overall index is a multiplicative combination of the three terms.
    """

    name = "ssim"
