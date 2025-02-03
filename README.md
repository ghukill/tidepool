# tidepool

## Installation

Clone repository:
```shell
git clone https://github.com/ghukill/tidepool.git
cd tidepool
```

Create python environment:
```shell
uv venv --python 3.13 .venv
```

Install dependencies:
```shell
uv sync
```

Start docker containers:
```shell
docker compose up -d
```

Create database:
```shell
# TODO: create database that matches env var 'TIDEPOOL_PG_DB'
```

Run database migrations:
```shell
# ensure connection
alembic history

# run migrations
alembic upgrade head
```


## Environment Variables

```shell
TIDEPOOL_PG_USER=# username for Postgres; default "postgres"
TIDEPOOL_PG_PASSWORD=# password for Postgres; default "password"
TIDEPOOL_PG_DB=# database name for Postgres; default "setter"
TIDEPOOL_PG_DATA_DIR=# mount location for Postgres data

TIDEPOOL_MINIO_ENDPOINT=# endpoint URL for minio file storage; default "http://localhost:9001"
TIDEPOOL_MINIO_USERNAME=# username for minio file storage; default "minioadmin"
TIDEPOOL_MINIO_PASSWORD=# username for minio file storage; default "minioadmin"
TIDEPOOL_MINIO_DATA_DIR=# mount location for Minio data
TIDEPOOL_MINIO_BUCKET=# bucket name

TIDEPOOL_QW_DATA_DIR=# mount location for Quickwit data
```