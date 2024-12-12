# [START cloudrun_pubsub_server]
import base64

from flask import Flask, request

from telegram import Bot

app = Flask(__name__)

# [END cloudrun_pubsub_server]


# {'update_id': 666162195, 'message': {'message_id': 13, 'from': {'id': 1419710088, 'is_bot': False, 'first_name': 'Vedant', 'username': 'TheDowny', 'language_code': 'en'}, 'chat': {'id': 1419710088, 'first_name': 'Vedant', 'username': 'TheDowny', 'type': 'private'}, 'date': 1734034112, 'text': '<pdf_url>'}}
def handle_pdf_url(pdf_url):
    print(f"Received video url: {pdf_url}")
    return "Received video url"


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message["text"]
    if text.startswith("https"):
        return handle_pdf_url(text)
    print(f"Received message: {text}")
    return "Received message"


@app.route("/webhook", methods=["POST"])
def data():
    data = request.get_json()
    handle_message(data["message"])
    print(data)
    return ("", 204)


# {"chat_id":"<chat_id>","text":"<text>", "pdf_url":"<pdf_url>"}
@app.route("/deliver", methods=["POST"])
def delivery():
    data = request.get_json()
    chat_id = data["chat_id"]
    text = data["text"]
    pdf_url = data["pdf_url"]
    bot = Bot(token="7770881506:AAGKMR-kF-uw2yVqz8cZurdxT3-Tj52caeg")
    bot.send_message(chat_id=chat_id, text=text)
    bot.send_video(chat_id=chat_id, video=pdf_url)
    return ("", 204)


# [END cloudrun_pubsub_handler]
