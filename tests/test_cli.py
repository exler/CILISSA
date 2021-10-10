from cilissa.parsers import parse_operation_instances, parse_roi
from cilissa.roi import ROI
from tests.base import BaseTest


class TestParsers(BaseTest):
    def test_parse_operation_instances(self) -> None:
        operations_str_list = ["ssim", "linear"]
        kwargs_str_list = ["ssim-channels-num=3", "linear-contrast=2", "linear-brightness=10"]

        parsed_operations = parse_operation_instances(operations_str_list, kwargs_str_list)
        parsed_metrics = parsed_operations["metrics"]
        parsed_transformations = parsed_operations["transformations"]

        self.assertEqual(parsed_metrics[0].get_class_name(), "ssim")
        self.assertEqual(parsed_metrics[0].channels_num, 3)

        self.assertEqual(parsed_transformations[0].get_class_name(), "linear")
        self.assertEqual(parsed_transformations[0].contrast, 2)
        self.assertEqual(parsed_transformations[0].brightness, 10)

    def test_parse_roi(self) -> None:
        roi_str = "0x0,384x512"

        parsed_roi = parse_roi(roi_str)

        roi = ROI(0, 0, 384, 512)
        self.assertEqual(parsed_roi, roi)
