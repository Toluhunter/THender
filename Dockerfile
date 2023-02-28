FROM python:slim-buster

WORKDIR /app

COPY . .

RUN mkdir /var/log/gunicorn

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD ["daphne", "thender.asgi:application", "--bind", "0.0.0.0:80000"]