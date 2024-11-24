import cv2
from typing import Iterator
from frame import Frame


class VideoProcessor:

    @staticmethod
    def get_frames(
        video_path: str, interval: int, start_seconds: int, end_seconds: int
    ) -> Iterator[Frame]:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval)

        try:
            frame_number = 0
            while cap.isOpened():
                if (
                    end_seconds is not None
                    and VideoProcessor.get_timestamp_from_frame_number(
                        video_path, frame_number
                    )
                    > end_seconds
                ):
                    break

                ret, frame = cap.read()
                if not ret:
                    break

                if frame_number % frame_interval == 0:
                    if (
                        start_seconds is not None
                        and VideoProcessor.get_timestamp_from_frame_number(
                            video_path, frame_number
                        )
                        < start_seconds
                    ):
                        pass
                    else:
                        yield Frame(frame_number, frame)

                frame_number += 1
        finally:
            cap.release()

    @staticmethod
    def get_timestamp_from_frame_number(video_path: str, frame_number: int) -> float:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamp = frame_number / fps
        cap.release()
        return timestamp
