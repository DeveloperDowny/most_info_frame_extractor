from input_strategy import InputStrategy
from ocr_strategy import OCRStrategy
from extraction_strategy import ExtractionStrategy
from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy

from local_video_input_strategy import LocalVideoInputStrategy
from k_transactions_extraction_strategy import KTransactionsExtractionStrategy


class SegmentsInputStrategy(InputStrategy):
    def __init__(
        self,
        segments,
        directory,
        ocr_strategy: OCRStrategy,
        extraction_strategy: ExtractionStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
    ):
        self.segments = segments
        self.directory = directory
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy
        if isinstance(self.extraction_strategy, KTransactionsExtractionStrategy):
            # TODO: This is a hack. Fix this.
            # video_duration = Helper.get_video_duration(video_url)
            # number_of_slides = Helper.get_number_of_slides(video_duration)
            # self.extraction_strategy.k = number_of_slides
            # self.extraction_strategy.auto_calculate_k = True
            self.extraction_strategy.k = 1
        self.ocr_approval_strategy = ocr_approval_strategy

    def proceed(self):
        for i in range(1, len(self.segments)):
            start_seconds = self.segments[i - 1]
            end_seconds = self.segments[i]
            print("\n\n====================================")
            print(f"Segment { i } Result")
            print("====================================")
            video_input_strategy = LocalVideoInputStrategy(
                self.directory,
                self.ocr_strategy,
                self.extraction_strategy,
                self.ocr_approval_strategy,
                start_seconds=start_seconds,
                end_seconds=end_seconds,
            )
            video_input_strategy.proceed()
