import cv2


class Frame:
    def __init__(self, frame_number: int, frame: cv2.Mat):
        self.frame_number = frame_number
        self.frame = frame
