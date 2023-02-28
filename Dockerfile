FROM python:slim-buster

WORKDIR /app

COPY . .

RUN mkdir /var/log/gunicorn

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Fake Secret key for testing purposes
ENV SECRET_KEY '+ulbdw9rocx92m6z9*_^d4ct*g5vf7a#4h32ph2p$-_%yskyr='
ENV DEBUG 'true'

CMD ["daphne", "thender.asgi:application", "-b", "0.0.0.0", "-p", "8000"]