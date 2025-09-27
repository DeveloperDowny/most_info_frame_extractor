import cv2
import easyocr
import numpy as np

from src.video2pdf.ocr_strategy.ocr_strategy import OCRStrategy


class EasyOCR(OCRStrategy):
    def __init__(self):
        self.reader = easyocr.Reader(["en"])

    def extract_text(self, img):
        if isinstance(img, str):
            results = self.reader.readtext(img)
        elif isinstance(img, np.ndarray):
            results = self.reader.readtext(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        text = [result[1] for result in results]
        return " ".join(text)
