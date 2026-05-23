import logging
import sys
from typing import Optional

import typer
from ytvideo2pdf.api import run_pipeline
from ytvideo2pdf.enums import ExtractionType, InputType, OCRApprovalType, OCRType

# Create the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the minimum log level

# Create a stream handler (for stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(stream_formatter)

# Add both handlers to the logger
if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
    logger.addHandler(stream_handler)

app = typer.Typer(help="Process a video and extract key frames.")


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
        ExtractionType.RATE_CHANGE_THRESHOLD,
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
    threshold: int | None = typer.Option(
        50,
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
    return run_pipeline(
        input_type=input,
        url=url,
        directory=dir,
        interval=interval,
        ocr_approval=ocr_approval,
        ocr=ocr,
        extraction=extraction,
        k=k,
        timestamps=timestamps,
        cleanup=cleanup,
        threshold=threshold,
        cache_frames=cache_frames,
        skip_plot=skip_plot,
        res_priority=res_priority,
    )


if __name__ == "__main__":
    app()
