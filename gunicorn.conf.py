import os as _os
import json as _json

# refs. https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/8748ba16cb9d4c8e4e5a99975438159ada14322c/docker-images/gunicorn_conf.py
bind = "0.0.0.0:80"
loglevel = "info"
accesslog = "-"
errorlog = "-"
graceful_timeout = 120
timeout = 120
keepalive = 5
# worker_tmp_dir = "/dev/shm"

_cores = _os.cpu_count() or 1
if _max_workers := _os.getenv("MAX_WORKERS"):
    workers = min(_cores, int(_max_workers))
else:
    workers = _cores

# For debug
print(_json.dumps({k: v for k, v in locals().items() if not k.startswith("_")}))
