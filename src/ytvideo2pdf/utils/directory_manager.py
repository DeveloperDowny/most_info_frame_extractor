import os
import shutil


class DirectoryManager:
    @staticmethod
    def create_directory(directory_name: str):
        if os.path.exists(directory_name):
            return
        os.mkdir(directory_name)

    @staticmethod
    def delete_directory(dir_path: str):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def get_file_name(directory: str) -> str:
        return os.listdir(directory)[0]

    @staticmethod
    def get_video_path(directory: str) -> str:
        return os.path.join(directory, DirectoryManager.get_file_name(directory))
