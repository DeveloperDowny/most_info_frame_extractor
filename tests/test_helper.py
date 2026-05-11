import pytest

from ytvideo2pdf.utils.helper import Helper


@pytest.mark.parametrize(
    "res_priority,expected",
    [
        ("720p", ["720p", "480p", "360p"]),
        ("480p", ["480p", "360p", "720p"]),
        ("360p", ["360p", "480p", "720p"]),
        ("999p", ["720p", "480p", "360p"]),
    ],
)
def test_build_resolution_priority(res_priority, expected):
    assert Helper.build_resolution_priority(res_priority) == expected