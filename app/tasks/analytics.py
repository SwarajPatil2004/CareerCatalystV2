import logging
import time
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.analytics.compute_daily_leaderboards")
def compute_daily_leaderboards():
    logger.info("Computing daily student leaderboards...")
    time.sleep(5)
    logger.info("Daily leaderboards computed successfully.")
    return True

@celery_app.task(name="app.tasks.analytics.generate_tpo_analytics_report")
def generate_tpo_analytics_report(institution_id: int):
    logger.info(f"Generating analytics report for institution {institution_id}")
    time.sleep(10)
    logger.info(f"Analytics report generated for institution {institution_id}")
    return True
