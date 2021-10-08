import os
from pathlib import Path

from verdandi.benchmark import Benchmark

from cilissa.images import Image
from cilissa.transformations import Blur, Equalization, Sharpen, Translation


class BenchmarkTransformation(Benchmark):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_path = os.path.dirname(__file__)
        cls.data_path = Path(cls.base_path, "..", "data")

    def setUp(self) -> None:
        self.im1 = Image(Path(self.data_path, "ref_images", "monarch.bmp"))

    def bench_blur(self) -> None:
        Blur().transform(self.im1)

    def bench_sharpen(self) -> None:
        Sharpen().transform(self.im1)

    def bench_equalization(self) -> None:
        Equalization().transform(self.im1)

    def bench_translation(self) -> None:
        Translation(x=64, y=64).transform(self.im1)
