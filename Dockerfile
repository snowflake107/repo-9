FROM ubuntu:latest

RUN apt-get update>/dev/null &&  apt-get install -y apache2 >/dev/null

RUN echo "Image generated" > /var/www/html/index.html
COPY test.html /var/www/html/test.html

EXPOSE 80
CMD /usr/sbin/apache2ctl -D FOREGROUND
