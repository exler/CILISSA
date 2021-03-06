from pathlib import Path

from cilissa.parsers import (
    parse_operations_from_json,
    parse_operations_from_str,
    parse_roi,
)
from cilissa.roi import ROI
from tests.base import BaseTest


class TestParsers(BaseTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.f = open(Path(cls.data_path, "operations_list.json"))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.f.close()

    def test_parse_operations_from_str(self) -> None:
        operations_str_list = ["ssim", "linear"]
        kwargs_str_list = ["ssim-channels-num=3", "linear-contrast=2", "linear-brightness=10"]

        parsed_operations = parse_operations_from_str(operations_str_list, kwargs_str_list)

        self.assertEqual(parsed_operations[0].get_class_name(), "ssim")
        self.assertEqual(parsed_operations[0].channels_num, 3)

        self.assertEqual(parsed_operations[1].get_class_name(), "linear")
        self.assertEqual(parsed_operations[1].contrast, 2)
        self.assertEqual(parsed_operations[1].brightness, 10)

    def test_parse_operations_from_json(self) -> None:
        parsed_operations = parse_operations_from_json(self.f)
        self.assertEqual(parsed_operations[0].get_class_name(), "mse")
        self.assertEqual(parsed_operations[0].root_mean_square_error, True)

        self.assertEqual(parsed_operations[1].get_class_name(), "linear")
        self.assertEqual(parsed_operations[1].contrast, 4)
        self.assertEqual(parsed_operations[1].brightness, 10)

    def test_parse_roi(self) -> None:
        roi_str = "0x0,384x512"

        parsed_roi = parse_roi(roi_str)

        roi = ROI(0, 0, 384, 512)
        self.assertEqual(parsed_roi, roi)
