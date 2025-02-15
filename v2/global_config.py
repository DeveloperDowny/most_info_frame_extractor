import os

class GlobalConfig:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"