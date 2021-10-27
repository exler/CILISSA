import argparse

from cilissa.images import Image, ImagePair
from cilissa.operations import OperationsList
from cilissa.parsers import parse_operations_from_str, parse_roi

help_message = """
CILISSA - Interactive computer image likeness assessing.
All arguments passed after `--kwargs` flag and beginning with metric's name will be passed to metric's constructor.
Example: `cilissa -m ssim ssim-channels-num=3` will be created as `SSIM(channels_num=3)`
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description=help_message,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-r", "--ref-image", required=True, help="Reference image against which quality is measured")
    parser.add_argument("-i", "--input-image", required=True, help="Image to be analyzed and transformed")
    parser.add_argument(
        "-O",
        "--operation",
        action="extend",
        nargs="+",
        required=True,
        help="Which operations to use (execution order depends on the order the arguments are passed)",
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
    args = parser.parse_args()

    image1 = Image(args.ref_image)
    image2 = Image(args.input_image)
    image_pair = ImagePair(image1, image2)

    if args.roi:
        roi = parse_roi(args.roi)
        image_pair.set_roi(roi)

    instances = parse_operations_from_str(args.operation or [], args.kwargs or [])
    operations = OperationsList(instances)
    result = operations.run_all(image_pair)

    if result:
        print(result)

    if args.show_end_image:
        image_pair.im2.show()


if __name__ == "__main__":
    main()
