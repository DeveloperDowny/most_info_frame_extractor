from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import os

from input_strategy_factory import InputStrategyFactory
from ocr_strategy_factory import OCRStrategyFactory
from extraction_strategy_factory import ExtractionStrategyFactory
from input_strategy import InputStrategy
from ocr_approval.ocr_approval_strategy_factory import OCRApprovalStrategyFactory

from input_data.input_data import InputData

app = Flask(__name__)

# Set Pub/Sub topic and project
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "my-topic")
PROJECT_ID = os.getenv("PROJECT_ID", "my-project-id")

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)


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
    input_strategy: InputStrategy = InputStrategyFactory.create_input_strategy(
        input_type, ocr_strategy, extraction_strategy, ocr_approval_strategy, input_data
    )

    input_strategy.proceed()


@app.route("/")
def index():
    return "Cloud Run Pub/Sub Demo Service", 200


@app.route("/publish", methods=["POST"])
def publish_message():
    try:
        data = request.json.get("message", "")
        if not data:
            return jsonify({"error": "Message is required"}), 400

        # Data must be a byte string for Pub/Sub
        data_bytes = data.encode("utf-8")

        # Publish message to the topic
        future = publisher.publish(topic_path, data_bytes)
        message_id = future.result()

        return jsonify({"message_id": message_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
