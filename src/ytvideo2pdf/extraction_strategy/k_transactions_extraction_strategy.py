import logging
from typing import List

import numpy as np
import pandas as pd
from scipy import signal
from scipy.ndimage import gaussian_filter1d

from ytvideo2pdf.extraction_strategy.base_extraction_strategy import (
    BaseExtractionStrategy,
)
from ytvideo2pdf.utils.processed_frame import ProcessedFrame

logger = logging.getLogger(__name__)


class KTransactionsExtractionStrategy(BaseExtractionStrategy):
    def __init__(self):
        self.k = None
        self.auto_calculate_k = False

    def calculate_peaks(self, x, y, window_size=5, prominence=0.1, width=None):
        """
        Calculate signal peaks after smoothing.

        Parameters:
        x: array-like, x coordinates of the signal
        y: array-like, y coordinates of the signal
        window_size: int, size of the moving average window
        prominence: float, required prominence of peaks
        width: float or None, required width of peaks
        """
        # Convert inputs to numpy arrays
        x = np.array(x)
        y = np.array(y)

        # Apply Gaussian smoothing to reduce noise
        y_smoothed = gaussian_filter1d(y, sigma=window_size / 3)

        # Apply moving average
        kernel = np.ones(window_size) / window_size
        y_smoothed = np.convolve(y_smoothed, kernel, mode="same")

        # Find peaks in the smoothed signal
        peaks, properties = signal.find_peaks(
            y_smoothed,
            prominence=prominence * (np.max(y_smoothed) - np.min(y_smoothed)),
            width=width,
        )

        return peaks, y_smoothed

    @staticmethod
    def max_profit(prices, n, k):
        if n <= 1 or k == 0:
            return 0, []

        profit = [[0 for _ in range(k + 1)] for _ in range(n)]
        transactions = [[[] for _ in range(k + 1)] for _ in range(n)]

        for i in range(1, n):
            for j in range(1, k + 1):
                max_so_far = 0
                best_transaction = []

                for l in range(i):
                    current_profit = prices[i] - prices[l] + profit[l][j - 1]
                    if current_profit > max_so_far:
                        max_so_far = current_profit
                        best_transaction = transactions[l][j - 1] + [(l, i)]

                if max_so_far > profit[i - 1][j]:
                    profit[i][j] = max_so_far
                    transactions[i][j] = best_transaction
                else:
                    profit[i][j] = profit[i - 1][j]
                    transactions[i][j] = transactions[i - 1][j]

        return profit[n - 1][k], transactions[n - 1][k]

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        # Create the signal from frames
        data = [(frame.frame_number, frame.char_count) for frame in frames]
        df = pd.DataFrame(data, columns=["frame_id", "char_count"])

        # Generate x and y coordinates for signal processing
        x = df.index.values
        y = df["char_count"].values

        if self.auto_calculate_k:
            # Calculate k using signal processing
            peaks, _ = self.calculate_peaks(x, y)
            # Set k as the number of detected peaks
            # self.k = len(peaks) #+ 10
            self.k = len(peaks) + 5
            logger.info(f"Detected {self.k} significant transitions in the signal")

        else:
            # Calculate k using signal processing if not already set
            if self.k is None:
                should_auto_calculate_or_k = input(
                    "Enter 'auto' to auto-calculate k or enter k: "
                )
                if should_auto_calculate_or_k == "auto":
                    peaks, _ = self.calculate_peaks(x, y)
                    # Set k as the number of detected peaks
                    self.k = len(peaks)
                    logger.info(
                        f"Detected {self.k} significant transitions in the signal"
                    )
                else:
                    self.k = int(should_auto_calculate_or_k)

        # Proceed with the original maxProfit calculation
        prices = df["char_count"].values
        n = len(prices)
        max_profit, transactions = self.max_profit(prices, n, self.k)

        return [frames[sell] for _, sell in transactions]
