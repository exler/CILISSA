import argparse

from cilissa.analyzers import ImageAnalyzer
from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive computer image likeness assessing.")
    parser.add_argument("-b", "--base-image", required=True)
    parser.add_argument("-t", "--test-image", required=True)
    args = parser.parse_args()

    image1 = Image(args.base_image)
    image2 = Image(args.test_image)

    image_pair = ImagePair(image1, image2)

    analyzer = ImageAnalyzer([MSE])
    result = analyzer.analyze_pair(image_pair)
    print(result)
