#Pi3
#FROM balenalib/raspberrypi3-ubuntu:latest
#Odroid XU4
FROM balenalib/odroid-xu4-ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	git \
	wget \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	python3-venv \
	nginx \
	supervisor \
	nano \
	# sha256sum \
	gpg \
	rsync \
	fail2ban \
	vim \
	systemd \
	sshfs && \
	pip3 install -U pip setuptools && \
rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Create python environment and install dependancies
RUN python3 -m venv env --without-pip
COPY ./requirements.txt /requirements.txt

# Enter python environment and install packages 
RUN /bin/bash -c 'source /usr/src/app/env/bin/activate && pip3 install -r /requirements.txt --only-binary=:all: --python-version 36 --implementation cp --abi cp36m --platform=linux_armv7l --extra-index-url https://www.piwheels.org/simple --target /usr/src/app/env/lib/python3.6/site-packages'

# This should bring you into python environment on boot
RUN echo "source /usr/src/app/env/bin/activate" >> /etc/bash.bashrc && echo "source /etc/bash.bashrc" >> /etc/profile

ENV VERSION 0.0.1
COPY start /usr/src/app

COPY code /usr/src/app/code

# Need to make a docker-gen file...
# *****************************
# *****************************

# *****************************
# *****************************

ENV INITSYSTEM on
CMD ["bash", "start"]