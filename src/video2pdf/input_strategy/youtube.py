import os
from typing import List

from video2pdf.extraction_strategy.base_extraction_strategy import (
    BaseExtractionStrategy,
)
from video2pdf.extraction_strategy.key_moments_extraction_strategy import (
    KeyMomentsExtractionStrategy,
)
from video2pdf.extraction_strategy.timestamp_extraction_strategy import (
    TimestampExtractionStrategy,
)
from video2pdf.input_strategy.base import BaseInputStrategy
from video2pdf.ocr_approval.base import OCRApprovalStrategy
from video2pdf.ocr_strategy.ocr_strategy import OCRStrategy
from video2pdf.utils.constants import BASE_DIR
from video2pdf.utils.directory_manager import DirectoryManager
from video2pdf.utils.helper import Helper
from video2pdf.utils.processed_frame import ProcessedFrame
from video2pdf.utils.random_generator import RandomGenerator


class YouTubeInput(BaseInputStrategy):
    def configure_extraction_strategy(self):
        # TODO: Ideally, this should not be here. Check if there is a better way to do this.
        if isinstance(self.extraction_strategy, KeyMomentsExtractionStrategy):
            self.extraction_strategy.video_url = self.video_url
            self.extraction_strategy.frame_rate = Helper.get_frame_rate(self.video_path)

        # TODO: Ideally, this should not be here. Check if there is a better way to do this.
        if isinstance(self.extraction_strategy, TimestampExtractionStrategy):
            self.extraction_strategy.frame_rate = Helper.get_frame_rate(self.video_path)

    def get_video_path(self):
        return DirectoryManager.get_video_path(self.internal_id)

    def create_internal_id(self):
        directory = RandomGenerator.generate_random_word(6)
        directory = os.path.join(BASE_DIR, directory)
        DirectoryManager.create_directory(directory)

        Helper.download_youtube_video(self.video_url, directory)
        return directory

    def get_frames(self) -> List[ProcessedFrame]:
        return ProcessedFrame.from_video(
            self.video_path, self.ocr_strategy, self.ocr_approval_strategy
        )

    def __init__(
            self,
            video_url: str,
            ocr_strategy: OCRStrategy,
            extraction_strategy: BaseExtractionStrategy,
            ocr_approval_strategy: OCRApprovalStrategy,
    ):
        super().__init__()
        self.video_url = video_url
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy
        self.ocr_approval_strategy = ocr_approval_strategy
