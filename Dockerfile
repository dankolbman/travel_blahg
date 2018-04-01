FROM        python:3.5

MAINTAINER  Dan Kolbman <dan@kolbman.com>

ADD         requirements.txt /app/
WORKDIR     /app
RUN         apt-get update & apt-get install gcc -y
RUN         pip install -r /app/requirements.txt
ADD         . /app
EXPOSE      80

ENV         FLASK_APP "manage.py"
ENV         BLOG_ENV "prod"

CMD ["gunicorn", "-b", "0.0.0.0:80", "manage:app"]
