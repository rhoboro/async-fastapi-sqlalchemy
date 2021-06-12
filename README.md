FastAPI+SQLAlchemy Async Sample

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.lock
```

## Setup a databaase and create tables

```
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=password \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13.3
(venv) $ APP_CONFIG_FILE=local python3 -m asyncio
>>> import asyncio
>>> from app.db import async_engine
>>> from app.models.base import Base
>>> async with async_engine.begin() as conn:
...   await conn.run_sync(Base.metadata.drop_all)
...   await conn.run_sync(Base.metadata.create_all)
>>>
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
