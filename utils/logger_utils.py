import os
import logging

def init_logger(log_path):
    try:
        # Ensure directory exists
        log_dir = os.path.dirname(log_path)
        os.makedirs(log_dir, exist_ok=True)

        # Try writing log normally
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            filemode="a"
        )
        return logging.getLogger("Transcriber")

    except PermissionError:
        # Fallback location (100% writable)
        fallback_dir = os.path.join(os.getenv("APPDATA"), "tantum_logs")
        os.makedirs(fallback_dir, exist_ok=True)
        fallback_path = os.path.join(fallback_dir, "run.log")

        logging.basicConfig(
            filename=fallback_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            filemode="a"
        )
        logger = logging.getLogger("Transcriber")
        logger.warning("Permission denied for default log path. Using fallback log directory.")
        return logger
