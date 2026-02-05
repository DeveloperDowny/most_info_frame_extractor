import os
from typing import List

from ytvideo2pdf.extraction_strategy.base_extraction_strategy import (
    BaseExtractionStrategy,
)
from ytvideo2pdf.extraction_strategy.timestamp_extraction_strategy import (
    TimestampExtractionStrategy,
)
from ytvideo2pdf.input_strategy.base import BaseInputStrategy
from ytvideo2pdf.ocr_strategy.ocr_strategy import OCRStrategy
from ytvideo2pdf.utils.constants import BASE_DIR
from ytvideo2pdf.utils.directory_manager import DirectoryManager
from ytvideo2pdf.utils.helper import Helper
from ytvideo2pdf.utils.processed_frame import ProcessedFrame
from ytvideo2pdf.utils.random_generator import RandomGenerator


class PickleInput(BaseInputStrategy):
    def __init__(
        self,
        directory: str,
        ocr_strategy: OCRStrategy,
        extraction_strategy: BaseExtractionStrategy,
        cache_frames: bool = False,
        skip_plot: bool = True,
        **kwargs,
    ):
        super().__init__(cache_frames=cache_frames, skip_plot=skip_plot)
        self.directory = os.path.join(BASE_DIR, directory)
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy

    def get_video_path(self):
        video_path_file_path = os.path.join(self.directory, "video_path.txt")
        video_path = Helper.load_text(video_path_file_path)
        return video_path

    def create_internal_id(self):
        old_internal_id = self.directory.rsplit("_", 2)[0]
        suffix = RandomGenerator.generate_random_word(3)
        new_directory = old_internal_id + "_" + suffix
        DirectoryManager.create_directory(new_directory)
        return new_directory

    def get_frames(self) -> List[ProcessedFrame]:
        python_object_path = os.path.join(self.directory, "processed_frames.pkl")
        processed_frames = Helper.load_python_object(python_object_path)
        return processed_frames

    def configure_extraction_strategy(self):
        if isinstance(self.extraction_strategy, TimestampExtractionStrategy):
            self.extraction_strategy.frame_rate = Helper.get_frame_rate(self.video_path)
