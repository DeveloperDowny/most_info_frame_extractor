import numpy as np


class Analyzer:
    @staticmethod
    def calculate_moving_averages(df, short_window=20, long_window=50):
        df["SMA_short"] = df["char_count"].rolling(window=short_window).mean()
        df["SMA_long"] = df["char_count"].rolling(window=long_window).mean()
        df["crossover"] = np.where(df["SMA_short"] > df["SMA_long"], 1, 0)
        df["crossover_change"] = df["crossover"].diff()
        return df

    @staticmethod
    def calculate_moving_average(array, window):
        return np.convolve(array, np.ones(window), 'valid') / window
