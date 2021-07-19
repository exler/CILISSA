import argparse
import logging

from cilissa.cli import get_operation_instances
from cilissa.core import ImageAnalyzer
from cilissa.images import Image, ImagePair
from cilissa.utils import all_metrics, all_transformations

help_message = """
CILISSA - Interactive computer image likeness assessing.
All arguments passed after `--kwargs` flag and beginning with metric's name will be passed to metric's constructor.
Example: `cilissa -m ssim ssim-channels-num=3` will be created as `SSIM(channels_num=3)`
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=help_message,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-r", "--ref-image", required=True, help="Reference image against which quality is measured")
    parser.add_argument("-c", "--comp-image", required=True, help="Modified/distorted image to be analyzed")
    parser.add_argument(
        "-m",
        "--metric",
        choices=list(all_metrics.keys()),
        action="extend",
        nargs="+",
        required=False,
        help="Which metrics to use for analysis",
    )
    parser.add_argument(
        "-t",
        "--transformation",
        choices=list(all_transformations.keys()),
        action="extend",
        nargs="+",
        required=False,
        help="Which transformations to use on the compared image",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on debugging messages")
    parser.add_argument(
        "--kwargs",
        nargs="+",
        help="Keyword arguments to be passed to their respective metric. Example: `ssim-channels-num=3`",
    )
    parser.add_argument("-s", "--show-end-image", action="store_true", help="Shows the image after all transformations")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    image1 = Image(args.ref_image)
    image2 = Image(args.comp_image)

    operations = list(args.metric or []) + list(args.transformation or [])
    instances = get_operation_instances(operations, args.kwargs or [])

    if len(instances["transformations"]) > 0:
        # transformer = ImageTransformer(instances["transformations"])
        # transformer.transform(image2, inplace=True)
        pass

    if args.show_end_image:
        image2.display()

    image_pair = ImagePair(image1, image2)

    if len(instances["metrics"]) > 0:
        analyzer = ImageAnalyzer(instances["metrics"])  # type: ignore
        result = analyzer.analyze(image_pair)
        print(result)
