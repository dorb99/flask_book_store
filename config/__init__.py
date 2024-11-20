from .db import init_db
import logging
import os
from dotenv import load_dotenv


def setup_logger(log_level=logging.INFO):
    """
    Setup basic logging configuration.
    """
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s - %(message)s - %(asctime)s",
        datefmt="%H:%M:%S"
)

def load_config():
    """
    Load configuration from environment variables.
    """
    load_dotenv() # Load .env file into environment variables
    if not os.getenv("SECRET_KEY"):
        logging.warning("SECRET_KEY isn't found in the environment, using the default")

    if not os.getenv("CLIENT_URL"):
        logging.warning("CLIENT_URL isn't found in the environment, using the default")
    return {
        "SECRET_KEY": os.getenv("SECRET_KEY", "default_secret"),
        "DEBUG": os.getenv("DEBUG", "false").lower() == "true",
        "CLIENT_URL": os.getenv("CLIENT_URL", "*"),
        "PORT": int(os.getenv("PORT", 5000)),
        "HOST": os.getenv("HOST", "0.0.0.0"),
    }
