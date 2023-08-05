import os

import pytest

import palettipy.config as config
import palettipy.palettes_loader as palettes_loader


SEP = "/"
TESTS_DIR = "palettipy/tests"


def test_palettes_loader(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(os, "sep", SEP)
    monkeypatch.setattr(config, "PALETTES_DIR", TESTS_DIR)

    test_palettes = palettes_loader.load_palettes(TESTS_DIR)

    assert len(test_palettes) == 5
