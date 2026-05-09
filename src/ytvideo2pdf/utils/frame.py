import numpy as np


class Frame:
    def __init__(self, frame_number: int, frame: np.ndarray):
        self.frame_number = frame_number
        self.frame = frame
