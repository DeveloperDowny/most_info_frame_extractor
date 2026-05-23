import json
import os
import pickle
import re
from math import ceil
from pathlib import Path
import shutil
from typing import TYPE_CHECKING, Any, Iterable, List, Sequence

import pandas as pd
from decord import VideoReader
from PIL import Image
from pytubefix import Playlist, Search, YouTube
from pytubefix.cli import on_progress
from sanitize_filename import sanitize

from ytvideo2pdf.utils.constants import BASE_DIR
from ytvideo2pdf.utils.directory_manager import DirectoryManager

if TYPE_CHECKING:
    from ytvideo2pdf.utils.processed_frame import ProcessedFrame

RESOLUTION_PRIORITY_LIST = ["720p", "480p", "360p"]


class Helper:
    @staticmethod
    def setup() -> None:
        output_directory = BASE_DIR
        DirectoryManager.create_directory(output_directory)

    @staticmethod
    def get_digits(text: str) -> int:
        return int(re.sub(r"\D", "", text))

    @staticmethod
    def build_resolution_priority(res_priority: str) -> List[str]:
        base_res_priority_list = RESOLUTION_PRIORITY_LIST.copy()
        # ---- descending order
        if res_priority in base_res_priority_list:
            index = base_res_priority_list.index(res_priority)
            if index == 0:
                return base_res_priority_list
            first_half = base_res_priority_list[:index]
            second_half = base_res_priority_list[index:]
            first_half.reverse()
            return second_half + first_half
        return base_res_priority_list

    @staticmethod
    def download_youtube_video(
        video_url: str,
        directory: str,
        res_priority: str = "720p",
    ) -> str:
        res_priority = Helper.build_resolution_priority(res_priority)
        yt = YouTube(video_url, on_progress_callback=on_progress)

        streams = None
        for res in res_priority:
            streams = yt.streams.filter(mime_type="video/mp4", res=res)
            if streams:
                break

        if not streams:
            raise Exception("No streams found for the video.")

        title = yt.title
        file_name = f"{title}.mp4"
        file_name = sanitize(file_name)
        streams[0].download(output_path=directory, filename=file_name)
        video_file_name = DirectoryManager.get_video_path(directory)
        return os.path.join(directory, video_file_name)

    @staticmethod
    def save_image(frame_output_path: str, frame_number: int, video_path: str) -> None:
        video_reader = VideoReader(video_path)
        if frame_number < 0 or frame_number >= len(video_reader):
            return
        frame_rgb = video_reader[frame_number].asnumpy()
        Image.fromarray(frame_rgb).save(frame_output_path)

    @staticmethod
    def save_extracted_frames(
        extracted_frames: Iterable["ProcessedFrame"],
        video_path: str,
        extracted_frames_directory: str,
    ) -> None:
        """For all timestamps, reads the corresponding frame of the video and saves it to the dir"""
        frame_numbers = {frame_info.frame_number for frame_info in extracted_frames}
        if not frame_numbers:
            return

        video_reader = VideoReader(video_path)
        for frame_number in sorted(frame_numbers):
            if frame_number < 0 or frame_number >= len(video_reader):
                continue
            frame_output_path = os.path.join(
                extracted_frames_directory, f"frame_{frame_number}.jpg"
            )
            frame_rgb = video_reader[frame_number].asnumpy()
            pil_img = Image.fromarray(frame_rgb)
            pil_img.save(frame_output_path, dpi=(300, 300))

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean the OCR output"""
        # Replace multiple whitespaces with a single space

        # Remove punctuation and special characters
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        text = text.lower()

        return text

    @staticmethod
    def save_python_objects(python_objects: Any, python_object_path: str) -> None:
        """Save python object to pickle file"""
        with open(python_object_path, "wb") as f:
            pickle.dump(python_objects, f)

    @staticmethod
    def save_text(text: str, text_file_path: str) -> None:
        """Save text to text file"""
        with open(text_file_path, "w") as f:
            f.write(text)

    @staticmethod
    def append_text(text: str, text_file_path: str) -> None:
        """Append text to text file"""
        with open(text_file_path, "a") as f:
            f.write(text)

    @staticmethod
    def index_results(directory: str, video_file_path: str) -> None:
        """Save directory to video name mapping"""
        result_file_path = Path(BASE_DIR) / "results.csv"

        if not result_file_path.exists():
            df = pd.DataFrame()
        else:
            df = pd.read_csv(result_file_path, sep="\t")
        new_row = {
            "internal_id": directory,
            "video_path": video_file_path,
        }
        df = pd.concat([df, pd.DataFrame([new_row])])
        df.to_csv(
            result_file_path,
            sep="\t",
            index=False,
        )

    @staticmethod
    def load_python_object(python_object_path: str) -> Any:
        """Load python object from pickle file"""
        with open(python_object_path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def load_text(text_file_path: str) -> str:
        """Load text from text file"""
        with open(text_file_path, "r") as f:
            return f.read()

    @staticmethod
    def get_video_urls_from_playlist(playlist_url: str) -> list[str]:
        """Get video urls from YouTube playlist"""
        playlist = Playlist(playlist_url)
        return playlist.video_urls

    @staticmethod
    def get_video_duration(video_url: str) -> int:
        """
        Get the duration of a video.

        Args:
            video_url (str): The URL of the video.

        Returns:
            int: The duration of the video in seconds.
        """
        video = YouTube(video_url)
        return video.length

    @staticmethod
    def get_number_of_slides(video_duration: int, seconds_per_slide: int = 30) -> int:
        """
        Get the number of slides in a video.

        Args:
            video_duration (int): The duration of the video in seconds.
            seconds_per_slide (int): The number of seconds per slide. Defaults to 10.

        Returns:
            int: The number of slides in the video.
        """

        return ceil(video_duration / seconds_per_slide)

    @staticmethod
    def get_key_moments(video_url: str) -> list[int]:
        """Get the key moments for the video"""
        video = YouTube(video_url)
        key_moments = video.key_moments
        key_moment_start_seconds = [
            key_moment.start_seconds for key_moment in key_moments
        ]
        return key_moment_start_seconds

    @staticmethod
    def get_frame_number_from_seconds(seconds: float, frame_rate: float) -> int:
        """Get approximate frame number for the timestamp"""
        return round(seconds * frame_rate)

    @staticmethod
    def get_key_frame_numbers(
        timestamps: Sequence[float], frame_rate: float
    ) -> list[int]:
        """Get key frame numbers from timestamps."""
        return [
            Helper.get_frame_number_from_seconds(seconds, frame_rate)
            for seconds in timestamps
        ]

    @staticmethod
    def save_objects(
        video_path: str,
        processed_frames: list["ProcessedFrame"],
        python_object_directory: str,
    ) -> str:
        """Save processed_frames to pickle file. Save video path to a text file."""
        DirectoryManager.create_directory(python_object_directory)
        python_object_path = os.path.join(
            python_object_directory, "processed_frames.pkl"
        )
        video_path_text_file_path = os.path.join(
            python_object_directory, "video_path.txt"
        )
        Helper.save_text(video_path, video_path_text_file_path)
        Helper.save_python_objects(processed_frames, python_object_path)
        return python_object_directory

    @staticmethod
    def get_video_name(video_path: str) -> str:
        """Give video name from video_path"""
        video_name = os.path.basename(video_path)
        return video_name

    @staticmethod
    def get_pdf_output_path(
        video_name: str, internal_id: str, output_dir: str = "output"
    ) -> Path:
        """Give output pdf path from video name and internal id"""
        video_name_path = Path(video_name)
        output_dir = Path.cwd().joinpath(output_dir).resolve()
        output_path = output_dir / f"{video_name_path.stem}_{internal_id}.pdf"
        return output_path

    @staticmethod
    def get_frame_rate(video_path: str) -> float:
        """Give video frame rate from video_path"""
        video_reader = VideoReader(video_path)
        return float(video_reader.get_avg_fps() or 0.0)

    @staticmethod
    def get_video_id(video_name: str) -> str:
        try:
            video = Search(video_name).videos[0]
        except IndexError:
            raise ValueError("Invalid video name")
        return video.video_id

    @staticmethod
    def save_json(data: Any, json_file_path: str) -> None:
        """Save data to json file"""

        with open(json_file_path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_json(file_path: str) -> dict[str, Any]:
        """Load data from json file"""
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def parse_timestamps(timestamps_str: str) -> List[float]:
        """Parse comma-separated timestamps into a list of floats."""
        if not timestamps_str:
            return []
        return [float(ts.strip()) for ts in timestamps_str.split(",") if ts.strip()]

    @staticmethod
    def get_internal_id_from_results() -> str:
        results_file = Path(BASE_DIR) / "results.csv"
        results_df = pd.read_csv(results_file, sep="\t")
        return results_df["internal_id"][0]

    @staticmethod
    def copy_output_files(
        internal_id: str | None = None, dest_dir: Path | None = None
    ) -> None:
        source_dir = Path(BASE_DIR)

        # Create destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Copy files from local output to Drive
        for source_file in source_dir.iterdir():
            if source_file.is_file():
                if internal_id:
                    if internal_id not in source_file.name:
                        continue
                    if source_file.name == f"{internal_id}.pdf":
                        continue
                dest_file = dest_dir / source_file.name
                shutil.copy(source_file, dest_file)
                print(f"Saved {source_file.name} to {dest_dir}")
