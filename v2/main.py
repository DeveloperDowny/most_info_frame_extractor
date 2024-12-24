# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_pubsub_server]
import base64

from flask import Flask, request


from input_strategy_factory import InputStrategyFactory
from ocr_strategy_factory import OCRStrategyFactory
from extraction_strategy_factory import ExtractionStrategyFactory
from input_strategy import InputStrategy
from ocr_approval.ocr_approval_strategy_factory import OCRApprovalStrategyFactory

from input_data.input_data import InputData
from storage.storage_strategy_factory import StorageStrategyFactory

import json

from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

from helper import Helper

from gcp_config import GCPConfig


app = Flask(__name__)

# [END cloudrun_pubsub_server]


def handle_video_url(video_url):
    ocr_approval_type = "pixel_comparison"

    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(
        ocr_approval_type
    )

    ocr_type = "tesseract"
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(ocr_type)

    extraction_type = "k_transactions"
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        extraction_type
    )

    input_type = "youtube"
    input_data = InputData()
    input_data.video_url = video_url

    storage_type = "gcp"
    storage_strategy = StorageStrategyFactory.create_storage_strategy(
        storage_type, GCPConfig.BUCKET_NAME
    )

    input_strategy: InputStrategy = InputStrategyFactory.create_input_strategy(
        input_type,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        input_data,
        storage_strategy,
    )

    input_strategy.proceed()


def find_input_type(name):
    if "playlist" in name:
        return "playlist"
    else:
        return "youtube"


def handle_playlist(playlist_url):
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""

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

    video_urls = Helper.get_video_urls_from_playlist(playlist_url)
    for video_url in video_urls:
        data = video_url
        # When you publish a message, the client returns a future.
        publish_future = publisher.publish(topic_path, data.encode("utf-8"))
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with error handler to {topic_path}.")


# [START cloudrun_pubsub_handler]
@app.route("/", methods=["POST"])
def index():
    """Receive and parse Pub/Sub messages."""
    try:
        envelope = request.get_json()
        if not envelope:
            msg = "no Pub/Sub message received"
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        if not isinstance(envelope, dict) or "message" not in envelope:
            msg = "invalid Pub/Sub message format"
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        pubsub_message = envelope["message"]

        data = "World"
        chat_id = None
        video_url = None
        if isinstance(pubsub_message, dict) and "data" in pubsub_message:
            data = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
            Helper.log(f"Received Data: {data}")
            json_data = json.loads(data)
            video_url = json_data["video_url"]
            chat_id = json_data["chat_id"]

        input_type = find_input_type(video_url)

        if input_type == "playlist":
            Helper.log(f"Handling playlist: {video_url}")
            handle_playlist(video_url)
            return ("", 204)

        Helper.log(f"Handling video: {video_url}")
        handle_video_url(video_url)
    except Exception as e:
        print(f"error: {e}")
    finally:
        return ("", 204)


# [END cloudrun_pubsub_handler]
