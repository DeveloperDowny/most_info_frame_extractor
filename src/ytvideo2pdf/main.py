import logging
import os
import sys
from typing import List, Optional

import typer
from ytvideo2pdf.enums import ExtractionType, InputType, OCRApprovalType, OCRType
from ytvideo2pdf.utils.constants import BASE_DIR
from ytvideo2pdf.utils.directory_manager import DirectoryManager
from pathlib import Path

# Create the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the minimum log level

# Create a stream handler (for stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(stream_formatter)

# Add both handlers to the logger
logger.addHandler(stream_handler)

app = typer.Typer(help="Process a video and extract key frames.")


def parse_timestamps(timestamps_str: str) -> List[float]:
    """Parse comma-separated timestamps into a list of floats."""
    return list(map(float, map(str.strip, timestamps_str.split(","))))


def cleanup_directory(directory):
    if os.path.exists(directory):
        DirectoryManager.delete_directory(directory)
        logger.debug(f"Cleaned up directory: {directory}")


@app.command()
def main(
    input: InputType = typer.Option(
        ...,
        "--input",
        help="Specify the input type.",
    ),
    url: Optional[str] = typer.Option(
        None,
        "--url",
        help="Provide YouTube video/playlist URL if applicable.",
    ),
    dir: Optional[str] = typer.Option(
        None,
        "--dir",
        help="Specify the local directory if input type is 'local'.",
    ),
    interval: int = typer.Option(
        3,
        "--interval",
        help="Specify the interval in seconds for frame extraction.",
    ),
    ocr_approval: OCRApprovalType = typer.Option(
        OCRApprovalType.PHASH,
        "--ocr_approval",
        help="Specify the OCR approval strategy.",
    ),
    ocr: OCRType = typer.Option(
        OCRType.TESSERACT,
        "--ocr",
        help="Specify the OCR strategy.",
    ),
    extraction: ExtractionType = typer.Option(
        ExtractionType.PROMINENT_PEAKS,
        "--extraction",
        help="Specify the extraction strategy.",
    ),
    k: Optional[str] = typer.Option(
        None,
        "--k",
        help="Specify the number of key frames to extract.",
    ),
    timestamps: Optional[str] = typer.Option(
        None,
        "--timestamps",
        help="Specify the key frame timestamps.",
    ),
    cleanup: bool = typer.Option(
        True,
        "--cleanup/--no-cleanup",
        help="Cleanup intermediate files after processing.",
    ),
    threshold: Optional[int] = typer.Option(
        None,
        "--threshold",
        help="Threshold for rate change extraction strategy.",
    ),
    cache_frames: bool = typer.Option(
        False,
        "--cache-frames/--no-cache-frames",
        help="Cache extracted frames to disk.",
    ),
    skip_plot: bool = typer.Option(
        True,
        "--skip-plot/--no-skip-plot",
        help="Skip plotting the OCR text length signal.",
    ),
    res_priority: str = typer.Option(
        "720p",
        "--res-priority",
        help="Preferred resolution for YouTube video download (e.g., '720p', '1080p').",
    ),
):
    from ytvideo2pdf.extraction_strategy.extraction_strategy_factory import (
        ExtractionStrategyFactory,
    )
    from ytvideo2pdf.input_strategy.base import BaseInputStrategy
    from ytvideo2pdf.input_strategy.factory import InputStrategyFactory
    from ytvideo2pdf.ocr_approval.factory import OCRApprovalStrategyFactory
    from ytvideo2pdf.ocr_strategy.ocr_strategy_factory import OCRStrategyFactory
    from ytvideo2pdf.utils.helper import Helper

    # ---- check all attributes and see if they are instance of typer option, if they are set to None
    if isinstance(input, typer.models.OptionInfo):
        input = None
    if isinstance(url, typer.models.OptionInfo):
        url = None
    if isinstance(dir, typer.models.OptionInfo):
        dir = None
    if isinstance(interval, typer.models.OptionInfo):
        interval = 3
    if isinstance(ocr_approval, typer.models.OptionInfo):
        ocr_approval = OCRApprovalType.PHASH
    if isinstance(ocr, typer.models.OptionInfo):
        ocr = OCRType.TESSERACT
    if isinstance(extraction, typer.models.OptionInfo):
        extraction = ExtractionType.PROMINENT_PEAKS
    if isinstance(k, typer.models.OptionInfo):
        k = None
    if isinstance(timestamps, typer.models.OptionInfo):
        timestamps = None
    if isinstance(cleanup, typer.models.OptionInfo):
        cleanup = True
    if isinstance(threshold, typer.models.OptionInfo):
        threshold = None
    if isinstance(cache_frames, typer.models.OptionInfo):
        cache_frames = False
    if isinstance(skip_plot, typer.models.OptionInfo):
        skip_plot = True
    if isinstance(interval, typer.models.OptionInfo):
        interval = 3
    if isinstance(res_priority, typer.models.OptionInfo):
        res_priority = "720p"
    Helper.setup()

    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(ocr_approval)
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(ocr)

    # Parse timestamps if provided
    parsed_timestamps = None
    if timestamps:
        logger.info(f"Parsing timestamps: {timestamps}")
        parsed_timestamps = parse_timestamps(timestamps)
        logger.info(f"Parsed timestamps: {parsed_timestamps}")

    extraction_strategy_args = {
        "timestamps": parsed_timestamps,
        "threshold": threshold,  # default threshold for rate change strategy
    }
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        extraction, **extraction_strategy_args
    )

    if k == "auto":
        extraction_strategy.auto_calculate_k = True
    else:
        if k:
            extraction_strategy.k = int(k)

    if parsed_timestamps:
        extraction_strategy.timestamps = parsed_timestamps

    logger.info(f"Input type: {input}")
    logger.info(f"Video URL: {url}")
    logger.info(f"Local directory: {dir}")
    logger.info(f"Interval: {interval} seconds")
    logger.info(f"Resolution priority: {res_priority}")
    logger.info(f"OCR approval strategy: {ocr_approval}")
    logger.info(f"OCR strategy: {ocr}")
    logger.info(f"Extraction strategy: {extraction}")
    logger.info(f"Number of key frames to extract (k): {k}")
    logger.info(f"Key frame timestamps: {parsed_timestamps}")
    logger.info(f"Threshold: {threshold}")
    logger.info(f"Cache frames: {cache_frames}")
    logger.info(f"Skip plot: {skip_plot}")
    logger.info(f"Cleanup: {cleanup}")

    metadata = {
        "input_type": input.value if isinstance(input, InputType) else input,
        "video_url": url,
        "local_directory": dir,
        "interval": interval,
        "ocr_approval_strategy": ocr_approval.value,
        "ocr_strategy": ocr.value,
        "extraction_strategy": extraction.value,
        "k": k,
        "timestamps": parsed_timestamps,
        "threshold": threshold,
        "cache_frames": cache_frames,
        "skip_plot": skip_plot,
        "cleanup": cleanup,
    }

    input_strategy: BaseInputStrategy = InputStrategyFactory.create_input_strategy(
        input,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        url,
        dir,
        cache_frames,
        skip_plot,
        metadata,
        interval=interval,
        res_priority=res_priority,
    )

    internal_id = input_strategy.process()
    directory = Path(BASE_DIR) / internal_id

    if cleanup:
        directory = str(directory)  # Convert Path object to string for cleanup function
        cleanup_directory(directory)
        cleanup_directory(directory + "_extracted_frames")
        cleanup_directory(directory + "_python_object")
        cleanup_directory(directory + "_plot")
        
        pdf_file_path = str(Path(BASE_DIR) / f"{internal_id}.pdf")
        if Path(pdf_file_path).exists():
            Path(pdf_file_path).unlink()
            logger.debug(f"Removed PDF file: {pdf_file_path}")


if __name__ == "__main__":
    app()
