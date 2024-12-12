import os
from helper import Helper
from ocr_strategy import OCRStrategy
from video_processor import VideoProcessor
from directory_manager import DirectoryManager
from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy

from concurrent.futures import ThreadPoolExecutor



class ProcessedFrame:
    def __init__(self):
        self.frame_number = 0
        self.ocr_text = ""

    @staticmethod
    def from_directory(directory, ocr_strategy: OCRStrategy):
        processed_frames = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                frame = ProcessedFrame()
                frame.frame_number = Helper.get_digits(filename)
                frame.ocr_text = ocr_strategy.extract_clean_text(
                    os.path.join(directory, filename)
                )
                processed_frames.append(frame)

    @staticmethod
    def from_video(video_path, ocr_strategy: OCRStrategy, ocr_approval_strategy: OCRApprovalStrategy):
        processed_frames = []
        old_frame = None
        for frame in VideoProcessor.get_frames(video_path, 3):
            
            if not ocr_approval_strategy.permit_ocr(frame.frame, old_frame):
                # result should be same as previous frame
                processed_frame = ProcessedFrame()
                processed_frame.frame_number = frame.frame_number
                processed_frame.ocr_text = processed_frames[-1].ocr_text
                processed_frames.append(processed_frame)
                continue
            old_frame = frame.frame

            processed_frame = ProcessedFrame()
            processed_frame.frame_number = frame.frame_number
            processed_frame.ocr_text = ocr_strategy.extract_clean_text(frame.frame)
            processed_frames.append(processed_frame)
        return processed_frames

    @staticmethod
    def from_youtube_video(video_url, directory, ocr_strategy: OCRStrategy):

        Helper.download_youtube_video(video_url, directory)
        video_path = DirectoryManager.get_video_path(directory)
        return ProcessedFrame.from_video(video_path, ocr_strategy)

    @staticmethod
    def get_data_for_plotting(processed_frames):
        x_data = [frame.frame_number for frame in processed_frames]
        y_data = [len(frame.ocr_text) for frame in processed_frames]
        return x_data, y_data


# This section will come in input strategy or something maybe
# @staticmethod
# def from_youtube_playlist(
#     playlist_url, ocr_strategy: OCRStrategy, video_processor: VideoProcessor
# ):
#     directory = RandomGenerator.generate_random_word(6)
#     DirectoryManager.create_directory(directory)
#     video_urls = Helper.get_youtube_playlist_urls(playlist_url)
#     for video_url in video_urls:
#         processed_frames = ProcessedFrame.from_youtube_video(
#             video_url, ocr_strategy, video_processor
#         )


    @staticmethod
    def from_video_parallel(video_path, ocr_strategy, ocr_approval_strategy, num_replicas=4):
        all_frames = list(VideoProcessor.get_frames(video_path, interval=3))  # Get all frames
        chunk_size = len(all_frames) // num_replicas
        chunks = [all_frames[i * chunk_size: (i + 1) * chunk_size] for i in range(num_replicas)]

        def process_chunk(chunk):
            processed_frames = []
            old_frame = None
            for frame in chunk:
                if not ocr_approval_strategy.permit_ocr(frame.frame, old_frame):
                    processed_frame = ProcessedFrame()
                    processed_frame.frame_number = frame.frame_number
                    processed_frame.ocr_text = processed_frames[-1].ocr_text if processed_frames else ""
                    processed_frames.append(processed_frame)
                    continue
                old_frame = frame.frame
                processed_frame = ProcessedFrame()
                processed_frame.frame_number = frame.frame_number
                processed_frame.ocr_text = ocr_strategy.extract_clean_text(frame.frame)
                processed_frames.append(processed_frame)
            return processed_frames

        with ThreadPoolExecutor(max_workers=num_replicas) as executor:
            results = list(executor.map(process_chunk, chunks))

        # Flatten list of lists
        return [frame for sublist in results for frame in sublist]
