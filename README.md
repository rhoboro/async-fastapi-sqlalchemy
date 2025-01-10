# Async Web API with FastAPI + SQLAlchemy 2.0

This is a sample project of Async Web API with FastAPI + SQLAlchemy 2.0.
It includes asynchronous DB access using asyncpg and test code covering them.

This sample project is explained in this blog (written in Japanese).  
https://www.rhoboro.com/2021/06/12/async-fastapi-sqlalchemy.html

If you want to use prisma instead of sqlalchemy, see [rhoboro/async-fastapi-prisma](https://github.com/rhoboro/async-fastapi-prisma).

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.lock
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=password \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:16.3-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

(venv) $ APP_CONFIG_FILE=local alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

After start-up, you can access [localhost:8000/docs](http://localhost:8000/docs) to see the api documentation.

## Using `fastapi dev`

[The fastapi>=0.111.0 has a `fastapi` command.](https://fastapi.tiangolo.com/release-notes/#01110)

```shell
(venv) $ APP_CONFIG_FILE=local fastapi dev
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

## Using uvicorn's multiprocess manager

[The uvicorn>=0.30.0 has a new multiprocess manager.](https://fastapiexpert.com/blog/2024/05/28/uvicorn-0300-release/#add-a-new-multiprocess-manager)

```shell
(venv) $ APP_CONFIG_FILE=local uvicorn --workers 4 app.main:app
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started parent process [46740]
INFO:     Started server process [46744]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Started server process [46742]
INFO:     Waiting for application startup.
INFO:     Started server process [46745]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Application startup complete.
INFO:     Started server process [46743]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

# Test

```shell
(venv) $ pip install -r requirements_test.txt
(venv) $ black app
(venv) $ ruff check app
(venv) $ mypy app
(venv) $ pytest app
```
