import argparse
import logging

from cilissa.cli import get_operation_instances, parse_roi
from cilissa.images import Image, ImagePair
from cilissa.metrics import all_metrics
from cilissa.operations import OperationsList
from cilissa.transformations import all_transformations

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
    parser.add_argument("-i", "--input-image", required=True, help="Image to be analyzed and transformed")
    parser.add_argument(
        "-M",
        "--metric",
        choices=list(all_metrics.keys()),
        action="extend",
        nargs="+",
        required=False,
        help="Which metrics to use for analysis",
    )
    parser.add_argument(
        "-T",
        "--transformation",
        choices=list(all_transformations.keys()),
        action="extend",
        nargs="+",
        required=False,
        help="Which transformations to use on the compared image",
    )
    parser.add_argument(
        "-R", "--roi", help="ROI start and end points for analysis/transformation. Example: `0x0,384x512`"
    )
    parser.add_argument(
        "--kwargs",
        nargs="+",
        help="Keyword arguments to be passed to their respective operation. Example: `ssim-channels-num=3`",
    )
    parser.add_argument("-s", "--show-end-image", action="store_true", help="Shows the image after all transformations")
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on debugging messages")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    image1 = Image(args.ref_image)
    image2 = Image(args.input_image)
    image_pair = ImagePair(image1, image2)

    if args.roi:
        roi = parse_roi(args.roi)
        image_pair.set_roi(roi)

    operations_choices = list(args.metric or []) + list(args.transformation or [])
    instances = get_operation_instances(operations_choices, args.kwargs or [])

    operations = OperationsList(instances["transformations"] + instances["metrics"])
    result = operations.run_all(image_pair)

    if result:
        print(result)

    if args.show_end_image:
        image_pair.im2.display_image()
