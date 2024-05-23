FROM python:3.11-slim as base
LABEL maintainer="https://github.com/Vladislav-Shi"

ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

# Инициализация проекта
WORKDIR ../
#ENTRYPOINT ["./docker-entrypoint.sh"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка питонячьих библиотек
COPY pyproject.toml .
COPY poetry.lock .

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копирование в контейнер папок и файлов.
COPY . .
CMD ["python", "run.py"]
