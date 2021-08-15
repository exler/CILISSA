import os
import unittest
from pathlib import Path

from numpy import isinf

from cilissa.core import OperationsList
from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.metrics import MSE, PSNR
from cilissa.transformations import Blur, Equalization


class TestOperationsList(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_path = Path(os.path.dirname(__file__), "data")

    def setUp(self) -> None:
        self.ref_image = Image(Path(self.data_path, "ref_images", "monarch.bmp"))
        self.A_image = self.ref_image.copy()

    def test_operations_list_pair(self) -> None:
        mse, psnr = MSE(), PSNR()
        blur, eq = Blur(), Equalization()
        operations = OperationsList([mse, blur, eq, psnr])

        image_pair = ImagePair(self.ref_image, self.A_image)
        result = operations.run(image_pair)

        self.assertEqual(result[0].value, 0.0)
        self.assertFalse(isinf(result[1].value))

    def test_operations_list_collection(self) -> None:
        mse, psnr = MSE(), PSNR()
        blur, eq = Blur(), Equalization()
        operations = OperationsList([mse, blur, eq, psnr])

        image_pair1 = ImagePair(self.ref_image, self.A_image)
        image_pair2 = ImagePair(self.ref_image.copy(), self.A_image.copy())
        image_collection = ImageCollection([image_pair1, image_pair2])

        result = operations.run(image_collection)

        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0][0], result[1][0])
        self.assertAlmostEqual(result[0][1], result[1][1])
