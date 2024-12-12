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


app = Flask(__name__)

# [END cloudrun_pubsub_server]


def main(video_url):
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
    bucket_name = "extracted-pdfs"
    storage_strategy = StorageStrategyFactory.create_storage_strategy(
        storage_type, bucket_name
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


# [START cloudrun_pubsub_handler]
@app.route("/", methods=["POST"])
def index():
    """Receive and parse Pub/Sub messages."""
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

    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print(f"New v2 Hello {name}!")

    main(name)

    return ("", 204)


@app.route("/data")
def data():
    url = request.args.get("url")
    main(url)
    return ("", 204)


# [END cloudrun_pubsub_handler]
