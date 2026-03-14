import logging
import time
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(
    name="app.tasks.email.send_email_verification",
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def send_email_verification(self, user_id: int, email: str):
    try:
        logger.info(f"Sending verification email to {email} (User ID: {user_id})")
        # Placeholder for actual email sending logic
        time.sleep(1) 
        logger.info(f"Verification email sent to {email}")
        return True
    except Exception as exc:
        logger.error(f"Error sending email to {email}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
