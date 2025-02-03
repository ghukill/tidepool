export PYTHONPATH = .

test:
	pytest -vv

services-start:
	docker compose --env-file .env up

services-start-daemon:
	docker compose --env-file .env up -d

services-stop:
	docker compose --env-file .env down

services-tail-logs:
	docker compose --env-file .env logs -f