from src.video2pdf.utils.directory_manager import DirectoryManager
from src.video2pdf.utils.video_processor import VideoProcessor

if __name__ == "__main__":
    directory = "data_archive_1/aecnku"
    video_path = DirectoryManager.get_video_path(directory)
    frame_number = 3870
    timestamp = VideoProcessor.get_timestamp_from_frame_number(video_path, frame_number)
    print(timestamp)

    formatted_time = VideoProcessor.get_formatted_time(timestamp)
    print(formatted_time)
