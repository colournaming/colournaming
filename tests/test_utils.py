import pytest

from colournaming.utils import rgb2lab


@pytest.mark.parametrize(
    "rgb, expected",
    [
        ((0, 0, 0), (0.0, 0.0, 0.0)),
        ((255, 255, 255), (100.0, 0.0, 0.0)),
        ((255, 0, 0), (53.24, 80.09, 67.20)),
        ((0, 255, 0), (87.73, -86.18, 83.18)),
        ((0, 0, 255), (32.30, 79.19, -107.86)),
        ((128, 128, 128), (53.59, 0.0, 0.0)),
    ],
)
def test_rgb2lab_reference_colours(rgb, expected):
    assert rgb2lab(rgb) == pytest.approx(expected, abs=0.05)


def test_rgb2lab_accepts_strings():
    assert rgb2lab(["255", "0", "0"]) == rgb2lab([255, 0, 0])


def test_rgb2lab_lightness_increases_with_grey_level():
    lightness = [rgb2lab((v, v, v))[0] for v in range(0, 256, 15)]
    assert lightness == sorted(lightness)
