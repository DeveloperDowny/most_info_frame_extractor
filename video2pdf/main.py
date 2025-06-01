import argparse
import logging
import os

from video2pdf.extraction_strategy.extraction_strategy_factory import ExtractionStrategyFactory
from video2pdf.input_strategy.base import BaseInputStrategy
from video2pdf.input_strategy.factory import InputStrategyFactory
from video2pdf.ocr_approval.factory import OCRApprovalStrategyFactory
from video2pdf.ocr_strategy.ocr_strategy_factory import OCRStrategyFactory
from video2pdf.utils.directory_manager import DirectoryManager
from video2pdf.utils.helper import Helper

log_file_name = os.getenv("LOG_FILE_NAME", "logs/video2pdf.log")
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO,
                    filename=log_file_name)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process a video and extract key frames."
    )
    parser.add_argument(
        "--input",
        required=True,
        choices=["youtube", "local", "pickle", "playlist"],
        help="Specify the input type.",
    )
    parser.add_argument(
        "--url", help="Provide YouTube video/playlist URL if applicable."
    )
    parser.add_argument(
        "--dir", help="Specify the local directory if input type is 'local'."
    )
    parser.add_argument(
        "--ocr_approval",
        choices=["pixel_comparison", "approve_all", "reject_all", "phash"],
        default="phash",
        help="Specify the OCR approval strategy.",
    )
    parser.add_argument(
        "--ocr",
        choices=["tesseract", "easy"],
        default="tesseract",
        help="Specify the OCR strategy.",
    )
    parser.add_argument(
        "--extraction",
        choices=["k_transactions", "key_moments", "timestamps", "prominent_peaks"],
        default="prominent_peaks",
        help="Specify the extraction strategy.",
    )
    parser.add_argument(
        "--k",
        type=str,
        help="Specify the number of key frames to extract.",
        default=None,
    )
    parser.add_argument(
        "--timestamps",
        type=lambda x: list(map(float, map(str.strip, x.split(",")))),
        help="Specify the key frame timestamps.",
        default=None,
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Cleanup intermediate files after processing.",
    )
    return parser.parse_args()


def cleanup_directory(directory):
    if os.path.exists(directory):
        DirectoryManager.delete_directory(directory)
        print(f"Cleaned up directory: {directory}")


def main():
    args = parse_arguments()
    Helper.setup()

    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(
        args.ocr_approval
    )
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(args.ocr)
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        args.extraction, timestamps=args.timestamps
    )

    if args.k == "auto":
        extraction_strategy.auto_calculate_k = True
    else:
        if args.k:
            extraction_strategy.k = int(args.k)

    if args.timestamps:
        extraction_strategy.timestamps = args.timestamps

    input_strategy: BaseInputStrategy = InputStrategyFactory.create_input_strategy(
        args.input,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        args.url,
        args.dir,
    )

    directory = input_strategy.process()

    if args.cleanup:
        cleanup_directory(directory)
        cleanup_directory(directory + "_extracted_frames")
        cleanup_directory(directory + "_python_object")
        cleanup_directory(directory + "_plot")


if __name__ == "__main__":
    main()
