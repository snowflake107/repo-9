FROM ubuntu:latest

RUN apt-get update>/dev/null &&  apt-get install -y apache2 curl >/dev/null

RUN echo "Image generated" > /var/www/html/index.html
COPY test.html /var/www/html/test.html

EXPOSE 80
USER root
CMD /usr/sbin/apache2ctl -D FOREGROUND
