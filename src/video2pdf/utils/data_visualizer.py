import matplotlib.pyplot as plt
import pandas as pd


class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

        weight_y = 10
        weight_x = 7
        max_chars = df["char_count"].max() / 4

        # plt.figure(figsize=( df.shape[0]  / weight_x, max_chars /weight_y))
        self.figsize = (df.shape[0] / weight_x, max_chars / weight_y)

    @staticmethod
    def plot_decorator(func):
        def wrapper(*args, **kwargs):
            # set style to normal style
            plt.style.use("classic")
            plt.figure(figsize=args[0].figsize)
            func(*args, **kwargs)
            # plt.grid(True, axis="both", linestyle="--", alpha=0.7)
            # color should be light of the grid
            plt.grid(True, axis="both", linestyle="--", alpha=0.7, color="lightgrey")
            plt.xticks(args[0].df["frame_id"], rotation=45, ha="right")

            plt.show()

        return wrapper

    @plot_decorator
    def plot_char_count(self):
        # Plot a histogram of the character count
        plt.hist(self.df["char_count"], bins=30, color="skyblue", edgecolor="black")
        plt.title("Character Count in Text")
        plt.xlabel("Character Count")
        plt.ylabel("Frequency")

    @plot_decorator
    def plot_frame_id_vs_char_count(self):
        # Plot the frame_id vs char_count
        plt.scatter(self.df["frame_id"], self.df["char_count"], color="skyblue")
        plt.title("Frame ID vs Character Count")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")

    @plot_decorator
    def plot_frame_id_vs_char_count_line(self):
        # Plot the frame_id vs char_count with a line connecting the points
        plt.plot(self.df["frame_id"], self.df["char_count"], color="blue")
        plt.title("Frame ID vs Character Count")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")

    @plot_decorator
    def plot_moving_averages(self):
        df = self.df
        plt.plot(
            df["frame_id"], df["char_count"], color="skyblue", label="Character Count"
        )
        plt.plot(
            df["frame_id"],
            df["SMA_short"],
            color="orange",
            label="Short Moving Average",
        )
        plt.plot(
            df["frame_id"], df["SMA_long"], color="red", label="Long Moving Average"
        )
        plt.title("Moving Averages")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")
        plt.legend()

    @plot_decorator
    def plot_crossover_points(self, crossover_points):
        df = self.df
        self.plot_moving_averages()
        plt.scatter(
            crossover_points["frame_id"],
            crossover_points["char_count"],
            color="black",
            label="Crossover Points",
        )
        plt.title("Crossover Points")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")
        plt.legend()
