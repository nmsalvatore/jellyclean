import os
from pathlib import Path
from shutil import rmtree

from jellyclean.file_types import FileExtension


def is_subtitle_directory(entry: Path) -> bool:
    """Check if entry is directory holding subtitles"""

    return os.path.isdir(entry) and any(
        FileExtension.SRT in subentry for subentry in os.listdir(entry)
    )


def extract_clean_subtitles(
    entry: Path, subentry: Path, count: int, clean_name: str
) -> None:
    """Extract subtitles and remove entry directory"""

    for filename in os.listdir(subentry):
        if filename.endswith(FileExtension.SRT) and "eng" in filename.lower():
            os.rename((subentry / filename), (entry / f"{clean_name}.eng.{count}.srt"))

    rmtree(subentry)
