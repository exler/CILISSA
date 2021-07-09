import argparse
import ast
import logging

from cilissa.analyzers import ImageAnalyzer
from cilissa.images import Image, ImagePair
from cilissa.metrics import get_all_metrics

help_message = """
CILISSA - Interactive computer image likeness assessing.
All arguments passed after `--kwargs` flag and beginning with metric's name will be passed to metric's constructor.
Example: `cilissa -m ssim ssim-channels-num=3` will be created as `SSIM(channels_num=3)`
"""

if __name__ == "__main__":
    all_metrics = get_all_metrics()

    parser = argparse.ArgumentParser(
        description=help_message,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-o", "--orig-image", required=True)
    parser.add_argument("-c", "--comp-image", required=True)
    parser.add_argument("-m", "--metric", choices=list(all_metrics.keys()), action="extend", nargs="+", required=True)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--kwargs", nargs="+")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    image1 = Image(args.orig_image)
    image2 = Image(args.comp_image)
    image_pair = ImagePair(image1, image2)

    metrics = []
    for metric in args.metric:
        metric = all_metrics.get(metric)
        metric_args = [arg for arg in args.kwargs if arg.find(metric.get_metric_name()) == 0]
        kwargs = {}
        for m_arg in metric_args:
            start = len(metric.get_metric_name()) + 1
            evaluate_type = False
            try:
                # Checking if argument has a value supplied
                key = m_arg[start : m_arg.index("=")].replace("-", "_")
                value = m_arg[m_arg.index("=") + 1 :]
                evaluate_type = True
            except ValueError:
                # Argument is a flag
                key = m_arg[start:]
                value = True

            if evaluate_type:
                # Try to figure out the correct type for argument
                try:
                    value = ast.literal_eval(value)
                except ValueError:
                    # Argument is a string or cannot guess correct type
                    pass

            kwargs[key] = value

        metrics.append(metric(**kwargs))

    analyzer = ImageAnalyzer(metrics)
    result = analyzer.analyze_pair(image_pair)
    print(result)
