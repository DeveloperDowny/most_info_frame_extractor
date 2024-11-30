import re
import yt_down
from random_generator import RandomGenerator
from directory_manager import DirectoryManager
import os
from pytubefix import Playlist, YouTube
import cv2
import pickle

from constants import BASE_DIR

from math import ceil


class Helper:
    @staticmethod
    def get_digits(text: str) -> int:
        return int(re.sub(r"\D", "", text))

    @staticmethod
    def download_youtube_video(video_url: str, directory: str) -> str:

        yt_down.download_youtube_video(video_url, directory)
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
        cap = cv2.VideoCapture(video_path)
        for frame in extracted_frames:
            frame_output_path = os.path.join(
                extracted_frames_directory, f"frame_{frame.frame_number}.jpg"
            )
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame.frame_number)
            ret, frame = cap.read()
            cv2.imwrite(frame_output_path, frame)
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def clean_text(text: str) -> str:
        # Replace multiple whitespaces with a single space

        # Remove punctuation and special characters
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        text = text.lower()

        return text

    @staticmethod
    def save_python_objects(python_objects, python_object_path):
        with open(python_object_path, "wb") as f:
            pickle.dump(python_objects, f)

    @staticmethod
    def save_text(text, text_file_path):
        with open(text_file_path, "w") as f:
            f.write(text)

    @staticmethod
    def append_text(text, text_file_path):
        with open(text_file_path, "a") as f:
            f.write(text)

    @staticmethod
    def index_results(directory, video_file_path):
        formatted_text = f"\n{directory} -> {video_file_path}"
        result_file_path = os.path.join(BASE_DIR, "results.txt")
        Helper.append_text(formatted_text, result_file_path)

    @staticmethod
    def load_python_object(python_object_path):
        with open(python_object_path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def load_text(text_file_path):
        with open(text_file_path, "r") as f:
            return f.read()

    @staticmethod
    def get_video_urls_from_playlist(playlist_url: str) -> list:
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
        video = YouTube(video_url)
        key_moments = video.key_moments
        key_moment_start_seconds = [
            key_moment.start_seconds for key_moment in key_moments
        ]
        return key_moment_start_seconds

    @staticmethod
    def get_frame_number_from_seconds(seconds: int, frame_rate: int) -> int:
        return seconds * frame_rate

    @staticmethod
    def get_key_moments_from_seconds(key_moments, frame_rate):
        return [
            Helper.get_frame_number_from_seconds(key_moment, frame_rate)
            for key_moment in key_moments
        ]

    @staticmethod
    def log(message: str):
        print(message)

    def save_objects(video_path, processed_frames, directory):
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

    @staticmethod
    def get_video_name(video_path):
        video_name = os.path.basename(video_path)
        return video_name

    @staticmethod
    def save_log(video_path, output_pdf_path):
        video_name = Helper.get_video_name(video_path)
        Helper.log(f"Saved PDF to {output_pdf_path} for {video_name}")

    @staticmethod
    def get_frame_rate(video_path):
        cap = cv2.VideoCapture(video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        cv2.destroyAllWindows()
        return frame_rate

    @staticmethod
    def get_segments(directory):
        return "0, 125, 198, 260, 344"

if __name__ == "__main__":
    print(Helper.get_digits("frame_234.jpg"))
