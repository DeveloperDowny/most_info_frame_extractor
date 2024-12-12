from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import os

app = Flask(__name__)

# Set Pub/Sub topic and project
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "my-topic")
PROJECT_ID = os.getenv("PROJECT_ID", "my-project-id")

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)


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
