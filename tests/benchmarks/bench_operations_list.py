import os
from pathlib import Path

from verdandi import Benchmark

from cilissa.images import Image, ImageCollection, ImagePair
from cilissa.metrics import MSE, PSNR
from cilissa.operations import OperationsList
from cilissa.transformations import Blur, Equalization


class BenchmarkOperationsList(Benchmark):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_path = os.path.dirname(__file__)
        cls.data_path = Path(cls.base_path, "..", "data")

        cls.mse, cls.psnr = MSE(), PSNR()
        cls.blur, cls.eq = Blur(), Equalization()
        cls.operations = OperationsList([cls.mse, cls.blur, cls.eq, cls.psnr])

    def setUp(self) -> None:
        self.im1 = Image(Path(self.data_path, "ref_images", "monarch.bmp"))
        self.im2 = self.im1.copy()

        self.pair1 = ImagePair(self.im1, self.im2)
        self.pair2 = self.pair1.copy()
        self.collection = ImageCollection([self.pair1, self.pair2])

    def bench_operations_list_pair(self) -> None:
        self.operations.run_all(self.pair1)

    def bench_operations_list_collection(self) -> None:
        self.operations.run_all(self.collection)
