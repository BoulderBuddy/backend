FROM python:3.10.4-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

RUN apt-get update \
  && apt-get -y install netcat gcc libffi-dev \
  && apt-get clean

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock .
#RUN . /venv/bin/activate && poetry install --no-root $(test "$YOUR_ENV" == production && echo "--no-dev")
RUN . /venv/bin/activate && poetry install --no-root --no-dev

COPY . .
RUN . /venv/bin/activate && poetry build

FROM base as final

ENV PATH="/venv/bin:${PATH}" \
   VIRTUAL_ENV="/venv"

COPY --from=builder /venv /venv
COPY --from=builder /app/dist .

RUN . /venv/bin/activate && pip install *.whl

ENTRYPOINT []

CMD ["./entrypoint.sh"]
