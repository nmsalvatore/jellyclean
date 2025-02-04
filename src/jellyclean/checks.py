import os
import re
from pathlib import Path


def tv_directory(dir: Path) -> bool:
    """Check if directory contains TV show files"""

    return any(re.search(r"\bS0", entry) for entry in os.listdir(dir))


def valid_name_format(entry: str) -> bool:
    """Check if file or directory name is in valid format

    Example:
        My.Home.Movie.1996
        My.Home.Movie.1996.mkv
    """

    match = re.match(r"^(\w+(?:-\w+)?\.)+\d{4}(.mkv|.mp4)?$", entry)
    return match is not None
