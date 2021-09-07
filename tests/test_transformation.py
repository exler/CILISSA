from pathlib import Path

from cilissa.images import Image
from cilissa.transformations import (
    Blur,
    Equalization,
    Linear,
    Sharpen,
    Transformation,
    Translation,
)
from tests.base import BaseTest


class TestImageTransformation(BaseTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.ref_image = Image(Path(cls.data_path, "ref_images", "monarch.bmp"))

    def use_transformation(self, t: Transformation) -> Image:
        return t.transform(self.ref_image)

    def get_image_for_comparison(self, t_name: str) -> Image:
        return Image(Path(self.data_path, "transformations", f"monarch_{t_name}.bmp"))

    def test_blur_transformation(self) -> None:
        blur = Blur()

        result = self.use_transformation(blur)
        comp = self.get_image_for_comparison("blur")

        self.assertEqual(result, comp)

    def test_equalization_transformation(self) -> None:
        equalization = Equalization()

        result = self.use_transformation(equalization)
        comp = self.get_image_for_comparison("equalization")

        self.assertEqual(result, comp)

    def test_sharpen_transformation(self) -> None:
        sharpen = Sharpen()

        result = self.use_transformation(sharpen)
        comp = self.get_image_for_comparison("sharpen")

        self.assertEqual(result, comp)

    def test_linear_transformation(self) -> None:
        linear = Linear(brightness=50)

        result = self.use_transformation(linear)
        comp = self.get_image_for_comparison("linear")

        self.assertEqual(result, comp)

    def test_translation_transformation(self) -> None:
        translation = Translation(x=40, y=40)

        result = self.use_transformation(translation)
        comp = self.get_image_for_comparison("translation")

        self.assertEqual(result, comp)
