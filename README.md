<p align="center">
    <img src="docs/logo.png" width="328">
    <p align="center"><strong>C</strong>omputer <strong>I</strong>mage <strong>Li</strong>keness A<strong>ss</strong>essing <strong>A</strong>utomation</p>
</p>

## Requirements

* Python >= 3.7

## Installation

### Build from source

```bash
# Using poetry
$ poetry install
```

## Usage

### GUI

Not yet available

### CLI

CILISSA can be used as a command line program, albeit it has limited functionality compared to the GUI or using the library with your own Python scripts.

Currently the CLI only supports working with a single pair of images.

The parameters of metrics can be modified by passing them to the `--kwargs` argument using the following format:
```
<metric-name>-<parameter-name>=<value>
``` 
where `parameter-name` uses hyphens (-) instead of underscores (_)

**Help message**

```bash
usage: python -m cilissa [-h] -o ORIG_IMAGE -c COMP_IMAGE -m {mse,psnr,ssim} [{mse,psnr,ssim} ...] [-d] [--kwargs KWARGS [KWARGS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -o ORIG_IMAGE, --orig-image ORIG_IMAGE
                        Original image working as a base for comparison
  -c COMP_IMAGE, --comp-image COMP_IMAGE
                        Modified image to be analyzed against the original
  -m {mse,psnr,ssim} [{mse,psnr,ssim} ...], --metric {mse,psnr,ssim} [{mse,psnr,ssim} ...]
                        Which metrics to use for analysis
  -d, --debug           Turn on debugging messages
  --kwargs KWARGS [KWARGS ...]
                        Keyword arguments to be passed to their respective metric. Example: `ssim-channels-num=3`
```

### Library

* Basic example of image pair analysis

```python
from cilissa.images import Image, ImagePair
from cilissa.metrics import SSIM
from cilissa.analyzers import ImageAnalyzer

image1 = Image("path/to/original/image")
image2 = Image("path/to/other/image")
image_pair = ImagePair(image1, image2)

# Compare using standalone metric
ssim = SSIM(channels_num=3)
result = mse.analyze(image_pair)

# Or use ImageAnalyzer
mse = MSE()
analyzer = ImageAnalyzer([mse, ssim])
results = analyzer.analyze_pair(image_pair)
```

