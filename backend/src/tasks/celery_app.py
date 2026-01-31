"""
Celery application initialization.

Celery is used for asynchronous task processing including:
- Document OCR processing
- NLP extraction
- Batch processing
- Report generation
"""

from celery import Celery
from src.config import get_settings


settings = get_settings()

# Create Celery app
celery_app = Celery(
    "signupreader",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_time_limit=settings.celery_task_time_limit,
    task_soft_time_limit=settings.celery_task_soft_time_limit,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=3600,  # Results expire after 1 hour
)

# Task routes for organization
celery_app.conf.task_routes = {
    "src.tasks.extraction.*": {"queue": "extraction"},
    "src.tasks.batch.*": {"queue": "batch"},
    "src.tasks.report.*": {"queue": "reports"},
}
