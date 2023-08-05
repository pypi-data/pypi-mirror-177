"""
palettipy
---------
Match the colors of an image to a palette
"""
import numpy as np
from PIL import Image

from .palette import Palette


def palettipy_image(palette: Palette, image: Image.Image) -> np.ndarray:
    """Get an image processed with the `palette` colors

    Parameters
    ----------
    palette : Palette
        The palette choosen to process the image
    image : Image
        The image to process

    Returns
    -------
    ndarray
        The processed image as a numpy ndarray
    """
    palette.load_colors()
    palette.cache_colorcube()
    image = np.asarray(image)
    colorcube = palette.load_colorcube()
    shape = image.shape
    indices = image.reshape((-1, shape[2]))
    output_image = colorcube[indices[:, 0], indices[:, 1], indices[:, 2]]
    return output_image.reshape(shape[0], shape[1], 3).astype(np.uint8)
