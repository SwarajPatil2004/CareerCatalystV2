import logging
import sys
from app.core.config import settings

def setup_logging():
    logging_level = logging.INFO if settings.ENVIRONMENT == "prod" else logging.DEBUG
    
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Suppress some noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
