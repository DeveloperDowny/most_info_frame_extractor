from youtube_video_url_input_strategy import YouTubeVideoURLInputStrategy
from input_strategy import InputStrategy
from local_video_input_strategy import LocalVideoInputStrategy
from python_object_input_strategy import PythonObjectInputStrategy
from playlist_input_strategy import PlaylistInputStrategy
from segments_input_strategy import SegmentsInputStrategy

from helper import Helper


class InputStrategyFactory:

    @staticmethod
    def create_input_strategy(
        input_type, ocr_strategy, extraction_strategy, ocr_approval_strategy
    ) -> InputStrategy:
        if input_type == "youtube":
            video_url = input("Enter YouTube video URL: ")
            start_seconds = int(input("Enter start seconds: "))
            end_seconds = int(input("Enter end seconds: "))
            return YouTubeVideoURLInputStrategy(
                video_url,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
                start_seconds,
                end_seconds,
            )
        elif input_type == "local":
            directory = input("Enter directory path: ")
            start_seconds = int(input("Enter start seconds: "))
            end_seconds = int(input("Enter end seconds: "))
            return LocalVideoInputStrategy(
                directory,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
                start_seconds,
                end_seconds,
            )
        elif input_type == "object":
            """The directory path should be like this `xxxxxx_python_object`"""
            directory = input("Enter directory path: ")
            return PythonObjectInputStrategy(
                directory, ocr_strategy, extraction_strategy
            )
        elif input_type == "playlist":
            playlist_url = input("Enter YouTube playlist URL: ")
            start_from = int(input("Enter start from: "))

            return PlaylistInputStrategy(
                playlist_url,
                start_from,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
            )
        elif input_type == "segments":
            directory = input("Enter directory path: ")
            segments = Helper.get_segments(directory)
            segments = [int(x) for x in segments.split(",")]
            return SegmentsInputStrategy(
                segments, directory, ocr_strategy, extraction_strategy, ocr_approval_strategy
            )
        else:
            raise ValueError("Invalid input type")
