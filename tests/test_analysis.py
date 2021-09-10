from pathlib import Path

from numpy import isinf

from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE, PSNR, SSIM, all_metrics
from tests.base import BaseTest


class TestImageAnalysis(BaseTest):
    def test_metric_mse(self) -> None:
        mse = MSE()

        for m_type in self.images_data.values():
            for m in m_type:
                ref_image = Image(Path(self.base_path, m["reference"]))
                mea_image = Image(Path(self.base_path, m["measured"]))
                image_pair = ImagePair(ref_image, mea_image)

                result = mse.analyze(image_pair)

                self.assertAlmostEqual(result, m["metrics"]["mse"], delta=0.1)

    def test_metric_psnr(self) -> None:
        psnr = PSNR()

        for m_type in self.images_data.values():
            for m in m_type:
                ref_image = Image(Path(self.base_path, m["reference"]))
                mea_image = Image(Path(self.base_path, m["measured"]))
                image_pair = ImagePair(ref_image, mea_image)

                result = psnr.analyze(image_pair)

                if m["metrics"]["psnr"] is None:
                    self.assertTrue(isinf(result))
                else:
                    self.assertAlmostEqual(result, m["metrics"]["psnr"], delta=0.1)

    def test_metric_ssim(self) -> None:
        ssim = SSIM()

        for m_type in self.images_data.values():
            for m in m_type:
                ref_image = Image(Path(self.base_path, m["reference"]))
                mea_image = Image(Path(self.base_path, m["measured"]))
                image_pair = ImagePair(ref_image, mea_image)

                result = ssim.analyze(image_pair)

                self.assertAlmostEqual(result, m["metrics"]["ssim"], delta=0.5)

    def test_analyze_grayscale_image(self) -> None:
        grayscale_image = Image(Path(self.data_path, "other", "monarch_grayscale.bmp"))
        image_pair = ImagePair(grayscale_image, grayscale_image.copy())

        for metric in all_metrics.values():
            try:
                metric().analyze(image_pair)
            except Exception:
                self.fail(f"Metric {metric.get_display_name()} failed grayscale image analysis")

    def test_analyze_any_depth(self) -> None:
        image_16bit = Image(Path(self.data_path, "other", "monarch_16bit.tiff"))
        image_16bit_float = Image(Path(self.data_path, "other", "monarch_16bit_float.tiff"))
        image_32bit = Image(Path(self.data_path, "other", "monarch_32bit.tiff"))
        image_32bit_float = Image(Path(self.data_path, "other", "monarch_32bit_float.tiff"))
        images = [image_16bit, image_32bit, image_16bit_float, image_32bit_float]

        for metric in all_metrics.values():
            for image in images:
                image_pair = ImagePair(image, image.copy())
                try:
                    metric().analyze(image_pair)
                except Exception:
                    self.fail(f"Metric {metric.get_display_name()} failed on color depth analysis")
