"""
Logging configuration and utilities
"""
import logging
import os
from pathlib import Path
from datetime import datetime

# Create logs directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file with date
log_filename = f"app_{datetime.now().strftime('%Y%m%d')}.log"
log_filepath = LOG_DIR / log_filename

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        # File handler - logs to file
        logging.FileHandler(log_filepath, encoding='utf-8'),
        # Stream handler - logs to console
        logging.StreamHandler()
    ]
)

# Create logger instance
logger = logging.getLogger(__name__)


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (usually __name__ of the module)
    
    Returns:
        Logger instance
    
    Example:
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("This is an info message")
    """
    return logging.getLogger(name)


# Logger methods for convenience
def log_info(message: str, **kwargs):
    """Log info message"""
    logger.info(message, extra=kwargs)


def log_error(message: str, **kwargs):
    """Log error message"""
    logger.error(message, extra=kwargs)


def log_warning(message: str, **kwargs):
    """Log warning message"""
    logger.warning(message, extra=kwargs)


def log_debug(message: str, **kwargs):
    """Log debug message"""
    logger.debug(message, extra=kwargs)


def log_exception(message: str, exc_info: bool = True):
    """
    Log exception with traceback
    
    Args:
        message: Error message
        exc_info: Include exception info (default: True)
    """
    logger.exception(message, exc_info=exc_info)


# Export logger
__all__ = ['logger', 'get_logger', 'log_info', 'log_error', 'log_warning', 'log_debug', 'log_exception']
