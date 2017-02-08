FROM python:3.6.0
MAINTAINER Jackeriss <i@jackeriss.com>

RUN mkdir -p /usr/src/top15
WORKDIR /usr/src/top15
COPY . /usr/src/top15

RUN apt-get update
RUN apt-get install crontab
RUN pip3 install -r requirements/common.txt
RUN crontab /usr/src/top15/crontabfile
RUN cp /usr/src/top15/crontabfile /etc/crontab
RUN touch /var/log/cron.log
RUN chmod +x /usr/src/top15/run.sh

WORKDIR /usr/src/top15

EXPOSE 8000

CMD ["bash","/usr/src/top15/run.sh"]
