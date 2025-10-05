import cv2
import numpy as np

from video2pdf.ocr_strategy.ocr_strategy import OCRStrategy

try:
    import paddleocr
except ImportError:
    paddleocr = None


class PaddleOCR(OCRStrategy):
    def __init__(self):
        if paddleocr is None:
            raise ImportError(
                "Run `pip install video2pdf[paddleocr]` to enable support for paddleocr"
            )
        self.reader = paddleocr.PaddleOCR(use_angle_cls=False, lang="en")

    def extract_text(self, img):
        if isinstance(img, str):
            results = self.reader.ocr(img, cls=False, det=False, rec=True)
        elif isinstance(img, np.ndarray):
            results = self.reader.ocr(
                cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cls=False, det=False, rec=True
            )
        result = results[0]
        texts = [i[0] for i in result]
        return " ".join(texts)
