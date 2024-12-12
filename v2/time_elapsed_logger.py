import logging
from datetime import datetime

class TimeElapsedLogger(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.last_log_time = None

    def format(self, record):
        current_time = datetime.now()
        if self.last_log_time:
            elapsed = (current_time - self.last_log_time).total_seconds() * 1000  # in milliseconds
            elapsed_str = f"+{elapsed:.0f}ms"
        else:
            elapsed_str = "+0ms"

        self.last_log_time = current_time

        # Add elapsed time to the log message
        record.elapsed = elapsed_str
        return super().format(record)

# Setup logger
logger = logging.getLogger("customLogger")
logger.setLevel(logging.DEBUG)

# Create a handler
handler = logging.StreamHandler()

# Define log format
log_format = (
    "%(asctime)s [%(levelname)s] %(message)s %(elapsed)s"
)  # Elapsed time placeholder

formatter = TimeElapsedLogger(fmt=log_format, datefmt="%m/%d/%Y, %I:%M:%S %p")
handler.setFormatter(formatter)

logger.addHandler(handler)

# Example usage
if __name__ == "__main__":
    logger.info("Starting application...")
    logger.debug("Initializing modules...")
    logger.warning("Low disk space warning!")
    logger.error("An error occurred")
