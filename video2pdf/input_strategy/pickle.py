import os
from typing import List

from video2pdf.extraction_strategy.base_extraction_strategy import BaseExtractionStrategy
from video2pdf.extraction_strategy.timestamp_extraction_strategy import TimestampExtractionStrategy
from video2pdf.input_strategy.base import BaseInputStrategy
from video2pdf.ocr_strategy.ocr_strategy import OCRStrategy
from video2pdf.utils.constants import BASE_DIR
from video2pdf.utils.directory_manager import DirectoryManager
from video2pdf.utils.helper import Helper
from video2pdf.utils.processed_frame import ProcessedFrame
from video2pdf.utils.random_generator import RandomGenerator


class PickleInput(BaseInputStrategy):
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

    def __init__(self, directory: str, ocr_strategy: OCRStrategy, extraction_strategy: BaseExtractionStrategy):
        super().__init__()
        self.directory = os.path.join(BASE_DIR, directory)
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy
