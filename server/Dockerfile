FROM python:3.10

COPY . /my_task_api
WORKDIR /my_task_api

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/my_task_api/src

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

CMD ["make", "run-local"]
