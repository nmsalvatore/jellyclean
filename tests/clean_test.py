import pytest

from jellyclean.formatting import valid, reformat


@pytest.mark.parametrize(
    "original, new",
    [
        ("Godzilla.Minus.One.2023.1080p.BluRay.x264.YG", "Godzilla.Minus.One.2023"),
        ("Wonka (2023) [1080p] [WEBRip] [5.1] [YTS.MX]", "Wonka.2023"),
        (
            "2001 A Space Odyssey 1968 Remastered 1080p BluRay",
            "2001.A.Space.Odyssey.1968",
        ),
        ("1917.2019.PROPER.1080p.BluRay.x265-RARBG", "1917.2019"),
        ("Death Race (2000) 1975 720p BluRay Hindi.mkv", "Death.Race.2000.1975.mkv"),
        ("The.Girl.Next.Door.2004", "The.Girl.Next.Door.2004"),
    ],
)
def test_reformat(original, new):
    assert reformat(original) == new


@pytest.mark.parametrize(
    "title",
    [
        "The.Girl.Next.Door.2004",
        "2001.A.Space.Odyssey.1968",
        "1917.2019",
        "Death.Race.2000.1975",
    ],
)
def test_valid_directories(title):
    assert valid(title)


@pytest.mark.parametrize(
    "title",
    [
        "The.Girl.Next.Door.2004.mkv",
        "2001.A.Space.Odyssey.1968.mp4",
        "1917.2019.mp4",
        "Death.Race.2000.1975.mkv",
    ],
)
def test_valid_files(title):
    assert valid(title)


@pytest.mark.parametrize(
    "title",
    [
        "The.Girl.Next.Door.2004.1080p.BluRay",
        "2001.A.Space.Odyssey (1968)",
        "Wonka (2023) [1080p] [WEBRip]",
        "Death.Race.2000.1975.",
    ],
)
def test_invalid_directories(title):
    assert not valid(title)


@pytest.mark.parametrize(
    "title",
    [
        "The.Girl.Next.Door.2004.1080p.BluRay.mkv",
        "2001.A.Space.Odyssey (1968).mp4",
        "Wonka (2023) [1080p] [WEBRip].mkv",
        "Death.Race.2000.19756.mkv",
    ],
)
def test_invalid_files(title):
    assert not valid(title)
