"""tidepool/settings.py"""

import os

# -------------------------------------------------------------------
# Repository
# -------------------------------------------------------------------
REPOSITORY_NAME = os.environ.get("TIDEPOOL_REPOSITORY_NAME", "Tidepool Repository")


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
POSIX_STORAGE = {
    "DATA_DIR": os.environ.get("TIDEPOOL_S3_DATA_DIR", "$HOME/.tidepool/posix/data"),
}
S3_STORAGE = {
    "REGION": os.environ.get("TIDEPOOL_S3_REGION", "us-east-1"),
    "ENDPOINT": os.environ.get("TIDEPOOL_S3_ENDPOINT", "http://localhost:9000"),
    "ACCESS_KEY_ID": os.environ.get("TIDEPOOL_S3_ACCESS_KEY_ID", "tidepool"),
    "SECRET_ACCESS_KEY": os.environ.get("TIDEPOOL_S3_SECRET_ACCESS_KEY", "password"),
    "BUCKET": os.environ.get("TIDEPOOL_S3_BUCKET", "tidepool"),
    "DATA_DIR": os.environ.get("TIDEPOOL_S3_DATA_DIR", "$HOME/.tidepool/minio/data"),
}
PRIMARY_STORAGE_SERVICE = ("tidepool.services.storage", "POSIXStorageService")
REPLICATION_STORAGE_SERVICES = []

# -------------------------------------------------------------------
# Full-Text Search
# -------------------------------------------------------------------
# TODO...
