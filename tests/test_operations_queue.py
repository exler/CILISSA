import os
import unittest
from pathlib import Path

from numpy import isinf

from cilissa.core import OperationsQueue
from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE, PSNR
from cilissa.transformations import Blur, Equalization


class TestOperationsQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_path = Path(os.path.dirname(__file__), "data")

        cls.ref_image = Image(Path(cls.data_path, "ref_images", "monarch.bmp"))
        cls.A_image = cls.ref_image.copy()

    def test_operations_queue_pair(self) -> None:
        mse, psnr = MSE(), PSNR()
        blur, eq = Blur(), Equalization()
        queue = OperationsQueue([mse, blur, eq, psnr])

        image_pair = ImagePair(self.ref_image, self.A_image)
        result = queue.run(image_pair)

        self.assertEqual(result[0], 0.0)
        self.assertFalse(isinf(result[1]))

    def test_operations_queue_collection(self) -> None:
        pass
