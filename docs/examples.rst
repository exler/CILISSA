Examples
============

Image pair analysis
-------------------

The following script compares 2 images using the SSIM metric via its ``analyze`` method
or uses both the MSE and SSIM metrics **in order** using the ``OperationsList`` class.

.. code-block:: python

    from cilissa.images import Image, ImagePair
    from cilissa.metrics import SSIM, MSE
    from cilissa.operations import OperationsList

    image1 = Image("path/to/original/image")
    image2 = Image("path/to/other/image")
    image_pair = ImagePair(image1, image2)

    # Compare using standalone metric
    ssim = SSIM(channels_num=3)
    result = ssim.analyze(image_pair)

    # Or use OperationsList
    mse = MSE()
    operations = OperationsList([mse, ssim])
    results = operations.run_all(image_pair)

Image transformation
--------------------

The following script transforms a single image with the ``Blur`` transformation using its ``transform`` method.
Transformations can be chained and mixed in the ``OperationsList`` class in the same way as metrics.

.. code-block:: python

    from cilissa.images import Image
    from cilissa.transformations import Blur

    image = Image("path/to/original/image")

    # Transform using standalone transformation
    blur = Blur(gaussian=False, sigma=2.0)
    result = blur.transform(image)
