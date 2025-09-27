from abc import abstractmethod, ABC
from typing import List

from src.video2pdf.utils.processed_frame import ProcessedFrame


class BaseExtractionStrategy(ABC):

    @abstractmethod
    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        pass
