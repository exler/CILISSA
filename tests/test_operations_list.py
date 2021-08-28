import os
import unittest
from pathlib import Path

from numpy import isinf

from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.metrics import MSE, PSNR
from cilissa.operations import OperationsList
from cilissa.transformations import Blur, Equalization


class TestOperationsList(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_path = Path(os.path.dirname(__file__), "data")

    def setUp(self) -> None:
        self.im1 = Image(Path(self.data_path, "ref_images", "monarch.bmp"))
        self.im2 = self.im1.copy()

    def test_operations_list_pair(self) -> None:
        mse, psnr = MSE(), PSNR()
        blur, eq = Blur(), Equalization()
        operations = OperationsList([mse, blur, eq, psnr])

        image_pair = ImagePair(self.im1, self.im2)
        result = operations.run_all(image_pair)

        self.assertEqual(result[0].value, 0.0)
        self.assertFalse(isinf(result[3].value))

    def test_operations_list_collection(self) -> None:
        mse, psnr = MSE(), PSNR()
        blur, eq = Blur(), Equalization()
        operations = OperationsList([mse, blur, eq, psnr])

        image_pair1 = ImagePair(self.im1, self.im2)
        image_pair2 = ImagePair(self.im1.copy(), self.im2.copy())
        image_collection = ImageCollection([image_pair1, image_pair2])

        result = operations.run_all(image_collection)

        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0][0].value, result[1][0].value)
        self.assertAlmostEqual(result[0][3].value, result[1][3].value)
