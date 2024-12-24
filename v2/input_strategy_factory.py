from youtube_video_url_input_strategy import YouTubeVideoURLInputStrategy
from input_strategy import InputStrategy

# from local_video_input_strategy import LocalVideoInputStrategy
# from python_object_input_strategy import PythonObjectInputStrategy
# from playlist_input_strategy import PlaylistInputStrategy
from input_data.input_data import InputData


class InputStrategyFactory:

    @staticmethod
    def create_input_strategy(
        input_type,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        input_data: InputData = None,
        storage_strategy=None,
    ) -> InputStrategy:
        if input_type == "youtube":
            if input_data == None:
                input_data = InputData()
                video_url = input("Enter YouTube video URL: ")
                input_data.video_url = video_url

            return YouTubeVideoURLInputStrategy(
                input_data.video_url,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
                storage_strategy,
            )
        # elif input_type == "local":
        #     directory = input("Enter directory path: ")
        #     return LocalVideoInputStrategy(
        #         directory, ocr_strategy, extraction_strategy, ocr_approval_strategy
        #     )
        # elif input_type == "object":
        #     """The directory path should be like this `xxxxxx_python_object`"""
        #     directory = input("Enter directory path: ")
        #     return PythonObjectInputStrategy(
        #         directory, ocr_strategy, extraction_strategy
        #     )
        # elif input_type == "playlist":
        #     playlist_url = input("Enter YouTube playlist URL: ")
        #     start_from = int(input("Enter start from: "))

        #     return PlaylistInputStrategy(
        #         playlist_url,
        #         start_from,
        #         ocr_strategy,
        #         extraction_strategy,
        #         ocr_approval_strategy,
        #     )
        else:
            raise ValueError("Invalid input type")
