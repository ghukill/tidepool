"""tests/fixtures/settings.py"""

import logging
import os

# -------------------------------------------------------------------
# Logging
# NOTE: currently, logging is quite basic for development purposes
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# -------------------------------------------------------------------
# Repository
# -------------------------------------------------------------------
REPOSITORY_NAME = os.environ.get(
    "TIDEPOOL_REPOSITORY_NAME",
    "Tidepool Repository - Testing",
)


# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------
DATABASE = {
    "SERVICE_DIR": "tidepool/services/db/sqlite",
    "NAME": os.environ.get("TIDEPOOL_SQLITE_DB_NAME", "tidepool.sqlite"),
    "DATA_DIR": os.environ.get("TIDEPOOL_SQLITE_DB_DATA_DIR", "/tmp/tidepool/db/sqlite"),
}
os.makedirs(DATABASE["DATA_DIR"], exist_ok=True)
print(DATABASE)
DATABASE_CONNECTION_URI = os.environ.get(
    "TIDEPOOL_SQLITE_DB_CONNECTION_STRING",
    f"sqlite:///{os.path.join(DATABASE['DATA_DIR'], DATABASE['NAME'])}",
)


# -------------------------------------------------------------------
# File Storage
# -------------------------------------------------------------------
PRIMARY_STORAGE_SERVICE = {
    "module": "tidepool.services.storage",
    "class": "POSIXStorageService",
    "config": {
        "NAME": "primary local filesystem storage",
        "DATA_DIR": os.environ.get("TIDEPOOL_POSIX_DATA_DIR"),
    },
}

REPLICATION_STORAGE_SERVICES = []


# -------------------------------------------------------------------
# API
# -------------------------------------------------------------------
API_HOST = "localhost"
API_PORT = 5000
API_DEBUG = True
API_BASE_URI = f"http://{API_HOST}:{API_PORT}"
