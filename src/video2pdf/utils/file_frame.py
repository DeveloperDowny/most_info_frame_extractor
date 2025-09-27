class FileFrame:
    def __init__(self, frame_path: str):
        self.frame_id = int(frame_path.split('_')[-1].split('.')[0])
        self.frame_path = frame_path

    @staticmethod
    def get_sorted_frames(list_of_files):
        frames = [FileFrame(file) for file in list_of_files]
        frames.sort(key=lambda x: x.frame_id)
        return frames
