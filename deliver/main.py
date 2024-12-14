import asyncio
import logging
import os
from typing import Optional

import pyrogram
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
    API_ID = os.getenv("TELEGRAM_API_ID")
    API_HASH = os.getenv("TELEGRAM_API_HASH")
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Request model for PDF delivery
class PDFDeliveryRequest(BaseModel):
    pdf_url: HttpUrl
    chat_id: str
    caption: Optional[str] = None


async def send_pdf_to_telegram(
    client: Client, chat_id: str, pdf_url: str, caption: Optional[str] = None
) -> bool:
    """
    Send PDF to Telegram user directly from GCS URL.

    Args:
        client (Client): Pyrogram Telegram client
        chat_id (str): Telegram chat ID
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


@app.post("/deliver-pdf/")
async def deliver_pdf(request: PDFDeliveryRequest):
    """
    Endpoint to deliver PDF to a Telegram user.

    Args:
        request (PDFDeliveryRequest): Request containing PDF URL and Telegram chat ID

    Returns:
        Dict: Delivery status
    """
    # Validate Telegram credentials
    if not all(
        [TelegramConfig.API_ID, TelegramConfig.API_HASH, TelegramConfig.BOT_TOKEN]
    ):
        raise HTTPException(
            status_code=500, detail="Telegram credentials not configured"
        )

    # Initialize Telegram client
    async with Client(
        "pdf_bot",
        api_id=TelegramConfig.API_ID,
        api_hash=TelegramConfig.API_HASH,
        bot_token=TelegramConfig.BOT_TOKEN,
    ) as client:
        # Send PDF directly from URL
        success = await send_pdf_to_telegram(
            client, int(request.chat_id), str(request.pdf_url), request.caption
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to send PDF to Telegram"
            )

        return {"status": "success", "message": "PDF delivered to Telegram"}


async def main():
    """Main entry point for the application."""
    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=8080)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
