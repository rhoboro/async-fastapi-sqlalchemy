# Async Web API with FastAPI + SQLAlchemy 2.0 Style

This is a sample project of Async Web API with FastAPI + SQLAlchemy 2.0 Style.
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
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:14.4-alpine

(venv) $ APP_CONFIG_FILE=local alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local uvicorn app.main:app --reload-dir app
```

You can now access [localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.


# Test

```shell
(venv) $ pip install -r requirements_test.txt
(venv) $ black app
(venv) $ isort app
(venv) $ mypy app
(venv) $ pytest app
```
