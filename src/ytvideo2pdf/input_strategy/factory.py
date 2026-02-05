from ytvideo2pdf.input_strategy.base import BaseInputStrategy
from ytvideo2pdf.input_strategy.local_file import LocalFileInput
from ytvideo2pdf.input_strategy.pickle import PickleInput
from ytvideo2pdf.input_strategy.youtube import YouTubeInput


class InputStrategyFactory:
    @staticmethod
    def create_input_strategy(
        input_type,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        url=None,
        directory=None,
        cache_frames=False,
        skip_plot=True,
        metadata=dict(),
    ) -> BaseInputStrategy:
        if input_type == "youtube":
            return YouTubeInput(
                url,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
                cache_frames=cache_frames,
                skip_plot=skip_plot,
                metadata=metadata
            )
        elif input_type == "local":
            return LocalFileInput(
                directory,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
                cache_frames=cache_frames,
                skip_plot=skip_plot,
                metadata=metadata
            )
        elif input_type == "pickle":
            """The directory path should be like this `xxxxxx_python_object`"""
            return PickleInput(
                directory,
                ocr_strategy,
                extraction_strategy,
                cache_frames=cache_frames,
                skip_plot=skip_plot,
                metadata=metadata
            )
        else:
            raise ValueError("Invalid input type")
