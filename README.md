# Async Web API with FastAPI + SQLAlchemy 2.0

This is a sample project of Async Web API with FastAPI + SQLAlchemy 2.0.
It includes asynchronous DB access using asyncpg and test code covering them.

This sample project is explained in this blog (written in Japanese).  
https://www.rhoboro.com/2021/06/12/async-fastapi-sqlalchemy.html

If you want to use prisma instead of sqlalchemy, see [rhoboro/async-fastapi-prisma](https://github.com/rhoboro/async-fastapi-prisma).


# Run with docker compose

After start-up, you can access [localhost:8000/docs](http://localhost:8000/docs) to see the api documentation.

```shell
$ docker compose up -w
```

## Setup a database and create tables

```shell
$ docker compose exec app uv run alembic upgrade head
```

## Test

```shell
$ docker compose exec app uv sync --frozen --group testing
$ docker compose exec app uv run black app
$ docker compose exec app uv run ruff check app
$ docker compose exec app uv run mypy app
$ docker compose exec app uv run pytest app
```

## Cleanup

```shell
$ docker compose down -v
```

# Run without docker compose

This project uses [uv](https://docs.astral.sh/uv/).

## Install dependencies

```shell
$ uv sync --frozen
```

## Setup a database and create tables

```shell
$ docker run -d --name db \
  -e POSTGRES_PASSWORD=password \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:16.3-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

# If your database host is not localhost, edit `DB_URI` in `app/config/local.env`.
$ APP_CONFIG_FILE=local uv run alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

## Run

```shell
$ APP_CONFIG_FILE=local uv run fastapi dev
INFO:     Will watch for changes in these directories: ['/Users/rhoboro/go/src/github.com/rhoboro/async-fastapi-sqlalchemy/app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [49448] using WatchFiles
INFO:     Started server process [49450]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO     Using path app/main.py
INFO     Resolved absolute path /Users/rhoboro/go/src/github.com/rhoboro/async-fastapi-sqlalchemy/app/main.py
INFO     Searching for package file structure from directories with __init__.py files
INFO     Importing from /Users/rhoboro/go/src/github.com/rhoboro/async-fastapi-sqlalchemy

 ╭─ Python package file structure ─╮
 │                                 │
 │  📁 app                         │
 │  ├── 🐍 __init__.py             │
 │  └── 🐍 main.py                 │
 │                                 │
 ╰─────────────────────────────────╯

INFO     Importing module app.main
INFO     Found importable FastAPI app

 ╭── Importable FastAPI app ──╮
 │                            │
 │  from app.main import app  │
 │                            │
 ╰────────────────────────────╯

INFO     Using import string app.main:app

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/Users/rhoboro/go/src/github.com/rhoboro/async-fastapi-sqlalchemy']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [47967] using WatchFiles
INFO:     Started server process [47969]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Test

```shell
$ uv sync --fronzen --group testing
$ uv run black app
$ uv run ruff check app
$ uv run mypy app
$ uv run pytest app
```
