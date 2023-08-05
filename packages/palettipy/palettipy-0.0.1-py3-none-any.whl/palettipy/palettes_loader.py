"""Module for the load_palettes function"""

import os

from . import config
from .palette import Palette


_palettes: list[Palette] = []


def load_palettes(path: str = config.PALETTES_DIR) -> list[Palette]:
    """
    Load all the palettes found in the `path` directory

    Parameters
    ----------
    path : str, optional
        The color from which to get the nearest palette color (default is config.PALETTES_DIR)

    Returns
    -------
    list[Palette]
        The nearest palette color to from_color
    """
    for palette_file in os.listdir(path):
        palette_path = os.path.join(path, palette_file)
        if os.path.isdir(palette_path):
            load_palettes(palette_path)
            continue
        elif not palette_file.endswith(config.COLORS_EXTENSION):
            continue
        _palettes.append(Palette(os.path.join(palette_path)))
    return sorted(_palettes, key=lambda p: p.name)
