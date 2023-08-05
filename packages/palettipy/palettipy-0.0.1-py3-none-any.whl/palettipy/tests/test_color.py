import numpy as np

from palettipy.color import Color


def test_color_default():
    color = Color()
    assert color.hex == "#000000"
    assert (color.rgb == np.array([0, 0, 0])).all()
    assert str(color) == "<Color #000000>"


def test_color_hex():
    color = Color(hex="#ffffff")
    assert color.hex == "#ffffff"
    assert (color.rgb == np.array([255, 255, 255])).all()
    assert str(color) == "<Color #ffffff>"


def test_color_rgb():
    color = Color(rgb=[255, 255, 255])
    assert color.hex == "#ffffff"
    assert (color.rgb == np.array([255, 255, 255])).all()
    assert str(color) == "<Color #ffffff>"
