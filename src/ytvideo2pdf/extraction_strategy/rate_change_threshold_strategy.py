import logging
from typing import Any, List

import pandas as pd

from ytvideo2pdf.extraction_strategy.base_extraction_strategy import (
    BaseExtractionStrategy,
)
from ytvideo2pdf.utils.processed_frame import ProcessedFrame

logger = logging.getLogger(__name__)


class RateChangeThresholdStrategy(BaseExtractionStrategy):
    """
    An extraction strategy that selects frames based on significant changes
    in character count between consecutive frames.

    This strategy identifies frames where the rate of change in character
    count exceeds a specified threshold, indicating potential scene changes
    or important content transitions in the video.
    """

    def __init__(self, threshold: float = 10.0, **kwargs: Any):
        """
        Initializes the RateChangeThresholdStrategy.

        Args:
            threshold (float): The minimum rate of change in character count
                required to select a frame. Defaults to 10.0.
            **kwargs (Any): Additional keyword arguments (not used in this strategy).
        """
        if not isinstance(threshold, (int, float)) or threshold <= 0:
            raise ValueError("Threshold must be a positive number.")

        self.threshold = threshold

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        """
        Extract frames where the rate of change in character count exceeds
        the specified threshold.

        Args:
            frames (List[ProcessedFrame]): List of processed frames with
                                            character count information.

        Returns:
            List[ProcessedFrame]: List of selected frames based on rate of
                                  change threshold.
        """
        df = pd.DataFrame()
        for item in frames:
            row = {
                "frame_number": item.frame_number,
                "char_count": item.char_count,
            }
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df["char_count_change"] = df["char_count"].diff()
        
        selected_frame_numbers = []
        
        prevRow = None
        for _, row in df.iterrows():
            if abs(row["char_count_change"]) < self.threshold:
                prevRow = row
                continue
            
            if row["char_count_change"] < 0:
                if prevRow is None:
                    prevRow = row
                    continue
                selected_frame_numbers.append(
                    prevRow["frame_number"],
                )
            else:
                selected_frame_numbers.append(
                    row["frame_number"],
                )
            prevRow = row
        selected_frame_numbers = list(set(selected_frame_numbers))
        selected_frame_numbers.sort()
        selected_frames = [
            frame for frame in frames if frame.frame_number in selected_frame_numbers
        ]
        return selected_frames
