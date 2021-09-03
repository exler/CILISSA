from pathlib import Path

from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE
from cilissa.roi import ROI
from cilissa.transformations import Equalization
from tests.base import BaseTest


class TestROI(BaseTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.base_image = Image(Path(cls.data_path, "ref_images", "parrots.bmp"))
        cls.transformed_image = Image(Path(cls.data_path, "roi", "roi_transformed.bmp"))

        cls.transformed_roi = ROI(0, 0, 384, 512)
        cls.unchanged_roi = ROI(384, 0, 768, 512)

    def test_roi_transformation(self) -> None:
        result_image = self.base_image.copy()
        cropped_image = result_image.crop(self.transformed_roi.slices)
        transformed_image = Equalization().transform(cropped_image)
        result_image.from_array(transformed_image.im, at=self.transformed_roi.slices)

        self.assertEqual(result_image, self.transformed_image)

    def test_roi_analysis(self) -> None:
        pair = ImagePair(self.base_image, self.transformed_image)
        pair.set_roi(self.unchanged_roi)

        mse = MSE()
        result = mse.analyze(pair)

        self.assertEqual(result, 0)
