import logging
import os
import sys
from typing import List, Optional

import typer

from ytvideo2pdf.enums import OCRApprovalType
from ytvideo2pdf.extraction_strategy.extraction_strategy_factory import (
    ExtractionStrategyFactory,
)
from ytvideo2pdf.input_strategy.base import BaseInputStrategy
from ytvideo2pdf.input_strategy.factory import InputStrategyFactory
from ytvideo2pdf.ocr_approval.factory import OCRApprovalStrategyFactory
from ytvideo2pdf.ocr_strategy.ocr_strategy_factory import OCRStrategyFactory
from ytvideo2pdf.utils.directory_manager import DirectoryManager
from ytvideo2pdf.utils.helper import Helper


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
    input: str = typer.Option(
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
    ocr_approval: OCRApprovalType = typer.Option(
        OCRApprovalType.PHASH,
        "--ocr_approval",
        help="Specify the OCR approval strategy.",
    ),
    ocr: str = typer.Option(
        "tesseract",
        "--ocr",
        help="Specify the OCR strategy.",
    ),
    extraction: str = typer.Option(
        "prominent_peaks",
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
        "--cleanup",
        help="Cleanup intermediate files after processing.",
    ),
    threshold: Optional[int] = typer.Option(
        None,
        "--threshold",
        help="Threshold for rate change extraction strategy.",
    ),
):
    # ---- check all attributes and see if they are instance of typer option, if they are set to None
    if isinstance(input, typer.models.OptionInfo):
        input = None
    if isinstance(url, typer.models.OptionInfo):
        url = None
    if isinstance(dir, typer.models.OptionInfo):
        dir = None
    if isinstance(ocr_approval, typer.models.OptionInfo):
        ocr_approval = "phash"
    if isinstance(ocr, typer.models.OptionInfo):
        ocr = "tesseract"
    if isinstance(extraction, typer.models.OptionInfo):
        extraction = "prominent_peaks"
    if isinstance(k, typer.models.OptionInfo):
        k = None
    if isinstance(timestamps, typer.models.OptionInfo):
        timestamps = None
    if isinstance(cleanup, typer.models.OptionInfo):
        cleanup = True
    if isinstance(threshold, typer.models.OptionInfo):
        threshold = None

    Helper.setup()

    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(ocr_approval)
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(ocr)

    # Parse timestamps if provided
    parsed_timestamps = None
    if timestamps:
        parsed_timestamps = parse_timestamps(timestamps)

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

    input_strategy: BaseInputStrategy = InputStrategyFactory.create_input_strategy(
        input,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        url,
        dir,
    )

    directory = input_strategy.process()

    if cleanup:
        cleanup_directory(directory)
        cleanup_directory(directory + "_extracted_frames")
        cleanup_directory(directory + "_python_object")
        cleanup_directory(directory + "_plot")


if __name__ == "__main__":
    app()
