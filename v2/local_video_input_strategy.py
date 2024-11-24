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

from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy


class LocalVideoInputStrategy(InputStrategy):
    def __init__(
        self,
        directory: str,
        ocr_strategy: OCRStrategy,
        extraction_strategy: ExtractionStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
        start_seconds: int = 0,
        end_seconds: int = None,
    ):
        self.directory = os.path.join(BASE_DIR, directory)
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy
        self.ocr_approval_strategy = ocr_approval_strategy
        self.start_seconds = start_seconds
        self.end_seconds = end_seconds

    def proceed(self):
        suffix = RandomGenerator.generate_random_word(3)
        new_directory = self.directory + "_" + suffix
        DirectoryManager.create_directory(new_directory)

        Helper.log(f"Created {new_directory}")

        video_path = DirectoryManager.get_video_path(self.directory)

        Helper.index_results(new_directory, video_path)

        processed_frames = ProcessedFrame.from_video(
            video_path, self.ocr_strategy, self.ocr_approval_strategy, self.start_seconds, self.end_seconds
        )

        Helper.log(f"Processed {len(processed_frames)} frames")

        Helper.save_objects(video_path, processed_frames, new_directory)

        x_data, y_data = ProcessedFrame.get_data_for_plotting(processed_frames)

        plot_directory = new_directory + "_plot"
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

        extracted_frames_directory = new_directory + "_extracted_frames"
        DirectoryManager.create_directory(extracted_frames_directory)

        Helper.save_extracted_frames(
            extracted_frames, video_path, extracted_frames_directory
        )

        Helper.log(f"Extracted frames to {extracted_frames_directory}")

        list_of_files = os.listdir(extracted_frames_directory)

        PostProcessor.add_text_to_frames_and_save(
            extracted_frames_directory, list_of_files, extracted_frames_directory
        )

        output_pdf_path = new_directory + ".pdf"
        PostProcessor.convert_images_to_pdf(
            extracted_frames_directory, list_of_files, output_pdf_path
        )

        Helper.save_log(video_path, output_pdf_path)
