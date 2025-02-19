# SQLite DB Service

## Alembic Migrations
```shell
TIDEPOOL_SETTINGS_MODULE=scratch.mollusk_settings alembic \
-c tidepool/services/db/postgres/alembic.ini \
<command>
```