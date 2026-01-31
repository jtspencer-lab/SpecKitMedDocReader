"""
Celery task configuration.

Defines Celery settings and configuration for different environments.
"""

from kombu import Exchange, Queue
from src.config import get_settings


settings = get_settings()

# Message queues
default_exchange = Exchange("default", type="direct")

CELERY_QUEUES = (
    Queue("default", exchange=default_exchange, routing_key="default"),
    Queue("extraction", exchange=default_exchange, routing_key="extraction"),
    Queue("batch", exchange=default_exchange, routing_key="batch"),
    Queue("reports", exchange=default_exchange, routing_key="reports"),
)

# Broker settings
CELERY_BROKER_URL = settings.celery_broker_url
CELERY_RESULT_BACKEND = settings.celery_result_backend

# Timeouts
CELERY_TASK_TIME_LIMIT = settings.celery_task_time_limit
CELERY_TASK_SOFT_TIME_LIMIT = settings.celery_task_soft_time_limit

# Serialization
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

# Timezone
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True

# Result backend
CELERY_RESULT_EXPIRES = 3600  # 1 hour

# Retries
CELERY_TASK_DEFAULT_RETRY_DELAY = 60
CELERY_TASK_DEFAULT_MAX_RETRIES = 3
