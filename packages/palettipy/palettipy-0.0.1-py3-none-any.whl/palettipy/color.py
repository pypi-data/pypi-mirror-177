"""Module for the Color dataclass"""
from dataclasses import dataclass, field


@dataclass
class Color:
    """A class used to store a color

    This dataclass is used to represent a color. It has both hex and rgb values of the color, and
    they default to black. To get a color, the constructor only needs one parameter between
    `hex` and `rgb`, the other one is calculated automatically

    Attributes
    ----------
    hex : str, optional
        The hex string of the color (default is "#000000")
    rgb : list[int], optional
        The RGB value of the color (default is [0, 0, 0])
    """

    hex: str = field(default_factory=str)
    rgb: list[int] = field(default_factory=list)

    def __post_init__(self):
        if self.hex == "" and len(self.rgb) == 0:
            self.hex = "#000000"
            self.rgb = [0, 0, 0]
        elif self.hex == "":
            self.hex = f"#{self.rgb[0]:x}{self.rgb[1]:x}{self.rgb[2]:x}"
        else:
            self.rgb = [int(self.hex.lstrip("#")[i : i + 2], 16) for i in [0, 2, 4]]

    def __str__(self) -> str:
        return f"<Color {self.hex}>"
