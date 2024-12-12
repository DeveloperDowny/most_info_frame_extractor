from storage.storage_strategy import StorageStrategy
from storage.gcp_storage_strategy import GCPStorageStrategy


class StorageStrategyFactory:
    @staticmethod
    def create_storage_strategy(storage_type: str, bucket_name: str) -> StorageStrategy:
        if storage_type == "gcp":
            return GCPStorageStrategy(bucket_name)
        else:
            raise ValueError(f"Invalid storage type: {storage_type}")
