import os

enable_utc = False
timezone = "Asia/Shanghai"

# Broker and Backend
broker_url = os.getenv("CELERY_BROKER_URL")
result_backend = os.getenv("CELERY_RESULT_BACKEND")
