from enum import StrEnum


class OCRApprovalType(StrEnum):
    PIXEL_COMPARISON = "pixel_comparison"
    APPROVE_ALL = "approve_all"
    REJECT_ALL = "reject_all"
    PHASH = "phash"


class ExtractionType(StrEnum):
    K_TRANSACTIONS = "k_transactions"
    KEY_MOMENTS = "key_moments"
    TIMESTAMPS = "timestamps"
    PROMINENT_PEAKS = "prominent_peaks"
    RATE_CHANGE_THRESHOLD = "rate_change_threshold"


class OCRType(StrEnum):
    TESSERACT = "tesseract"
    EASY_OCR = "easy_ocr"
    COMBINED = "paddleocr"
