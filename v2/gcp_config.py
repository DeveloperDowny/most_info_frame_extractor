import os

class GCPConfig:
    PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    TOPIC_ID = os.getenv("GCP_TOPIC_ID") 
    PDF_CREATION_TOPIC_ID = os.getenv("PDF_CREATION_TOPIC_ID")