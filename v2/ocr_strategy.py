from helper import Helper

class OCRStrategy:
    def extract_text(self, image):
        pass
    def extract_clean_text(self, image):
        text = self.extract_text(image)
        return Helper.clean_text(text)