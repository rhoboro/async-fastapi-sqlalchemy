FROM python:3.13-slim

WORKDIR /app
RUN groupadd -r app \
  && useradd --no-log-init -m -g app app \
  && chown app /app
USER app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
RUN --mount=type=cache,target=/app/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY --chown=app:app . /app
RUN --mount=type=cache,target=/app/.cache/uv \
    uv sync --frozen

EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
