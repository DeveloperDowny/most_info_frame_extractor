from delivery.delivery_strategy import DeliveryStrategy

from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

import json

from gcp_config import GCPConfig


class TelegramDeliveryStrategy(DeliveryStrategy):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def deliver(self, pdf_url: str, caption: str) -> None:
        """Publishes multiple messages to a Pub/Sub topic with an error handler."""

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(GCPConfig.PROJECT_ID, GCPConfig.PDF_CREATION_TOPIC_ID)
        publish_futures = []

        def get_callback(
            publish_future: pubsub_v1.publisher.futures.Future, data: str
        ) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
            def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
                try:
                    # Wait 60 seconds for the publish call to succeed.
                    print(publish_future.result(timeout=60))
                except futures.TimeoutError:
                    print(f"Publishing {data} timed out.")

            return callback

        json_data = {"pdf_url": pdf_url, "chat_id": self.chat_id, "caption": caption}
        data = json.dumps(json_data)
        # When you publish a message, the client returns a future.
        publish_future = publisher.publish(topic_path, data.encode("utf-8"))
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)

        # Wait for all the publish futures to resolve before exiting.
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        print(f"Published messages with error handler to {topic_path}.")
