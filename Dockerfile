FROM python:3.6.0
MAINTAINER Jackeriss <i@jackeriss.com>

RUN mkdir -p /usr/src/top15
WORKDIR /usr/src/top15
COPY . /usr/src/top15

RUN pip3 install -r requirements/common.txt
RUN crontab updateAll.cron

EXPOSE 8000

CMD ["python","application.py"]
