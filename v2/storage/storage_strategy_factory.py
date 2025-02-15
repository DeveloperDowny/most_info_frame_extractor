from storage.storage_strategy import StorageStrategy
from storage.gcp_storage_strategy import GCPStorageStrategy
from storage.dummy_storage_strategy import DummyStorageStrategy


class StorageStrategyFactory:
    @staticmethod
    def create_storage_strategy(storage_type: str, bucket_name: str) -> StorageStrategy:
        if storage_type == "gcp":
            return GCPStorageStrategy(bucket_name)
        elif storage_type == "dummy":
            return DummyStorageStrategy()
        else:
            raise ValueError(f"Invalid storage type: {storage_type}")
