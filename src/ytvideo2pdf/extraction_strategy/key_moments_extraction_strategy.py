from typing import List

from ytvideo2pdf.extraction_strategy.base_extraction_strategy import (
    BaseExtractionStrategy,
)
from ytvideo2pdf.utils.helper import Helper
from ytvideo2pdf.utils.processed_frame import ProcessedFrame


class KeyMomentsExtractionStrategy(BaseExtractionStrategy):
    def __init__(self):
        self.video_url = None
        self.frame_rate = None

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        key_moments = Helper.get_key_moments(self.video_url)
        key_frame_numbers = Helper.get_key_frame_numbers(key_moments, self.frame_rate)
        key_frames = []

        for frame_number in key_frame_numbers:
            processed_frame = ProcessedFrame()
            processed_frame.frame_number = frame_number
            key_frames.append(processed_frame)

        return key_frames

        # below code won't work cause interval is 3 in our case and here the interval is 1 (for frames from key_moments)
        # key_frames = []
        # i = 0
        # j = 0

        # n = len(frames)
        # m = len(key_frame_numbers)

        # while j < m:
        #     while frames[i].frame_number < key_frame_numbers[j] and i < n:
        #         i += 1

        #     if frames[i].frame_number == key_frame_numbers[j]:
        #         key_frames.append(frames[i])

        #     j += 1

        # return key_frames
