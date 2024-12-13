# Project structure:
# /
# ├── main.py
# ├── requirements.txt
# └── Dockerfile

# main.py
import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config

app = FastAPI()

@app.get("/")
async def root():
    """Basic health check endpoint."""
    return {"message": "AsyncIO server is running!"}

@app.get("/hello/{name}")
async def hello(name: str):
    """Dummy endpoint demonstrating async functionality."""
    await asyncio.sleep(0.1)  # Simulate some async work
    return {"message": f"Hello, {name}!"}

async def custom_background_task():
    """Example of a background task."""
    while True:
        logging.info("Background task running...")
        await asyncio.sleep(60)  # Run every minute

async def main():
    """Main entry point for the application."""
    # Configure logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Start background task
    background_task = asyncio.create_task(custom_background_task())
    
    # Hypercorn configuration
    config = Config()
    config.bind = ["0.0.0.0:8080"]  # Cloud Run requires binding to 0.0.0.0
    
    # Serve the application
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())