from typing import Iterator

import cv2
from ytvideo2pdf.utils.frame import Frame


class VideoProcessor:
    @staticmethod
    def get_total_frames(video_path: str, interval: int = 3) -> int:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        frame_interval = int(fps * interval)
        # Calculate how many frames match the interval
        return (total_frame_count + frame_interval - 1) // frame_interval

    @staticmethod
    def get_frames(video_path: str, interval: int) -> Iterator[Frame]:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval)

        try:
            frame_number = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_number % frame_interval == 0:
                    # Create a copy of the frame to ensure the original buffer can be released
                    frame_copy = frame.copy()
                    yield Frame(frame_number, frame_copy)
                    # Explicitly delete the copy after yielding if not needed
                    del frame

                frame_number += 1
        finally:
            cap.release()
            # Call garbage collector explicitly to help clean up any remaining references
            import gc

            gc.collect()
    
    @staticmethod
    def get_frame_rate(video_path: str) -> float:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return fps

    @staticmethod
    def get_timestamp_from_frame_number(fps: float, frame_number: int) -> int:
        timestamp = frame_number / fps
        return int(timestamp)

    @staticmethod
    def get_formatted_time(seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
