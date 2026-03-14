import os
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "careercatalyst",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email",
        "app.tasks.ai",
        "app.tasks.analytics",
        "app.tasks.reporting"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_queues={
        "high": {"exchange": "high", "routing_key": "high"},
        "medium": {"exchange": "medium", "routing_key": "medium"},
        "low": {"exchange": "low", "routing_key": "low"},
    },
    task_default_queue="medium",
    task_routes={
        "app.tasks.email.*": {"queue": "high"},
        "app.tasks.ai.*": {"queue": "medium"},
        "app.tasks.analytics.*": {"queue": "low"},
        "app.tasks.reporting.*": {"queue": "low"},
    },
    beat_schedule={
        "weekly-tpo-report": {
            "task": "app.tasks.reporting.generate_weekly_tpo_report",
            "schedule": 604800.0, # Every 7 days
            "args": (1,) # Generic ID placeholder
        },
    }
)
