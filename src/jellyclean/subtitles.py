import os
from pathlib import Path
from shutil import rmtree

from jellyclean.file_types import FileExtension


def rename_subtitle(entry: Path, filename: str, new_name: str, count: int) -> int:
    """Rename subtitle file and increment count"""

    os.rename(Path(entry, filename), Path(entry, f"{new_name}.eng.{count}.srt"))
    return count + 1


def is_subtitle_directory(entry: Path) -> bool:
    """Check if entry is directory holding subtitles"""

    return os.path.isdir(entry) and any(
        FileExtension.SRT in subentry for subentry in os.listdir(entry)
    )


def extract_subtitles(entry: Path, count: int, *, subtitle_name: str) -> None:
    """Extract subtitles and remove entry directory"""

    for subentry in os.listdir(entry):
        if "eng" in subentry.lower():
            count = rename_subtitle(entry, subentry, subtitle_name, count)

    rmtree(entry)
