import os
import re
from pathlib import Path
from shutil import rmtree

from jellyclean.file_types import FileExtension
from jellyclean.subtitles import (
    extract_clean_subtitles,
    is_subtitle_directory,
)


def cleanup_name(og_name: str) -> str:
    """Check if file or directory name is valid and reformat if not"""

    if not valid_name(og_name):
        new_name: str = rename_entry(og_name)

        if not valid_name(new_name):
            error_message = "Could not validate entry name after reformat"
            raise ValueError(f"{error_message}:\n{og_name} -> {new_name}")

        return new_name

    return og_name


def valid_name(entry: str) -> bool:
    """Check if file or directory name is in valid format

    Example:
        My.Home.Movie.1996
        My.Home.Movie.1996.mkv
    """
    return re.match(r"^(\w+\.)+\d{4}(.mkv|.mp4)?$", entry) is not None


def rename_entry(original_name: str) -> str:
    """Reformat file and directory names to dot-separated movie title and release year

    Example:
        My.Home.Movie.1996
        My.Home.Movie.1996.mkv
    """

    cleaned_name: str = re.sub(r"\s", ".", original_name)
    cleaned_name: str = re.sub(r"[\(\)]", "", cleaned_name)

    cutoff: int = 0
    for year_match in re.finditer(r"(?<=.)\b(?:19|20)\d{2}\b", cleaned_name):
        cutoff = year_match.end()

    ext_match: re.Match[str] | None = re.search(r"(.mkv|.mp4)", original_name)
    if ext_match:
        return cleaned_name[:cutoff] + ext_match.group()

    return cleaned_name[:cutoff]


def clean_file(root_directory: Path, file: Path) -> None:
    """Clean and organize single files into a directory/file structure

    Example of modification:
        My Home Movie (1996) -> My.Home.Movie.1996/My.Home.Movie.1996.mp4
    """

    clean_filename = cleanup_name(file.name)
    clean_dirname: str = re.sub(r"(.mkv|.mp4)", "", clean_filename)
    (root_directory / clean_dirname).mkdir()
    os.rename(file, (root_directory / clean_dirname / clean_filename))


def clean_directory(root_directory: Path, entry: Path) -> None:
    """Clean and organize directory containing movie files

    Example of desired structure:
        My.Home.Movie.1996/My.Home.Movie.1996.mp4
        My.Home.Movie.1996/My.Home.Movie.1996.eng.1.srt
        My.Home.Movie.1996/My.Home.Movie.1996.eng.2.srt
    """

    subtitle_count: int = 1
    clean_dirname: str = cleanup_name(entry.name)

    for subentry in map(lambda e: (entry / e), os.listdir(entry)):
        if subentry.name.endswith((FileExtension.MKV, FileExtension.MP4)):
            clean_filename: str = cleanup_name(subentry.name)
            os.rename(subentry, (entry / clean_filename))

        elif subentry.name.endswith(FileExtension.SRT):
            os.rename(
                subentry,
                (entry / f"{clean_dirname}.eng.{subtitle_count}.srt"),
            )
            subtitle_count = subtitle_count + 1

        elif is_subtitle_directory(subentry):
            extract_clean_subtitles(entry, subentry, subtitle_count, clean_dirname)

        elif os.path.isdir(subentry):
            rmtree(subentry)

        else:
            os.remove(subentry)

    os.rename(entry, (root_directory / clean_dirname))
