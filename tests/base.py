import json
import os
import unittest
from pathlib import Path


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_path = os.path.dirname(__file__)
        cls.data_path = Path(cls.base_path, "data")

        cls.images_data = cls.load_metrics_data()

    @classmethod
    def load_metrics_data(cls) -> None:
        fp = open(Path(cls.data_path, "data.json"))
        return json.load(fp)
