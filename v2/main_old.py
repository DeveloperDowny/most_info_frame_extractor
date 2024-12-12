from input_strategy_factory import InputStrategyFactory
from ocr_strategy_factory import OCRStrategyFactory
from extraction_strategy_factory import ExtractionStrategyFactory
from input_strategy import InputStrategy
from ocr_approval.ocr_approval_strategy_factory import OCRApprovalStrategyFactory


def main():
    ocr_approval_type = "pixel_comparison"
    # ocr_approval_type = "approve_all"
    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(
        ocr_approval_type
    )

    # ocr_type = input("Enter OCR type: ")
    # ocr_type = "tesseract"
    ocr_type = "easy"
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(ocr_type)

    extraction_type = "k_transactions"
    # extraction_type = "key_moments"
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        extraction_type
    )

    # input_type = input("Enter input type: ")
    input_type = "youtube"
    # input_type = "playlist"
    # input_type = "local"
    # input_type = "object"
    input_strategy: InputStrategy = InputStrategyFactory.create_input_strategy(
        input_type, ocr_strategy, extraction_strategy, ocr_approval_strategy
    )
    input_strategy.proceed()


if __name__ == "__main__":
    main()
