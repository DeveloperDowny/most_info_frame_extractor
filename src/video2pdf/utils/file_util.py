class FileUtil:
    @staticmethod
    def get_inputs(file_path):
        inputs = []
        with open(file_path, "r") as file:
            inputs = file.readlines()
        return inputs
