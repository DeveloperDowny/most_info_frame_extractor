import re
import shutil
from pathlib import Path
from typing import List

from video2pdf.utils.constants import BASE_DIR


def move_folders(dir: str | Path, archive_dir: Path, to_move: List[str]) -> None:
    dir = Path(dir)

    folders_to_move = []

    all_folders = dir.glob("*/")
    for folder in all_folders:
        for pattern in to_move:
            if re.fullmatch(pattern, folder.name):
                folders_to_move.append(folder)
                break

    archive_dir.mkdir()

    for folder in folders_to_move:
        shutil.move(str(folder), str(archive_dir))

    result_src = dir / "results.xlsx"
    result_src.is_file()

    result_dst = archive_dir / "results.xlsx"

    try:
        shutil.move(str(result_src), str(result_dst))
    except FileNotFoundError:
        pass


def move_files(dir: str | Path, archive_dir: Path, patterns: List[str]) -> None:
    dir = Path(dir)

    files_to_move = []

    all_files = dir.glob("*.pdf")
    for file in all_files:
        for pattern in patterns:
            if re.fullmatch(pattern, file.name):
                files_to_move.append(file)
                break

    archive_dir.mkdir()

    for file in files_to_move:
        shutil.move(str(file), str(archive_dir / file.name))


def move_results_file(archive_dir, dir):
    result_src = dir / "results.txt"
    result_src.is_file()
    result_dst = archive_dir / "results.txt"
    shutil.move(str(result_src), str(result_dst))


def main(name, file_patterns, folder_patterns):
    """Move all the derived folders and files to an archive."""
    # ---- Declare variables
    dir = BASE_DIR
    base_archive_dir = Path("/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/archives")

    # ---- Archiving folders
    folder_archive = construct_archive_dir(name, base_archive_dir)
    move_folders(dir, folder_archive, folder_patterns)

    # ---- Archiving files
    files_archive = construct_archive_dir(name, base_archive_dir, True)
    move_files(dir, files_archive, file_patterns)


def construct_archive_dir(archive_number: int, base_archive_dir: Path | str, for_files: bool = False) -> Path:
    """Construct archive dir path"""
    base_archive_dir = Path(base_archive_dir)
    suffix = "_pdfs" if for_files else ""
    return base_archive_dir / f"data_archive_{archive_number}{suffix}"


if __name__ == "__main__":
    name = "47_tmp_everything_except_local_videos"

    # ---- For moving, the object must be a full match of one of the following pattern
    folder_patterns = [
        r"\w{6}_.*"
    ]
    file_patterns = [
        r"\w{6}_.*.pdf",
    ]
    main(name, file_patterns, folder_patterns)
