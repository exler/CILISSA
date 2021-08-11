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

The parameters of metrics and transformations can be modified by passing them to the `--kwargs` argument using the following format:
```
<operation-name>-<parameter-name>=<value>
``` 
where `parameter-name` uses hyphens (-) instead of underscores (_)

**Help message**

```bash
usage: cilissa [-h] -r REF_IMAGE -c COMP_IMAGE [-m {mse,psnr,ssim} [{mse,psnr,ssim} ...]]
               [-t {blur,sharpen,linear,translation,equalization} [{blur,sharpen,linear,translation,equalization} ...]] [-d]
               [--kwargs KWARGS [KWARGS ...]] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -r REF_IMAGE, --ref-image REF_IMAGE
                        Reference image against which quality is measured
  -c COMP_IMAGE, --comp-image COMP_IMAGE
                        Modified/distorted image to be analyzed
  -m {mse,psnr,ssim} [{mse,psnr,ssim} ...], --metric {mse,psnr,ssim} [{mse,psnr,ssim} ...]
                        Which metrics to use for analysis
  -t {blur,sharpen,linear,translation,equalization} [{blur,sharpen,linear,translation,equalization} ...], --transformation {blur,sharpen,linear,translation,equalization} [{blur,sharpen,linear,translation,equalization} ...]
                        Which transformations to use on the compared image
  -d, --debug           Turn on debugging messages
  --kwargs KWARGS [KWARGS ...]
                        Keyword arguments to be passed to their respective operation. Example: `ssim-channels-num=3`
  -s, --show-end-image  Shows the image after all transformations
```

### Library

* Example: image pair analysis

```python
from cilissa.images import Image, ImagePair
from cilissa.metrics import SSIM
from cilissa.core import OperationsList

image1 = Image("path/to/original/image")
image2 = Image("path/to/other/image")
image_pair = ImagePair(image1, image2)

# Compare using standalone metric
ssim = SSIM(channels_num=3)
result = ssim.analyze(image_pair)

# Or use OperationsList
mse = MSE()
operations = OperationsList([mse, ssim])
results = operations.run(image_pair)
```

* Example: image transformation
```python
from cilissa.images import Image
from cilissa.transformations import Blur, Equalization
from cilissa.core import OperationsList

image = Image("path/to/original/image")

# Transform using standalone transformation
blur = Blur(gaussian=False, sigma=2.0)
result = blur.transform(image)
```
