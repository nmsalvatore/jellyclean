from pathlib import Path

import pytest

from jellyclean.formatting import valid, rename
from jellyclean.jellyclean import clean_dir


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
def test_rename(original, new):
    assert rename(original) == new


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


@pytest.fixture
def temp_directory(tmp_path):
    test_dir: Path = tmp_path / "test_dir"
    test_dir.mkdir(exist_ok=True)

    messy_name = "My.Home.Movie.2018.720p.DVD.x264.HELLO"

    subdir: Path = test_dir / messy_name
    subdir.mkdir(exist_ok=True)
    (subdir / f"{messy_name}.mkv").touch()
    (subdir / "1_English.srt").touch()
    (subdir / "Subs").mkdir(exist_ok=True)
    (subdir / "Subs" / "English.srt").touch()
    (subdir / "README.md").touch()

    return test_dir


def test_clean_dir(temp_directory):
    clean_dir(temp_directory)

    clean_name: str = "My.Home.Movie.2018"

    assert (temp_directory / clean_name).exists()
    assert (temp_directory / clean_name).is_dir()
    assert (temp_directory / clean_name / f"{clean_name}.mkv").exists()
    assert (temp_directory / clean_name / f"{clean_name}.eng.1.srt").exists()
    assert (temp_directory / clean_name / f"{clean_name}.eng.2.srt").exists()
    assert not (temp_directory / clean_name / "README.md").exists()
