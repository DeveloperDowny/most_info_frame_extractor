from abc import ABC, abstractmethod

from video2pdf.utils.helper import Helper


class OCRStrategy(ABC):
    @abstractmethod
    def extract_text(self, image):
        pass

    def extract_clean_text(self, image):
        text = self.extract_text(image)
        return Helper.clean_text(text)

    def get_char_count(self, image):
        text = self.extract_clean_text(image)
        return len(text)
