from input_strategy import InputStrategy
from processed_frame import ProcessedFrame
from ocr_strategy import OCRStrategy
from extraction_strategy import ExtractionStrategy
from data_plotter import DataPlotter
from random_generator import RandomGenerator
from directory_manager import DirectoryManager
import os
from helper import Helper
from post_processor import PostProcessor

from constants import BASE_DIR

from key_moments_extraction_strategy import KeyMomentsExtractionStrategy
from k_transactions_extraction_strategy import KTransactionsExtractionStrategy

from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
from storage.storage_strategy import StorageStrategy


class YouTubeVideoURLInputStrategy(InputStrategy):
    def __init__(
        self,
        video_url: str,
        ocr_strategy: OCRStrategy,
        extraction_strategy: ExtractionStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
        storage_strategy: StorageStrategy,
    ):
        self.video_url = video_url
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy
        self.ocr_approval_strategy = ocr_approval_strategy
        self.storage_strategy = storage_strategy

    def proceed(self):
        # create base directory
        DirectoryManager.create_directory(BASE_DIR)

        directory = RandomGenerator.generate_random_word(6)
        directory = os.path.join(BASE_DIR, directory)
        DirectoryManager.create_directory(directory)

        Helper.download_youtube_video(self.video_url, directory)

        Helper.log(f"Downloaded video to {directory}")

        video_path = DirectoryManager.get_video_path(directory)

        Helper.index_results(directory, video_path)

        processed_frames = ProcessedFrame.from_video(
            video_path, self.ocr_strategy, self.ocr_approval_strategy
        )

        Helper.save_objects(video_path, processed_frames, directory)

        Helper.log(f"Processed {len(processed_frames)} frames")

        x_data, y_data = ProcessedFrame.get_data_for_plotting(processed_frames)

        plot_directory = directory + "_plot"
        DirectoryManager.create_directory(plot_directory)
        plot_output_path = os.path.join(plot_directory, "plot.png")

        DataPlotter.plot_data(
            x_data,
            y_data,
            "Frame Number",
            "Number of Characters",
            "Number of Characters in OCR Text",
            plot_output_path,
        )

        # TODO: Ideally, this should not be here. Check if there is a better way to do this.
        if isinstance(self.extraction_strategy, KeyMomentsExtractionStrategy):
            self.extraction_strategy.video_url = self.video_url
            self.extraction_strategy.frame_rate = Helper.get_frame_rate(video_path)

        # TODO: Ideally, this should not be here. Check if there is a better way to do this.
        if isinstance(self.extraction_strategy, KTransactionsExtractionStrategy):
            # TODO: This is a hack. Fix this.
            self.extraction_strategy.auto_calculate_k = False
            video_duration = Helper.get_video_duration(self.video_url)
            number_of_slides = Helper.get_number_of_slides(video_duration)
            self.extraction_strategy.k = number_of_slides

        extracted_frames = self.extraction_strategy.extract_frames(processed_frames)

        DataPlotter.plot_data(
            x_data,
            y_data,
            "Frame Number",
            "Number of Characters",
            "Number of Characters in OCR Text",
            plot_output_path,
            extracted_frames=extracted_frames,
        )

        extracted_frames_directory = directory + "_extracted_frames"
        DirectoryManager.create_directory(extracted_frames_directory)

        Helper.save_extracted_frames(
            extracted_frames, video_path, extracted_frames_directory
        )

        Helper.log(f"Extracted frames to {extracted_frames_directory}")

        list_of_files = os.listdir(extracted_frames_directory)

        PostProcessor.add_text_to_frames_and_save(
            extracted_frames_directory, list_of_files, extracted_frames_directory
        )

        output_pdf_path = directory + ".pdf"
        PostProcessor.convert_images_to_pdf(
            extracted_frames_directory, list_of_files, output_pdf_path
        )

        Helper.save_log(video_path, output_pdf_path)

        pdf_url = self.storage_strategy.upload_file(
            output_pdf_path, os.path.basename(output_pdf_path)
        )

        Helper.log(f"Uploaded PDF to {pdf_url}")
