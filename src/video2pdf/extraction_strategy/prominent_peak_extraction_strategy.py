from typing import Any, List

import numpy as np
from scipy.signal import find_peaks

from src.video2pdf.extraction_strategy.base_extraction_strategy import BaseExtractionStrategy
from src.video2pdf.utils.processed_frame import ProcessedFrame


class ProminentPeakExtractionStrategy(BaseExtractionStrategy):
    """
    An extraction strategy that selects frames corresponding to prominent peaks
    in the character count signal using scipy.signal.find_peaks.

    This strategy identifies frames where the character count is significantly
    higher than its surrounding frames, which can indicate stable slides,
    title cards, or important content points in a video (like a presentation).
    The effectiveness depends heavily on the nature of the video content and
    the chosen parameters.
    """

    def __init__(self, prominence: float = 10, distance: int = 12, **kwargs: Any):
        """
        Initializes the ProminentPeakExtractionStrategy.

        Args:
            prominence (float): The required prominence of peaks. This value
                represents the minimum vertical distance a peak must stand out
                from its surrounding signal to be identified. A higher value
                selects only more significant peaks. Defaults to 1.0.
                This parameter often requires tuning based on the typical
                character count variations in the specific video content.
                See `scipy.signal.find_peaks` documentation for more details.
            distance (int): The minimum required horizontal distance (in number
                of frames) between neighboring peaks. Peaks closer than this
                distance will be suppressed, keeping only the highest peak
                in the vicinity. Defaults to 1 (meaning peaks can be adjacent
                if they meet other criteria). Increasing this helps avoid
                selecting frames that are very close temporally.
            **kwargs (Any): Additional keyword arguments to pass directly to
                             `scipy.signal.find_peaks`. This allows for fine-tuning
                             using parameters like `width`, `threshold`, `height`, etc.
                             Example: `ProminentPeakExtractionStrategy(prominence=10, width=5)`
        """
        if not isinstance(prominence, (int, float)) or prominence <= 0:
            raise ValueError("Prominence must be a positive number.")
        if not isinstance(distance, int) or distance < 1:
            raise ValueError("Distance must be an integer greater than or equal to 1.")

        self.prominence = prominence
        self.distance = distance
        # Store any additional keyword arguments for find_peaks
        self.find_peaks_kwargs = kwargs

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        """
        Extracts frames corresponding to prominent peaks in the character count.

        Args:
            frames: A list of ProcessedFrame objects, assumed to be sorted
                    chronologically by frame_number.

        Returns:
            A list of ProcessedFrame objects corresponding to the detected peaks.
            Returns an empty list if no frames are provided or no peaks meeting
            the criteria are found. The order of returned frames matches their
            original order in the input list.
        """
        if not frames:
            # Handle empty input list gracefully
            return []

        # Extract the character count signal as a NumPy array
        # Using float type for compatibility with SciPy functions
        char_counts = np.array([frame.char_count for frame in frames], dtype=float)

        # Handle edge case: find_peaks requires a signal of certain length
        # for meaningful results (at least 3 points for prominence).
        # If the signal is too short, peak detection might not be reliable or useful.
        # As a fallback, return the single frame with the maximum character count.
        if len(char_counts) < 3:
            # Find the frame with the maximum character count
            # max() returns the first element in case of ties, preserving order somewhat
            max_frame = max(frames, key=lambda f: f.char_count, default=None)
            return [max_frame] if max_frame else []  # Return list with the max frame or empty

        try:
            # Find peaks in the character count signal using configured parameters
            # The `_` variable holds the properties dictionary returned by find_peaks,
            # which we don't need for basic index selection.
            peak_indices, _ = find_peaks(
                char_counts,
                prominence=self.prominence,
                distance=self.distance,
                **self.find_peaks_kwargs  # Pass any extra arguments
            )

            # Select the ProcessedFrame objects corresponding to the detected peak indices
            # Maintain the original order by iterating through the sorted peak_indices
            extracted_frames = [frames[i] for i in sorted(peak_indices)]

        except Exception as e:
            # Catch potential errors during peak finding (e.g., invalid kwargs)
            # In a real application, consider logging this error
            print(f"Error during peak finding: {e}")
            return []  # Return empty list on error

        return extracted_frames
