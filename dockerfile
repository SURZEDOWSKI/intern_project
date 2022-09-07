FROM python:latest

RUN pip install poetry

WORKDIR /container_app

COPY . /container_app

RUN poetry config virtualenvs.create false && poetry install

WORKDIR /container_app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]