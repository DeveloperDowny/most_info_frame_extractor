import os
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

import cv2
import numpy as np
import tempfile

from ytvideo2pdf.ocr_strategy.ocr_strategy import OCRStrategy

try:
    from paddleocr import TextRecognition
except ImportError:
    TextRecognition = None
    


class PaddleOCR(OCRStrategy):
    def __init__(self):
        if TextRecognition is None:
            raise ImportError(
                "Run `pip install video2pdf[paddleocr]` to enable support for paddleocr"
            )
        self.model = TextRecognition(device="gpu")

    def extract_text(self, img):
        if isinstance(img, str):
            # img is already a file path
            output = self.model.predict(input=img)
        elif isinstance(img, np.ndarray):
            # Save numpy array to temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                tmp_path = tmp_file.name
                cv2.imwrite(tmp_path, img)

            try:
                output = self.model.predict(input=tmp_path)
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        # Extract text from results
        texts = []
        for res in output:
            if hasattr(res, "res") and isinstance(res.res, dict):
                rec_text = res.res.get("rec_text", "")
                if rec_text:
                    texts.append(rec_text)

        return " ".join(texts)
