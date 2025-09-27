from pathlib import Path


class TextUtil:
    @staticmethod
    def get_directory_and_video_name(input):
        input = input.split(" -> ")

        directory = Path(input[0])
        directory = directory.name

        video_name = Path(input[1])
        video_name = video_name.stem

        return directory, video_name
