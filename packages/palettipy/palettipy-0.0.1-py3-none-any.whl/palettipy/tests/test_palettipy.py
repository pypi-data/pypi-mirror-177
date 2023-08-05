import os

import numpy as np
import pytest
from PIL import Image

import palettipy
from palettipy import config, palette

SEP = "/"
TESTS_DIR = "palettipy/tests"

TEST_PALETTE_COLORS_PATH = f"{TESTS_DIR}/test_palette.txt"
TEST_PALETTE_PATH = f"{TESTS_DIR}/test_palette"
TEST_IMAGE_PATH = f"{TESTS_DIR}/test_image.png"


def test_palettipy_image(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(os, "sep", SEP)
    monkeypatch.setattr(config, "PALETTES_DIR", TESTS_DIR)

    test_palette = palette.Palette(TEST_PALETTE_COLORS_PATH)
    test_palette.load_colors()

    image = Image.open(TEST_IMAGE_PATH)

    image_output = palettipy.palettipy_image(test_palette, image)

    assert image_output.shape == np.asarray(image).shape
    assert np.isin(test_palette.colors_rgb, image_output).all()
