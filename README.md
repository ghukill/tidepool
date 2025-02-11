# tidepool

## Installation

Clone repository:
```shell
git clone https://github.com/ghukill/tidepool.git
cd tidepool
```
  * _NOTE_: if cloning as a functional repository, consider renaming on clone

Create python environment:
```shell
uv venv --python 3.13 .venv
```

Install dependencies:
```shell
uv sync
```

Create `settings.py` file from template
```shell
cp tidepool/settings_template.py tidepool/settings.py
```

Start docker containers:
```shell
docker compose up -d
```

Run database migrations:
```shell
# ensure connection
alembic history

# run migrations
alembic upgrade head
```


## Configuration

Configuration is done primarily by modifying the `tidepool.settings` file, where env vars can be used to set values there.