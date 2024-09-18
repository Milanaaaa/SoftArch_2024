FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY server .

CMD poetry run uvicorn main:app \
 --forwarded-allow-ips='*' \
 --host 0.0.0.0 --port 8000
