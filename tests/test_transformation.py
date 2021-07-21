import os
import unittest
from pathlib import Path

from cilissa.core import ImageTransformer
from cilissa.images import Image
from cilissa.transformations import (
    Blur,
    Equalization,
    Linear,
    Sharpen,
    Transformation,
    Translation,
)


class TestImageTransformation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_path = Path(os.path.dirname(__file__), "data")

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
        linear = Linear(constrast=2, brightness=50)

        result = self.use_transformation(linear)
        comp = self.get_image_for_comparison("linear")

        self.assertEqual(result, comp)

    def test_translation_transformation(self) -> None:
        translation = Translation(x=40, y=40)

        result = self.use_transformation(translation)
        comp = self.get_image_for_comparison("translation")

        self.assertEqual(result, comp)

    def test_image_transformer(self) -> None:
        blur, eq = Blur(), Equalization()
        transformations = [blur, eq]
        transformer = ImageTransformer(transformations)

        result = transformer.transform(self.ref_image)
        comp = self.get_image_for_comparison("multiple")

        self.assertEqual(result, comp)
