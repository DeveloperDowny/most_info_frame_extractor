from storage.storage_strategy import StorageStrategy

from google.cloud import storage


class GCPStorageStrategy(StorageStrategy):
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket_name = bucket_name

    def upload_file(self, file_path: str, file_name: str) -> str:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_name} uploaded to {self.bucket_name}.")

        uploaded_url = f"https://storage.googleapis.com/{self.bucket_name}/{file_name}"

        return uploaded_url