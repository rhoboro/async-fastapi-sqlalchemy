FastAPI+SQLAlchemy Async Sample

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.lock
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=password \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13.3
(venv) $ APP_CONFIG_FILE=local gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app.main:app
```

```shell
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
