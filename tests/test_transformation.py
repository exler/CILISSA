from pathlib import Path

from cilissa.images import Image
from cilissa.transformations import (
    Blur,
    Equalization,
    Linear,
    Sharpen,
    Transformation,
    Translation,
    all_transformations,
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

    def test_transformation_blur(self) -> None:
        blur = Blur()

        result = self.use_transformation(blur)
        comp = self.get_image_for_comparison("blur")

        self.assertEqual(result, comp)

    def test_transformation_equalization(self) -> None:
        equalization = Equalization()

        result = self.use_transformation(equalization)
        comp = self.get_image_for_comparison("equalization")

        self.assertEqual(result, comp)

    def test_transformation_sharpen(self) -> None:
        sharpen = Sharpen()

        result = self.use_transformation(sharpen)
        comp = self.get_image_for_comparison("sharpen")

        self.assertEqual(result, comp)

    def test_transformation_linear(self) -> None:
        linear = Linear(brightness=50)

        result = self.use_transformation(linear)
        comp = self.get_image_for_comparison("linear")

        self.assertEqual(result, comp)

    def test_transformation_translation(self) -> None:
        translation = Translation(x=40, y=40)

        result = self.use_transformation(translation)
        comp = self.get_image_for_comparison("translation")

        self.assertEqual(result, comp)

    def test_transform_grayscale_image(self) -> None:
        grayscale_image = Image(Path(self.data_path, "other", "monarch_grayscale.bmp"))

        for transformation in all_transformations.values():
            try:
                transformation().transform(grayscale_image)
            except Exception:
                self.fail(f"Transformation {transformation.get_display_name()} failed grayscale image transformation")

    def test_transform_any_depth(self) -> None:
        image_16bit = Image(Path(self.data_path, "other", "monarch_16bit.tiff"))
        image_16bit_float = Image(Path(self.data_path, "other", "monarch_16bit_float.tiff"))
        image_32bit = Image(Path(self.data_path, "other", "monarch_32bit.tiff"))
        image_32bit_float = Image(Path(self.data_path, "other", "monarch_32bit_float.tiff"))
        images = [image_16bit, image_32bit, image_16bit_float, image_32bit_float]

        for transformation in all_transformations.values():
            for image in images:
                try:
                    transformation().transform(image)
                except Exception:
                    self.fail(
                        f"Transformation {transformation.get_display_name()} failed on color depth transformation"
                    )
