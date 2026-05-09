from typing import Iterator

from decord import VideoReader

from ytvideo2pdf.utils.frame import Frame


class VideoProcessor:
    @staticmethod
    def get_total_frames(video_path: str, interval: int = 3) -> int:
        video_reader = VideoReader(video_path)
        fps = video_reader.get_avg_fps()
        total_frame_count = len(video_reader)

        frame_interval = int(fps * interval) if fps else 1
        if total_frame_count <= 0 or frame_interval <= 0:
            return 0
        # Calculate how many frames match the interval
        return (total_frame_count + frame_interval - 1) // frame_interval

    @staticmethod
    def get_frames(video_path: str, interval: int) -> Iterator[Frame]:
        video_reader = VideoReader(video_path)
        fps = video_reader.get_avg_fps()
        frame_interval = int(fps * interval) if fps else 1
        if frame_interval <= 0:
            frame_interval = 1

        for frame_number in range(0, len(video_reader), frame_interval):
            frame_rgb = video_reader[frame_number].asnumpy()
            frame_bgr = frame_rgb[:, :, ::-1]
            yield Frame(frame_number, frame_bgr)

    @staticmethod
    def get_frame_rate(video_path: str) -> float:
        video_reader = VideoReader(video_path)
        return float(video_reader.get_avg_fps() or 0.0)

    @staticmethod
    def get_timestamp_from_frame_number(fps: float, frame_number: int) -> int:
        timestamp = frame_number / fps
        return int(timestamp)

    @staticmethod
    def get_formatted_time(seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
