# THIS IS WHERE YOU SPECIFY THE BASE IMAGE
# THE BASE IMAGE IS HOW YOU CHOOSE WHICH EMBEDDED PLATFORM YOU WANT TO USE
# LEARN MORE ABOUT BASE IMAGES AND SUPPORTED PLATFORMS HERE:
# https://www.balena.io/docs/reference/base-images/base-images/
#Pi3
# FROM balenalib/raspberrypi3-ubuntu:latest
#Pi4
FROM balenalib/raspberrypi4-64-ubuntu:latest
#Odroid XU4
#FROM balenalib/odroid-xu4-ubuntu
# FROM balenalib/raspberrypi3-64-debian

RUN apt-get update && \
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
	gpg \
	rsync \
	fail2ban \
	vim \
	systemd \
	whiptail \
	dphys-swapfile \
	openssh-server \
	sshfs \
	libevent-dev \
	openssl \
	zlib1g-dev \
	&& \
	rm -rf /var/lib/apt/lists/*

# TOR
#apt install libevent-dev
#apt install openssl
#apt install zlib1g-dev

RUN pip3 install -U pip setuptools
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Create python environment and install dependancies
RUN python3 -m venv env --without-pip
COPY ./requirements.txt /requirements.txt

# Enter python environment and install packages 
RUN /bin/bash -c 'source /usr/src/app/env/bin/activate && pip3 install -r /requirements.txt --only-binary=:all: --python-version 36 --implementation cp --abi cp36m --platform=linux_armv7l --extra-index-url https://www.piwheels.org/simple --target /usr/src/app/env/lib/python3.6/site-packages'



# Generate a swapfile, and copy to SSD?
# RUN dphys-swapfile swapoff && \
# 	sudo dphys-swapfile uninstall && \
# 	echo "CONF_SWAPFILE=/root/swapfile" >> /etc/dphys-swapfile

# RUN dd if=/dev/zero of=/root/swapfile count=1000 bs=1MiB && \
# 	chmod 
#600 /root/swapfile && \
# 	mkswap /root/swapfile && \
# 	dphys-swapfile setup

# This should bring you into python environment on boot
RUN echo "source /usr/src/app/env/bin/activate" >> /etc/bash.bashrc && echo "source /etc/bash.bashrc" >> /etc/profile

RUN curl https://dist.torproject.org/tor-0.4.3.6.tar.gz | tar -xvz
#	./configure && \
#	make && \


# Install GO!
RUN curl https://dl.google.com/go/go1.14.4.linux-arm64.tar.gz | tar -C /usr/local -xvz && mkdir -p /usr/src/app/go

# Do GO environment things to we can use it
ENV GOPATH="/usr/src/app/go"
ENV PATH="/usr/local/go/bin:$GOPATH/bin:$PATH"

# Install the latest version of LND!
RUN go get -d -v github.com/lightningnetwork/lnd && \
  cd $GOPATH/src/github.com/lightningnetwork/lnd && \
  make && make install tags="experimental autopilotrpc signrpc walletrpc chainrpc invoicesrpc routerrpc watchtowerrpc dev"

ENV VERSION 0.0.1

# Update this last, so we dont have to rebuild LND
RUN pip3 install git+https://github.com/sako0938/lnd_pyshell

# Copy the startup script to the image
COPY start /usr/src/app
COPY start_wowee /usr/src/app
COPY scripts /usr/src/app/scripts
# COPY code /usr/src/app/code



# Need to make a docker-gen file...
# *****************************
# *****************************

# *****************************
# *****************************

ENV INITSYSTEM on
#CMD ["bash", "start"]

# use the start script for bitcoind / litecoind (core) & lnd
ENTRYPOINT exec /usr/src/app/start

# use the start_wowee script for btcd / ltcd & lnd/neutrino (golang)
#ENTRYPOINT exec /usr/src/app/start_wowee

