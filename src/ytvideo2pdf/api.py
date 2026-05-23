import logging
import os
from pathlib import Path
from typing import List, Optional, Sequence, Union

from ytvideo2pdf.enums import ExtractionType, InputType, OCRApprovalType, OCRType
from ytvideo2pdf.utils.constants import BASE_DIR
from ytvideo2pdf.utils.directory_manager import DirectoryManager

logger = logging.getLogger(__name__)


def parse_timestamps(timestamps_str: str) -> List[float]:
    """Parse comma-separated timestamps into a list of floats."""
    if not timestamps_str:
        return []
    return [float(ts.strip()) for ts in timestamps_str.split(",") if ts.strip()]


def cleanup_directory(directory: str) -> None:
    if os.path.exists(directory):
        DirectoryManager.delete_directory(directory)
        logger.debug("Cleaned up directory: %s", directory)


def _normalize_timestamps(
    timestamps: Optional[Union[str, Sequence[float]]],
) -> Optional[List[float]]:
    if timestamps is None:
        return None
    if isinstance(timestamps, str):
        parsed = parse_timestamps(timestamps)
        return parsed if parsed else None
    return list(timestamps)


def run_pipeline(
    *,
    input_type: InputType | str,
    url: Optional[str] = None,
    directory: Optional[str] = None,
    interval: int = 3,
    ocr_approval: OCRApprovalType | str = OCRApprovalType.PHASH,
    ocr: OCRType | str = OCRType.TESSERACT,
    extraction: ExtractionType | str = ExtractionType.RATE_CHANGE_THRESHOLD,
    k: Optional[Union[str, int]] = None,
    timestamps: Optional[Union[str, Sequence[float]]] = None,
    cleanup: bool = True,
    threshold: int | None = 50,
    cache_frames: bool = False,
    skip_plot: bool = True,
    res_priority: str = "720p",
) -> str:
    """Run the extraction pipeline programmatically.

    Args:
        input_type: Input source type (enum or string).
        url: YouTube video/playlist URL when using the YouTube input.
        directory: Local directory when using local or pickle inputs.
        interval: Frame sampling interval in seconds.
        ocr_approval: OCR approval strategy (enum or string).
        ocr: OCR strategy (enum or string).
        extraction: Extraction strategy (enum or string).
        k: Number of key frames or "auto" to infer the count.
        timestamps: Key frame timestamps as a list or comma-separated string.
        cleanup: Remove intermediate artifacts after processing.
        threshold: Threshold for rate-change extraction.
        cache_frames: Cache extracted frames to disk.
        skip_plot: Skip generating OCR signal plots.
        res_priority: Preferred YouTube download resolution (e.g., "720p").

    Returns:
        Internal ID for the run (used as the working directory name).
    """
    from ytvideo2pdf.extraction_strategy.extraction_strategy_factory import (
        ExtractionStrategyFactory,
    )
    from ytvideo2pdf.input_strategy.base import BaseInputStrategy
    from ytvideo2pdf.input_strategy.factory import InputStrategyFactory
    from ytvideo2pdf.ocr_approval.factory import OCRApprovalStrategyFactory
    from ytvideo2pdf.ocr_strategy.ocr_strategy_factory import OCRStrategyFactory
    from ytvideo2pdf.utils.helper import Helper

    if input_type is None:
        raise ValueError("input_type is required")

    Helper.setup()

    ocr_value = ocr.value if isinstance(ocr, OCRType) else ocr
    ocr_approval_value = (
        ocr_approval.value
        if isinstance(ocr_approval, OCRApprovalType)
        else ocr_approval
    )
    extraction_value = (
        extraction.value if isinstance(extraction, ExtractionType) else extraction
    )

    parsed_timestamps = _normalize_timestamps(timestamps)
    if parsed_timestamps is not None:
        logger.info("Parsed timestamps: %s", parsed_timestamps)

    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(ocr_approval)
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(ocr_value)

    extraction_strategy_args = {
        "timestamps": parsed_timestamps,
        "threshold": threshold,
    }
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        extraction, **extraction_strategy_args
    )

    if k == "auto":
        extraction_strategy.auto_calculate_k = True
    elif k is not None:
        extraction_strategy.k = int(k)

    if parsed_timestamps:
        extraction_strategy.timestamps = parsed_timestamps

    logger.info("Input type: %s", input_type)
    logger.info("Video URL: %s", url)
    logger.info("Local directory: %s", directory)
    logger.info("Interval: %s seconds", interval)
    logger.info("Resolution priority: %s", res_priority)
    logger.info("OCR approval strategy: %s", ocr_approval_value)
    logger.info("OCR strategy: %s", ocr_value)
    logger.info("Extraction strategy: %s", extraction_value)
    logger.info("Number of key frames to extract (k): %s", k)
    logger.info("Key frame timestamps: %s", parsed_timestamps)
    logger.info("Threshold: %s", threshold)
    logger.info("Cache frames: %s", cache_frames)
    logger.info("Skip plot: %s", skip_plot)
    logger.info("Cleanup: %s", cleanup)

    metadata = {
        "input_type": input_type.value
        if isinstance(input_type, InputType)
        else input_type,
        "video_url": url,
        "local_directory": directory,
        "interval": interval,
        "ocr_approval_strategy": ocr_approval_value,
        "ocr_strategy": ocr_value,
        "extraction_strategy": extraction_value,
        "k": k,
        "timestamps": parsed_timestamps,
        "threshold": threshold,
        "cache_frames": cache_frames,
        "skip_plot": skip_plot,
        "cleanup": cleanup,
    }

    input_strategy: BaseInputStrategy = InputStrategyFactory.create_input_strategy(
        input_type,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        url,
        directory,
        cache_frames,
        skip_plot,
        metadata,
        interval=interval,
        res_priority=res_priority,
    )

    internal_id = input_strategy.process()
    directory_path = Path(BASE_DIR) / internal_id

    if cleanup:
        directory_str = str(directory_path)
        cleanup_directory(directory_str)
        cleanup_directory(directory_str + "_extracted_frames")
        cleanup_directory(directory_str + "_python_object")
        cleanup_directory(directory_str + "_plot")

        pdf_file_path = str(Path(BASE_DIR) / f"{internal_id}.pdf")
        if Path(pdf_file_path).exists():
            Path(pdf_file_path).unlink()
            logger.debug("Removed PDF file: %s", pdf_file_path)

    return internal_id
