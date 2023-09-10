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
  postgres:15.2-alpine

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

```shell
(venv) $ APP_CONFIG_FILE=local uvicorn app.main:app --reload --reload-dir app
INFO:     Will watch for changes in these directories: ['/Users/rhoboro/go/src/github.com/rhoboro/async-fastapi-sqlalchemy/app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [49448] using WatchFiles
INFO:     Started server process [49450]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can now access [localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

# Test

```shell
(venv) $ pip install -r requirements_test.txt
(venv) $ black app
(venv) $ ruff app
(venv) $ mypy app
(venv) $ pytest app
```
