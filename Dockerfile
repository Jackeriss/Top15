FROM python:3.6.0
MAINTAINER Jackeriss <i@jackeriss.com>

RUN mkdir -p /usr/src/top15
WORKDIR /usr/src/top15
COPY . /usr/src/top15

RUN pip3 install -r requirements/prod.txt

EXPOSE 8082

CMD ["bash","run.sh"]
