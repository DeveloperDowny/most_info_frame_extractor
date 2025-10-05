from ytvideo2pdf.ocr_strategy.easy_ocr import EasyOCR
from ytvideo2pdf.ocr_strategy.paddle_ocr import PaddleOCR
from ytvideo2pdf.ocr_strategy.tesseract_ocr import Tesseract


class OCRStrategyFactory:
    @staticmethod
    def create_ocr_strategy(ocr_type):
        if ocr_type == "tesseract":
            return Tesseract()
        elif ocr_type == "easy_ocr":
            return EasyOCR()
        elif ocr_type == "paddleocr":
            return PaddleOCR()
        else:
            raise ValueError("Invalid OCR type")
