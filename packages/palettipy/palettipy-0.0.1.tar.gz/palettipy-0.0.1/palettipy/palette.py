"""Module for the Palette class"""

import os

import numpy as np

from . import color, config


class Palette:
    """
    A class used to represent a palette of colors

    Attributes
    ----------
    name : str
        The name of the palette
    colors_path : str
        The path of the palette file
    colorcube_path : str
        The path of the color cube file
    size : int
        The number of colors of the palette
    colors : list[Color]
        The list of Color objects
    colors_rgb : list[list[int]]
        The list of colors as rgb values

    Methods
    -------
    load_colors()
        Load self.colors and self.colors_rgb from self.colors_path file
    """

    def __init__(self, path: str):
        """
        Parameters
        ----------
        path : str
            The path of the palette colors file
        """
        self.name = (
            path.replace(f"{config.PALETTES_DIR}{os.sep}", "")
            .replace(os.sep, " ")
            .replace("_", " ")
            .replace(config.COLORS_EXTENSION, "")
        )
        self.colors_path = path
        self.colorcube_path = self.colors_path.replace(config.COLORS_EXTENSION, ".npz")
        self.size = 0
        self.colors = []
        self.colors_rgb = []

    def load_colors(self):
        """
        Load `self.colors` and `self.colors_rgb` from the `self.colors_path` file
        """
        colors = []
        with open(self.colors_path, "rt", encoding="UTF-8") as palette_colors_file:
            for num, _hex in enumerate(palette_colors_file, 1):
                color_hex = _hex.rstrip()
                if not color_hex.startswith("#") or len(color_hex) != 7:
                    raise Exception(
                        f'[{self.name}] Error in "{self.colors_path}" at line {num}: Colors must be in format "#000000" (got "{color_hex}")'
                    )
                if not color_hex.removeprefix("#").isalnum():
                    raise Exception(
                        f'[{self.name}] Error in "{self.colors_path}" at line {num}: Invalid color "{color_hex}"'
                    )
                colors.append(color.Color(hex=color_hex))
        self.size = len(colors)
        self.colors: list[color.Color] = colors
        self.colors_rgb: list[list[int]] = [color.rgb for color in self.colors]

    def get_nearest_color(self, from_color: color.Color) -> color.Color:
        """
        Get the nearest palette color for the color argument

        Parameters
        ----------
        from_color : Color
            The color from which to get the nearest palette color

        Returns
        -------
        Color
            The nearest palette color to from_color
        """
        return self.colors[
            np.argmin(
                np.sqrt(
                    np.sum(
                        (np.array(self.colors_rgb) - from_color.rgb) ** 2,
                        axis=1,
                    )
                )
            )
        ]

    def calculte_colorcube(self, begin=0, end=255) -> list[int]:
        """
        Calculate the colorcube from the palette colors

        Parameters
        ----------
        begin : int, optional
            The begin R, G, B value from which to calculate the colorcube (default is 0)
        end : int, optional
            The last R, G, B value from which to calculate the colorcube (default is 255)

        Returns
        -------
        list[int]
            The calculated color cube
        """
        size = end - begin + 1
        colorcube = np.zeros(shape=[size, size, size, 3], dtype=int)
        for i, r_value in enumerate(range(begin, end + 1)):
            for j, g_value in enumerate(range(begin, end + 1)):
                for k, b_value in enumerate(range(begin, end + 1)):
                    colorcube[i, j, k] = self.get_nearest_color(
                        color.Color(rgb=[r_value, g_value, b_value])
                    ).rgb
        return colorcube

    def cache_colorcube(self) -> bool:
        """Cache the colorcube

        Check if the color cube file is present in `self.colorcube_path`, otherwise it calculates
        the color cube and saves it in `self.colorcube_path` as a compressed `.npz` format file

        Returns
        -------
        bool
            A boolean value to indicate if the color cube was calculated in this call
        """
        if os.path.exists(self.colorcube_path):
            self.log("Color cube cached")
            return False
        self.log("Color cube not cached")
        self.log("Calculating color cube...")
        colorcube = np.array(self.calculte_colorcube())
        self.log("Color cube calculated")
        np.savez_compressed(self.colorcube_path, color_cube=colorcube)
        self.log("Color cube cached")
        return True

    def load_colorcube(self) -> np.ndarray:
        """Load the colorcube

        Returns
        -------
        ndarray
            The color cube loaded from the `self.colorcube_path` file
        """
        return np.load(self.colorcube_path)["color_cube"]

    def log(self, *values: object):
        """Print to stdout with the `[<self.name>] ` prefix"""
        print(f"[{self.name}]", *values)

    def __str__(self) -> str:
        return f"<Palette {self.name} ({self.size} colors)>"
