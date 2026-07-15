FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y graphviz && \
    rm -rf /var/lib/apt/list/*

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]