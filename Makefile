ifneq (,$(wildcard ./.env))
    include .env
    export
endif
export PYTHONPATH = .

test:
	uv run coverage run --source=tidepool -m pytest -vv
	uv run coverage report -m

lint:
	uv run ruff check .

lint-apply:
	uv run ruff check --fix .

services-start:
	docker compose --env-file .env up

services-start-daemon:
	docker compose --env-file .env up -d

services-stop:
	docker compose --env-file .env down

services-tail-logs:
	docker compose --env-file .env logs -f

start-api:
	uv run flask -A tidepool.api.app:api_app --debug run --host 0.0.0.0 -p 5000

start-ui:
	uv run flask -A tidepool.ui.app:ui_app --debug run --host 0.0.0.0 -p 5001