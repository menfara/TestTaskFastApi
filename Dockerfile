FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src/

RUN pip install pipenv==2023.6.18

COPY Pipfile Pipfile.lock /src/

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /src/
