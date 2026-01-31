"""
Entry point for running Celery worker.

Usage:
    celery -A src.tasks.celery_app worker --loglevel=info
"""

from src.tasks.celery_app import celery_app


if __name__ == "__main__":
    celery_app.start()
