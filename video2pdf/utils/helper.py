import os
import pickle
import re
from math import ceil
from pathlib import Path
from typing import List

import cv2
import pandas as pd
from PIL import Image
from pytubefix import Playlist
from pytubefix import YouTube
from pytubefix.cli import on_progress

from video2pdf.utils.constants import BASE_DIR
from video2pdf.utils.directory_manager import DirectoryManager


class Helper:
    @staticmethod
    def setup():
        output_directory = BASE_DIR
        DirectoryManager.create_directory(output_directory)

    @staticmethod
    def get_digits(text: str) -> int:
        return int(re.sub(r"\D", "", text))

    @staticmethod
    def download_youtube_video(
            video_url: str,
            directory: str,
            res_priority: List[str] = ["480p", "360p", "720p"],
    ) -> str:

        yt = YouTube(video_url, on_progress_callback=on_progress)

        streams = None
        for res in res_priority:
            streams = yt.streams.filter(mime_type="video/mp4", res=res)
            if streams:
                break

        if not streams:
            raise Exception("No streams found for the video.")

        streams[0].download(directory)
        video_file_name = DirectoryManager.get_video_path(directory)
        return os.path.join(directory, video_file_name)

    @staticmethod
    def save_image(frame_output_path, frame_number, video_path):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cv2.imwrite(frame_output_path, frame)
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def save_extracted_frames(extracted_frames, video_path, extracted_frames_directory):
        """For all timestamps, reads the corresponding frame of the video and saves it to the dir"""
        cap = cv2.VideoCapture(video_path)
        for frame_info in extracted_frames:
            frame_output_path = os.path.join(
                extracted_frames_directory, f"frame_{frame_info.frame_number}.jpg"
            )
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_info.frame_number)
            ret, frame = cap.read()
            if ret and frame is not None:
                # Convert OpenCV image (BGR) to PIL image (RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                pil_img.save(frame_output_path, dpi=(300, 300))  # Save with proper DPI
        cap.release()
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
    def save_python_objects(python_objects, python_object_path):
        """Save python object to pickle file"""
        with open(python_object_path, "wb") as f:
            pickle.dump(python_objects, f)

    @staticmethod
    def save_text(text, text_file_path):
        """Save text to text file"""
        with open(text_file_path, "w") as f:
            f.write(text)

    @staticmethod
    def append_text(text, text_file_path):
        """Append text to text file"""
        with open(text_file_path, "a") as f:
            f.write(text)

    @staticmethod
    def index_results(directory, video_file_path):
        """Save directory to video name mapping"""
        result_file_path = Path(BASE_DIR) / "results.xlsx"

        if not result_file_path.exists():
            df = pd.DataFrame()
        else:
            df = pd.read_excel(result_file_path)
        new_row = {
            "internal_id": directory,
            "video_path": video_file_path,
        }
        df = pd.concat([df, pd.DataFrame([new_row])])
        df.to_excel(result_file_path, index=False)

    @staticmethod
    def load_python_object(python_object_path):
        """Load python object from pickle file"""
        with open(python_object_path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def load_text(text_file_path):
        """Load text from text file"""
        with open(text_file_path, "r") as f:
            return f.read()

    @staticmethod
    def get_video_urls_from_playlist(playlist_url: str) -> list:
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

        # TODO: Call the YouTube API to get the duration of the video
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
    def get_key_moments(video_url: str) -> list:
        """Get the key moments for the video"""
        video = YouTube(video_url)
        key_moments = video.key_moments
        key_moment_start_seconds = [
            key_moment.start_seconds for key_moment in key_moments
        ]
        return key_moment_start_seconds

    @staticmethod
    def get_frame_number_from_seconds(seconds: float, frame_rate: int) -> int:
        """Get approximate frame number for the timestamp"""
        return round(seconds * frame_rate)

    @staticmethod
    def get_key_frame_numbers(timestamps: List[float], frame_rate):
        """Get key frame numbers from timestamps."""
        return [
            Helper.get_frame_number_from_seconds(seconds, frame_rate)
            for seconds in timestamps
        ]

    @staticmethod
    def log(message: str):
        """Print log"""
        print(message)

    @staticmethod
    def save_objects(video_path, processed_frames, directory):
        """Save processed_frames to pickle file. Save video path to a text file."""
        python_object_directory = directory + "_python_object"
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
    def get_video_name(video_path):
        """Give video name from video_path"""
        video_name = os.path.basename(video_path)
        return video_name

    @staticmethod
    def get_frame_rate(video_path):
        """Give video frame rate from video_path"""
        cap = cv2.VideoCapture(video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        cv2.destroyAllWindows()
        return frame_rate
