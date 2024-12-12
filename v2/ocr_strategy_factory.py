from tesseract_ocr import Tesseract


class OCRStrategyFactory:
    @staticmethod
    def create_ocr_strategy(ocr_type):
        if ocr_type == "tesseract":
            return Tesseract()
        else:
            raise ValueError("Invalid OCR type")
