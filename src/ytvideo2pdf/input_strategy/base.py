import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
import shutil
from typing import List, Optional

from ytvideo2pdf.extraction_strategy.base_extraction_strategy import BaseExtractionStrategy
from ytvideo2pdf.utils.data_plotter import DataPlotter
from ytvideo2pdf.utils.directory_manager import DirectoryManager
from ytvideo2pdf.utils.helper import Helper
from ytvideo2pdf.utils.post_processor import PostProcessor
from ytvideo2pdf.utils.processed_frame import ProcessedFrame
from ytvideo2pdf.utils.video_processor import VideoProcessor

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

logger = logging.getLogger()


class BaseInputStrategy(ABC):
    def __init__(self, cache_frames: bool = False, skip_plot: bool = True, metadata=dict()):
        self.cache_frames = cache_frames
        self.skip_plot = skip_plot
        self.extraction_strategy: BaseExtractionStrategy = None
        self.internal_id = None
        self.video_path = None
        self.metadata = metadata

    def process(self):
        # ---- Create internal_id
        self.internal_id = self.create_internal_id()
        logger.info(f"Internal ID: {self.internal_id!r}")
        self.metadata["internal_id"] = self.internal_id

        # ---- Get video path
        self.video_path = self.get_video_path()
        logger.info(f"Video path: {self.video_path!r}")
        self.metadata["video_path"] = self.video_path

        # ---- Save mapping of internal_id to video_path
        logger.info(f"Internal ID for video {self.video_path}: {self.internal_id!r}")
        logger.info(f"Saving internal_id to video_id mapping")
        self.save_video_path()

        # ---- Get frames
        logger.info(f"Getting frames...")
        frames = self.get_frames()
        logger.info(f"Number of frames: {len(frames)!r}")

        logger.info(f"Cache frames: {self.cache_frames!r}, Skip plot: {self.skip_plot!r}")
        # ---- Cache frames
        if self.cache_frames:
            logger.info(f"Caching frames...")
            cache_dir = self.cache_frames_(frames)
            logger.info(f"Caching frames to {cache_dir!r}")
            self.metadata["cached_frames_directory"] = cache_dir

        if not self.skip_plot:
            # ---- Plot graph
            logger.info(f"Plotting signal of varying ocr text length...")
            plot_path = self.plot_graph(frames)
            logger.info(f"Plot path: {plot_path!r}")
            self.metadata["plot_path"] = plot_path

        # ---- Configuring extraction_strategy
        self.configure_extraction_strategy()

        # ---- Extracting key frames
        logger.info(f"Extracting frames...")
        extracted_frames = self.extract_frames(frames)
        logger.info(f"Number of extracted frames: {len(extracted_frames)!r}")
        self.metadata["total_frames"] = len(frames)
        self.metadata["total_extracted_frames"] = len(extracted_frames)
        self.metadata["extracted_frame_numbers"] = [
            frame.frame_number for frame in extracted_frames
        ]
        fps = VideoProcessor.get_frame_rate(self.video_path)
        frame_timestamps = [
            VideoProcessor.get_timestamp_from_frame_number(fps, frame.frame_number)
            for frame in extracted_frames
        ]
        formatted_frame_timestamps = [
            VideoProcessor.get_formatted_time(timestamp)
            for timestamp in frame_timestamps
        ]
        self.metadata["extracted_frame_timestamps"] = frame_timestamps
        self.metadata["extracted_frame_formatted_timestamps"] = formatted_frame_timestamps

        if not self.skip_plot:
            # ---- Plotting key frames
            logger.info(f"Plotting key frames....")
            self.plot_graph(frames, extracted_frames)
            logger.info(f"Plot path: {plot_path!r}")

        # ---- Saving key frames
        logger.info(f"Saving extracted frames...")
        output_dir = self.save_frames(extracted_frames)
        logger.info(f"Extracted frames directory: {output_dir!r}")
        self.metadata["extracted_frames_directory"] = output_dir

        # ---- Post processing
        logger.info(f"Post processing...")
        self.post_process(output_dir)
        logger.info(f"Post processing done successfully")

        # ---- Create PDF
        logger.info(f"Creating PDF...")
        pdf_path = self.create_pdf(output_dir)
        logger.info(f"PDF path: {pdf_path!r}")
        self.metadata["output_pdf_path"] = pdf_path
        # ---- Save video_path to output_pdf_path mapping
        logger.info(f"PDF for video {self.video_path!r}: {pdf_path!r}")
        video_name = Helper.get_video_name(self.video_path)
        self.metadata["video_name"] = video_name
        logger.info(f"Saved PDF to {pdf_path!r} for video {video_name!r}")

        # ---- Copy PDF to output path
        pdf_output_path = Helper.get_pdf_output_path(video_name)
        pdf_output_path.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(str(pdf_path), str(pdf_output_path))
        logger.info(
            f"Result PDF for video {video_name!r} saved at {str(pdf_output_path)}"
        )

        # ---- save metadata
        metadata_output_path = pdf_output_path.with_suffix(".json")
        Helper.save_json(self.metadata, metadata_output_path)
        logger.info(
            f"Metadata for video {video_name!r} saved at {str(metadata_output_path)}"
        )

        return self.internal_id

    @abstractmethod
    def get_video_path(self):
        """Get the path of the video whose key frames are being extracted."""
        raise NotImplementedError()

    @abstractmethod
    def create_internal_id(self):
        """Creates the unique internal ID for the current instance of extraction."""
        raise NotImplementedError()

    @abstractmethod
    def get_frames(self) -> List[ProcessedFrame]:
        """Gets the processed frames"""
        raise NotImplementedError()

    def save_video_path(self):
        """Saves the video_path of the video along with internal_id for future reference"""
        Helper.index_results(self.internal_id, self.video_path)

    def plot_graph(
        self,
        frames: List[ProcessedFrame],
        extracted_frames: Optional[List[ProcessedFrame]] = None,
    ):
        """Plot and save graph of the signal of varying ocr text length"""
        x_data, y_data = ProcessedFrame.get_data_for_plotting(frames)

        plot_directory = self.internal_id + "_plot"
        DirectoryManager.create_directory(plot_directory)
        plot_output_path = os.path.join(plot_directory, "plot.png")

        DataPlotter.plot_data(
            x_data,
            y_data,
            "Frame Number",
            "Number of Characters",
            "Number of Characters in OCR Text",
            plot_output_path,
            extracted_frames=extracted_frames,
        )
        return plot_output_path

    @abstractmethod
    def configure_extraction_strategy(self):
        raise NotImplementedError()

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        """Extract key frames using the extraction strategy."""
        return self.extraction_strategy.extract_frames(frames)

    def save_frames(self, extracted_frames: List[ProcessedFrame]) -> str:
        """Save the extracted frames to a folder"""
        extracted_frames_directory = self.internal_id + "_extracted_frames"
        DirectoryManager.create_directory(extracted_frames_directory)

        Helper.save_extracted_frames(
            extracted_frames, self.video_path, extracted_frames_directory
        )

        return extracted_frames_directory

    @staticmethod
    def post_process(output_dir: str):
        """Add text to extracted frames"""
        list_of_files = os.listdir(output_dir)

        PostProcessor.add_text_to_frames_and_save(output_dir, list_of_files, output_dir)

    def create_pdf(self, output_dir):
        """Create PDF of the extracted frames"""
        output_pdf_path = self.internal_id + ".pdf"
        list_of_files = os.listdir(output_dir)
        PostProcessor.convert_images_to_pdf(output_dir, list_of_files, output_pdf_path)
        return output_pdf_path

    def cache_frames_(self, frames):
        """Save the frames to pickle file along with video path"""
        return Helper.save_objects(self.video_path, frames, self.internal_id)
