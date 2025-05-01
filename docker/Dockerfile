FROM python:3.12-slim-bookworm AS base

WORKDIR /opt/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/opt/src


COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN apt-get update \
    && apt-get install -y make \
    && pip install --upgrade pip \
    && pip install setuptools poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root \
    && pip cache purge


# =============== #
# ===== Dev ===== #
# =============== #
FROM base AS dev
COPY . .
RUN poetry install --only-root
ENTRYPOINT ["/bin/sh", "-c", "poetry run python /opt/manage.py runserver 0.0.0.0:8000"]
