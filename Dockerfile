FROM python:3.6.0
MAINTAINER Jackeriss <i@jackeriss.com>

RUN mkdir -p /usr/src/top15
WORKDIR /usr/src/top15
COPY . /usr/src/top15

RUN apt-get update
RUN apt-get -y install cron
RUN pip3 install -r requirements/common.txt
ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN touch /var/log/cron.log

EXPOSE 8082

CMD ["bash","run.sh"]
