FROM python:3.5

RUN pip install behave selenium ipython ipdb behave-pytest

# Install dockerize https://github.com/jwilder/dockerize
RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.3.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN mkdir -p /app
WORKDIR /app
ADD . /app/
