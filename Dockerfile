FROM python:3.6.13-alpine3.13

ENV PYTHONUNBUFFERED 1

# RUN apk update \
#     && apk add \
#     build-base \
#     gcc \
#     musl-dev \
#     python3-dev \
#     libffi-dev \
#     libressl-dev \
#     cargo \
#     libxml2-dev \
#     libxslt-dev \
#     mariadb-dev
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./ /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.8.0/wait /wait
RUN chmod +x /wait