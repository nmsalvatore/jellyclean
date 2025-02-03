from pathlib import Path

import pytest

from jellyclean.formatting import valid_name, rename_entry, clean_file
from jellyclean.checks import is_tv_directory
from jellyclean.clean import process_directory


@pytest.mark.parametrize(
    "original, new",
    [
        ("Justins.First.Date.1991.1080p.BluRay.x264.YYY", "Justins.First.Date.1991"),
        (
            "Victorian Christmas (2023) [1080p] [DVDRip] [5.1]",
            "Victorian.Christmas.2023",
        ),
        (
            "2001 A Space Oddity 1999 Remastered 1080p BluRay",
            "2001.A.Space.Oddity.1999",
        ),
        ("1980.2010.PROPER.1080p.BluRay.x265-RARBG", "1980.2010"),
        ("Feel The Noise 2000 1975 720p BluRay BLURPP", "Feel.The.Noise.2000.1975"),
        ("Samesies.2004", "Samesies.2004")
    ],
)
def test_rename_directories(original, new):
    assert rename_entry(original) == new


@pytest.mark.parametrize(
    "original, new",
    [
        (
            "Justins.First.Date.1991.1080p.BluRay.x264.YYY.mkv",
            "Justins.First.Date.1991.mkv",
        ),
        (
            "Victorian Christmas (2023) [1080p] [DVDRip] [5.1].mp4",
            "Victorian.Christmas.2023.mp4",
        ),
        (
            "2001 A Space Oddity 1999 Remastered 1080p BluRay.mp4",
            "2001.A.Space.Oddity.1999.mp4",
        ),
        ("1980.2010.PROPER.1080p.BluRay.x265-RARBG.mkv", "1980.2010.mkv"),
        (
            "Feel The Noise 2000 1975 720p BluRay BLURPP.mkv",
            "Feel.The.Noise.2000.1975.mkv",
        ),
        ("Samesies.2004.mp4", "Samesies.2004.mp4"),
    ],
)
def test_rename_files(original, new):
    assert rename_entry(original) == new


@pytest.mark.parametrize(
    "title",
    [
        "Samesies.2004",
        "2001.A.Space.Oddity.1999",
        "1980.2010",
        "Feel.The.Noise.2000.1975",
        "Samesies.2024",
        "Dude-Man.The.Guy.With.The.Stuff.2013"
    ],
)
def test_valid_directories(title):
    assert valid_name(title)


@pytest.mark.parametrize(
    "title",
    [
        "Samesies.2004.mkv",
        "2001.A.Space.Oddity.1999.mp4",
        "1980.2010.mp4",
        "Feel.The.Noise.2000.1975.mkv",
    ],
)
def test_valid_files(title):
    assert valid_name(title)


@pytest.mark.parametrize(
    "title",
    [
        "Samesies.2004.1080p.BluRay",
        "2001.A.Space.Oddity (1999)",
        "Victorian Christmas (2023) [1080p] [DVDRip]",
        "Feel.The.Noise.2000.1975.",
    ],
)
def test_invalid_directories(title):
    assert not valid_name(title)


@pytest.mark.parametrize(
    "title",
    [
        "Samesies.2004.1080p.BluRay.mkv",
        "2001.A.Space.Oddity (1999).mp4",
        "Victorian Christmas (2023) [1080p] [DVDRip]",
        "Feel.The.Noise.2000.19756.mkv",
    ],
)
def test_invalid_files(title):
    assert not valid_name(title)


@pytest.fixture
def temp_directory(tmp_path):
    test_dir: Path = tmp_path / "test_dir"
    test_dir.mkdir(exist_ok=True)
    return test_dir


@pytest.mark.parametrize(
    "messy_name, clean_name",
    [
        ("My.Home.Movie.2018.720p.DVD.x264.HELLO", "My.Home.Movie.2018"),
        (
            "Victorian Christmas (2023) [1080p] [DVDRip] [5.1]",
            "Victorian.Christmas.2023",
        ),
        (
            "2001 A Space Oddity 1999 Remastered 1080p BluRay",
            "2001.A.Space.Oddity.1999",
        ),
        ("1980.2010.PROPER.1080p.BluRay.x265-RARBG", "1980.2010"),
        ("Feel The Noise 2000 1975 720p BluRay BLURPP", "Feel.The.Noise.2000.1975"),
        ("Samesies.2004", "Samesies.2004"),
    ],
)
def test_process_directory(temp_directory, messy_name, clean_name):
    subdir: Path = temp_directory / messy_name
    subdir.mkdir(exist_ok=True)
    (subdir / f"{messy_name}.mkv").touch()
    (subdir / "English_1.srt").touch()
    (subdir / "Subs").mkdir(exist_ok=True)
    (subdir / "Subs" / "English.srt").touch()
    (subdir / "README.md").touch()

    process_directory(temp_directory)

    assert (temp_directory / clean_name).exists()
    assert (temp_directory / clean_name).is_dir()
    assert (temp_directory / clean_name / f"{clean_name}.mkv").exists()
    assert (temp_directory / clean_name / f"{clean_name}.eng.1.srt").exists()
    assert (temp_directory / clean_name / f"{clean_name}.eng.2.srt").exists()
    assert not (temp_directory / clean_name / "README.md").exists()


def test_single_file_cleanup(temp_directory):
    messy_filename = "My Home Movie (1996).mkv"
    clean_name = "My.Home.Movie.1996"
    clean_filename = f"{clean_name}.mkv"
    single_file = temp_directory / messy_filename
    single_file.touch()

    clean_file(temp_directory, single_file)

    assert (temp_directory / clean_name).exists()
    assert (temp_directory / clean_name).is_dir()
    assert (temp_directory / clean_name / clean_filename).exists()


def test_tv_directory_match(temp_directory):
    messy_dirname = "My Home Show (2006) COMPLETE"
    (temp_directory / messy_dirname).mkdir()
    (temp_directory / messy_dirname / "My Home Show S0E1 Pilot.mkv").touch()
    (temp_directory / messy_dirname / "My Home Show S0E2 Apples.mkv").touch()
    (temp_directory / messy_dirname / "My Home Show S0E3 Bananas.mkv").touch()
    (temp_directory / messy_dirname / "My Home Show S0E4 Oranges.mkv").touch()
    (temp_directory / messy_dirname / "My Home Show S0E5 Strawberries.mkv").touch()
    (temp_directory / messy_dirname / "My Home Show S0E6 Kiwi.mkv").touch()

    assert is_tv_directory((temp_directory / messy_dirname))
