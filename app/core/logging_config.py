import logging
import sys
from app.core.config import settings

try:
    from pythonjsonlogger import jsonlogger
except ImportError:
    jsonlogger = None

def setup_logging():
    logging_level = logging.INFO if settings.ENVIRONMENT == "prod" else logging.DEBUG
    
    handler = logging.StreamHandler(sys.stdout)
    
    if settings.ENVIRONMENT == "prod" and jsonlogger:
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        handler.setFormatter(formatter)
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

    logging.root.setLevel(logging_level)
    logging.root.addHandler(handler)

    # Suppress some noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
