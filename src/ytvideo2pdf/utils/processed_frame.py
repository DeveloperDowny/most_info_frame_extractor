import os
from pathlib import Path
import tempfile
from typing import List

from PIL import Image

from tqdm import tqdm
from ytvideo2pdf.ocr_approval.base import OCRApprovalStrategy
from ytvideo2pdf.ocr_strategy.ocr_strategy import OCRStrategy
from ytvideo2pdf.utils.helper import Helper
from ytvideo2pdf.utils.video_processor import VideoProcessor


class ProcessedFrame:
    def __init__(self):
        self.frame_number = 0
        self.char_count = 0

    @staticmethod
    def from_directory(directory, ocr_strategy: OCRStrategy):
        processed_frames = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                frame = ProcessedFrame()
                frame.frame_number = Helper.get_digits(filename)
                frame.char_count = len(
                    ocr_strategy.extract_clean_text(os.path.join(directory, filename))
                )
                processed_frames.append(frame)
        return processed_frames

    @staticmethod
    def from_video(
        video_path,
        ocr_strategy: OCRStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
        interval: int = 3,
    ):
        processed_frames: List[ProcessedFrame] = []
        old_frame = None

        total_steps = VideoProcessor.get_total_frames(video_path, interval)

        parent_dir = Path(video_path).parent
        for frame in tqdm(
            VideoProcessor.get_frames(video_path, interval),
            desc="Processing Frames",
            total=total_steps,
        ):
            # ---- save the frame at parent of video path
            frame_path  = parent_dir / f"frame_{frame.frame_number}.jpg"
            Image.fromarray(frame.frame[:, :, ::-1]).save(frame_path)
            if not ocr_approval_strategy.permit_ocr(frame.frame, old_frame):
                # result should be same as previous frame
                processed_frame = ProcessedFrame()
                processed_frame.frame_number = frame.frame_number

                if processed_frames:
                    processed_frame.char_count = processed_frames[-1].char_count + 1
                else:
                    processed_frame.char_count = 0
                processed_frames.append(processed_frame)
                continue
            old_frame = frame.frame.copy()

            processed_frame = ProcessedFrame()
            processed_frame.frame_number = frame.frame_number
            processed_frame.char_count = ocr_strategy.get_char_count(frame.frame)
            processed_frames.append(processed_frame)
        return processed_frames

    @staticmethod
    def from_video_parallel(
        video_path,
        ocr_strategy: OCRStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
        interval: int = 3,
        # batch_size: int = 100,
        batch_size: int = 1, # can't see any perf boost. maybe take a diff route
    ):
        if batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")

        model = getattr(ocr_strategy, "model", None)
        if model is None or not hasattr(model, "predict"):
            raise ValueError(
                "from_video_parallel requires a PaddleOCR strategy with TextRecognition"
            )

        processed_frames: List[ProcessedFrame] = []
        old_frame = None
        pending_frames = []
        pending_indices = []
        use_paths_only = None

        total_steps = VideoProcessor.get_total_frames(video_path, interval)

        def predict_with_paths(frames_batch):
            with tempfile.TemporaryDirectory() as tmp_dir:
                paths = []
                for index, frame in enumerate(frames_batch):
                    frame_path = os.path.join(tmp_dir, f"frame_{index}.png")
                    Image.fromarray(frame[:, :, ::-1]).save(frame_path)
                    paths.append(frame_path)
                return model.predict(input=paths)

        def predict_batch(frames_batch):
            nonlocal use_paths_only
            if use_paths_only is True:
                return predict_with_paths(frames_batch)
            try:
                output = model.predict(input=frames_batch)
                use_paths_only = False
                return output
            except TypeError:
                use_paths_only = True
                return predict_with_paths(frames_batch)

        def extract_text_from_results(results):
            texts = []
            for res in results:
                if hasattr(res, "res") and isinstance(res.res, dict):
                    rec_text = res.res.get("rec_text", "")
                    if rec_text:
                        texts.append(rec_text)
            return " ".join(texts)

        def get_char_counts(frames_batch):
            output = predict_batch(frames_batch)
            if not isinstance(output, list):
                output = []

            if output and hasattr(output[0], "res"):
                texts = [extract_text_from_results(output)]
            else:
                texts = []
                for item in output:
                    if isinstance(item, list):
                        texts.append(extract_text_from_results(item))
                    elif hasattr(item, "res"):
                        texts.append(extract_text_from_results([item]))
                    else:
                        texts.append("")

            if len(texts) < len(frames_batch):
                texts.extend([""] * (len(frames_batch) - len(texts)))
            elif len(texts) > len(frames_batch):
                texts = texts[: len(frames_batch)]

            return [len(Helper.clean_text(text)) for text in texts]

        def flush_pending():
            if not pending_frames:
                return
            # Batch OCR uses GPU parallelism under the hood.
            char_counts = get_char_counts(pending_frames)
            for index, char_count in zip(pending_indices, char_counts):
                processed_frames[index].char_count = char_count
            pending_frames.clear()
            pending_indices.clear()

        for frame in tqdm(
            VideoProcessor.get_frames(video_path, interval),
            desc="Processing Frames",
            total=total_steps,
        ):
            if not ocr_approval_strategy.permit_ocr(frame.frame, old_frame):
                if pending_frames:
                    flush_pending()

                processed_frame = ProcessedFrame()
                processed_frame.frame_number = frame.frame_number
                if processed_frames:
                    processed_frame.char_count = processed_frames[-1].char_count + 1
                else:
                    processed_frame.char_count = 0
                processed_frames.append(processed_frame)
                continue

            old_frame = frame.frame.copy()

            processed_frame = ProcessedFrame()
            processed_frame.frame_number = frame.frame_number
            processed_frames.append(processed_frame)
            pending_frames.append(frame.frame)
            pending_indices.append(len(processed_frames) - 1)

            if len(pending_frames) >= batch_size:
                flush_pending()

        flush_pending()
        return processed_frames

    @staticmethod
    def get_data_for_plotting(processed_frames: List["ProcessedFrame"]):
        x_data = [frame.frame_number for frame in processed_frames]
        y_data = [frame.char_count for frame in processed_frames]
        return x_data, y_data
