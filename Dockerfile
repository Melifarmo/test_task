FROM python:3.11-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# ставим зависимости в системный python
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /app

EXPOSE 8000

CMD alembic upgrade head && \
    python fill_db.py && \
    gunicorn "app.main:get_application()" \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:8000 \
        --timeout 600 \
        --forwarded-allow-ips='*' \
        --worker-tmp-dir /dev/shm
