from extraction_strategy import ExtractionStrategy
import pandas as pd
from processed_frame import ProcessedFrame
from scipy import signal
import numpy as np
from scipy.ndimage import gaussian_filter1d

from typing import List


class KTransactionsExtractionStrategy(ExtractionStrategy):
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
    def maxProfit(prices, n, k):
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
        data = [(frame.frame_number, frame.ocr_text) for frame in frames]
        df = pd.DataFrame(data, columns=["frame_id", "text"])
        df["char_count"] = df["text"].apply(len)

        # Generate x and y coordinates for signal processing
        x = df.index.values
        y = df["char_count"].values

        if self.auto_calculate_k:
            # Calculate k using signal processing
            peaks, _ = self.calculate_peaks(x, y)
            # Set k as the number of detected peaks
            # self.k = len(peaks) #+ 10
            self.k = len(peaks) + 5
            print(f"Detected {self.k} significant transitions in the signal")
        
        else:
            # Calculate k using signal processing if not already set
            if self.k is None:
                should_auto_calculate_or_k = input(
                    "Enter 'auto' to auto-calculate k or enter k: "
                )
                if should_auto_calculate_or_k == "auto":
                    peaks, _ = self.calculate_peaks(x, y)
                    # Set k as the number of detected peaks
                    self.k = len(peaks) + 5
                    print(f"Detected {self.k} significant transitions in the signal")
                else:
                    self.k = int(should_auto_calculate_or_k)

        # Proceed with the original maxProfit calculation
        prices = df["char_count"].values
        n = len(prices)
        max_profit, transactions = self.maxProfit(prices, n, self.k)

        return [frames[sell] for _, sell in transactions]
