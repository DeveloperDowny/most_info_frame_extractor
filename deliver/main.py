import asyncio
import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from pyrogram import Client
from pyrogram.errors import RPCError

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Application configuration
app = FastAPI()


# Telegram client configuration
class TelegramConfig:
    API_ID = int(os.getenv("TELEGRAM_API_ID"))
    API_HASH = os.getenv("TELEGRAM_API_HASH")
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Request model for PDF delivery
class PDFDeliveryRequest(BaseModel):
    pdf_url: HttpUrl
    chat_id: int
    caption: Optional[str] = None


async def send_pdf_to_telegram(
    client: Client, chat_id: int, pdf_url: str, caption: Optional[str] = None
) -> bool:
    """
    Send PDF to Telegram user directly from GCS URL.

    Args:
        client (Client): Pyrogram Telegram client
        chat_id (int): Telegram chat ID
        pdf_url (str): URL of the PDF (supports GCS URLs)
        caption (Optional[str]): Optional caption for the document

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        await client.send_document(
            chat_id=chat_id, document=str(pdf_url), caption=caption or "PDF Document"
        )
        logger.info(f"PDF sent to {chat_id} from URL: {pdf_url}")
        return True

    except RPCError as e:
        logger.error(f"Telegram RPC Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending PDF to Telegram: {e}")
        return False


from fastapi import Request
import base64
import json


# [START cloudrun_pdf_delivery]
@app.post("/deliver-pdf/")
async def index(request: Request):
    """Receive and parse Pub/Sub messages."""
    envelope = await request.json()
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
    pdf_url = None
    caption = None
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        json_data = json.loads(data)
        chat_id = json_data.get("chat_id")
        pdf_url = json_data.get("pdf_url")
        caption = json_data.get("caption")

    if not all([chat_id, pdf_url, caption]):
        msg = "invalid Pub/Sub message: missing chat_id or pdf_url"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    async with Client(
        "pdf_bot",
        api_id=TelegramConfig.API_ID,
        api_hash=TelegramConfig.API_HASH,
        bot_token=TelegramConfig.BOT_TOKEN,
    ) as client:
        # Send PDF directly from URL
        success = await send_pdf_to_telegram(client, chat_id, str(pdf_url), caption)

        if not success:
            print("Failed to send PDF to Telegram")
            return ("", 204)

        return ("", 204)

    return ("", 204)


# [END cloudrun_pdf_delivery]


async def main():
    """Main entry point for the application."""
    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=8080)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
