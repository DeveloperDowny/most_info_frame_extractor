from tesseract_ocr import Tesseract
from easy_ocr import EasyOCR

class OCRStrategyFactory:
    @staticmethod
    def create_ocr_strategy(ocr_type):
        if ocr_type == "tesseract":
            return Tesseract()
        elif ocr_type == "easy":
            return EasyOCR()
        else:
            raise ValueError("Invalid OCR type")