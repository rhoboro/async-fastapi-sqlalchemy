FastAPI+SQLAlchemy Async Sample

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.lock
(venv) $ APP_CONFIG_FILE=local gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app.main:app
```

