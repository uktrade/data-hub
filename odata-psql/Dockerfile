# This is here for testing purposes only
FROM python:3.5.2

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install ipdb

ADD . /src
WORKDIR /src
CMD py.test
