# [START cloudrun_pubsub_server]

from flask import Flask, request
from gcp_config import GCPConfig

import json

app = Flask(__name__)

# [END cloudrun_pubsub_server]


# {'update_id': 666162195, 'message': {'message_id': 13, 'from': {'id': 1419710088, 'is_bot': False, 'first_name': 'Vedant', 'username': 'TheDowny', 'language_code': 'en'}, 'chat': {'id': 1419710088, 'first_name': 'Vedant', 'username': 'TheDowny', 'type': 'private'}, 'date': 1734034112, 'text': '<video_url>'}}
def handle_video_url(video_url, chat_id):
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    from concurrent import futures
    from google.cloud import pubsub_v1
    from typing import Callable

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCPConfig.PROJECT_ID, GCPConfig.TOPIC_ID)
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

    # data = video_url.strip() + f" {chat_id}"
    json_data = {
        "video_url": video_url.strip(),
        "chat_id": chat_id,
    }
    data = json.dumps(json_data)
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with error handler to {topic_path}.")


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message["text"]
    if text.startswith("https"):
        return handle_video_url(text, chat_id)
    print(f"Received message: {text}")
    return "Received message"


@app.route("/webhook", methods=["POST"])
def data():
    data = request.get_json()
    handle_message(data["message"])
    print(data)
    return ("", 204)


# [END cloudrun_pubsub_handler]
