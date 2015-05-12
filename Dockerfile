FROM ubuntu

MAINTAINER Dan <dan@kolbman.com>

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y vim tar git curl wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

ADD ./ /tblog

# Get pip to download and install requirements:
RUN pip install -r /tblog/requirements.txt


WORKDIR /tblog

CMD python app.py &
