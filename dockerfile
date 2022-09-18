FROM python:latest

RUN pip install poetry

WORKDIR /app

COPY /app /app

RUN poetry config virtualenvs.create false && poetry install

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]