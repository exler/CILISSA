import os
from pathlib import Path

from verdandi.benchmark import Benchmark

from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE, PSNR, SSIM


class BenchmarkAnalysis(Benchmark):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_path = os.path.dirname(__file__)
        cls.data_path = Path(cls.base_path, "..", "data")

    def setUp(self) -> None:
        self.im1 = Image(Path(self.data_path, "ref_images", "monarch.bmp"))
        self.im2 = Image(Path(self.data_path, "gblur", "monarch_5.bmp"))
        self.pair = ImagePair(self.im1, self.im2)

    def bench_mse(self) -> None:
        MSE().analyze(self.pair)

    def bench_psnr(self) -> None:
        PSNR().analyze(self.pair)

    def bench_ssim(self) -> None:
        SSIM().analyze(self.pair)
