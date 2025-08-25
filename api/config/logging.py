import logging

from config.settings import get_settings

app_settings = get_settings()
_is_logging_configured = False

def _configure_logging():
    global _is_logging_configured
    log_config = {
        "level": app_settings.log_level,
        "filepath": app_settings.log_path,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
    if not _is_logging_configured:
        logging.basicConfig(
            filename=log_config["filepath"],
            level=log_config["level"],
            format=log_config["format"],
            datefmt=log_config["datefmt"],
        )
        _is_logging_configured = True

def get_logger(name: str) -> logging.Logger:
    _configure_logging()
    logger = logging.getLogger(name)
    return logger
