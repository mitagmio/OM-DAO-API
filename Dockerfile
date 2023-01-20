FROM tiangolo/uvicorn-gunicorn:python3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-ansi

COPY ./app /code/app
COPY ./alembic /code/alembic
COPY alembic.ini /code/alembic.ini
COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]