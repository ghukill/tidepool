"""tidepool/settings.py"""

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
    "A Tidepool Repository",
)


# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------
DATABASE = {
    "HOST": os.environ.get("TIDEPOOL_DB_HOST", "localhost"),
    "PORT": os.environ.get("TIDEPOOL_DB_PORT", "5432"),
    "NAME": os.environ.get("TIDEPOOL_DB_NAME", "tidepool"),
    "USERNAME": os.environ.get("TIDEPOOL_DB_USERNAME", "postgres"),
    "PASSWORD": os.environ.get("TIDEPOOL_DB_PASSWORD", "password"),
    "DATA_DIR": os.environ.get("TIDEPOOL_DB_DATA_DIR", "$HOME/.tidepool/postgres/data"),
}
DATABASE_CONNECTION_URI = os.environ.get(
    "TIDEPOOL_DB_CONNECTION_STRING",
    "postgresql://%s:%s@%s:%s/%s"
    % (
        DATABASE["USERNAME"],
        DATABASE["PASSWORD"],
        DATABASE["HOST"],
        DATABASE["PORT"],
        DATABASE["NAME"],
    ),
)


# -------------------------------------------------------------------
# File Storage
# -------------------------------------------------------------------
PRIMARY_STORAGE_SERVICE = {
    "module": "tidepool.services.storage",
    "class": "POSIXStorageService",
    "config": {
        "NAME": "primary local filesystem storage",
        "DATA_DIR": os.environ.get(
            "TIDEPOOL_POSIX_DATA_DIR", "$HOME/.tidepool/posix/data"
        ),
    },
}

REPLICATION_STORAGE_SERVICES = [
    {
        "module": "tidepool.services.storage",
        "class": "S3StorageService",
        "config": {
            "NAME": "local dockerized minio instance",
            "REGION": os.environ.get("TIDEPOOL_MINIO_REGION", "us-east-1"),
            "ENDPOINT": os.environ.get(
                "TIDEPOOL_MINIO_ENDPOINT", "http://localhost:9000"
            ),
            "ACCESS_KEY_ID": os.environ.get("TIDEPOOL_MINIO_ACCESS_KEY_ID", "tidepool"),
            "SECRET_ACCESS_KEY": os.environ.get(
                "TIDEPOOL_MINIO_SECRET_ACCESS_KEY", "password"
            ),
            "BUCKET": os.environ.get("TIDEPOOL_MINIO_BUCKET", "tidepool"),
            "DATA_DIR": os.environ.get(
                "TIDEPOOL_MINIO_DATA_DIR", "$HOME/.tidepool/minio/data"
            ),
        },
    },
    # {
    #     "module": "tidepool.services.storage",
    #     "class": "S3StorageService",
    #     "config": {
    #         "NAME": "personal AWS S3 bucket",
    #         "REGION": os.environ.get("TIDEPOOL_S3_REGION", "us-east-1"),
    #         "ACCESS_KEY_ID": os.environ.get("TIDEPOOL_S3_ACCESS_KEY_ID", "abc123..."),
    #         "SECRET_ACCESS_KEY": os.environ.get(
    #             "TIDEPOOL_S3_SECRET_ACCESS_KEY", "def456..."
    #         ),
    #         "BUCKET": os.environ.get("TIDEPOOL_S3_BUCKET", "tidepool"),
    #     },
    # },
    # {
    #     "module": "tidepool.services.storage",
    #     "class": "POSIXStorageService",
    #     "config": {
    #         "NAME": "secondary filesystem on home network",
    #         "DATA_DIR": os.environ.get(
    #             "TIDEPOOL_POSIX_DATA_DIR-2", "/another/computer/somewhere"
    #         ),
    #     },
    # },
]


# -------------------------------------------------------------------
# Full-Text Search
# -------------------------------------------------------------------
# TODO...


# -------------------------------------------------------------------
# API
# -------------------------------------------------------------------
API_HOST = "localhost"
API_PORT = 5000
API_DEBUG = True
API_BASE_URI = f"http://{API_HOST}:{API_PORT}/api"


# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------
UI_HOST = "localhost"
UI_PORT = 5001
UI_DEBUG = True
UI_BASE_URI = f"http://{API_HOST}:{API_PORT}/ui"
