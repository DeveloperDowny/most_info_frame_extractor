from storage.storage_strategy import StorageStrategy

class DummyStorageStrategy(StorageStrategy):
    def __init__(self):
        pass

    def upload_file(self, file_path: str, file_name: str) -> str:
        print(f"Uploading file {file_name} to dummy storage.")
        return f"https://dummy_storage.com/{file_name}"