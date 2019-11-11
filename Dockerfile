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
	sshfs && \
	rm -rf /var/lib/apt/lists/*

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
# 	chmod 600 /root/swapfile && \
# 	mkswap /root/swapfile && \
# 	dphys-swapfile setup

# This should bring you into python environment on boot
RUN echo "source /usr/src/app/env/bin/activate" >> /etc/bash.bashrc && echo "source /etc/bash.bashrc" >> /etc/profile

# Install go
# echo "golang not found, installing!"
# echo "download & install of golang 12.7"
# sha256sum go1.12.7.linux-armv6l.tar.gz | awk -F " " '{ print $1 }' \
# echo "The final output of the command above should be 48edbe936e9eb74f259bfc4b621fafca4d4ec43156b4ee7bd0d979f257dcd60a" \
ENV GO_BIN go1.13.4.linux-arm64.tar.gz
# RUN wget -nv --report-speed=bits https://dl.google.com/go/go1.13.4.linux-armv6l.tar.gz


RUN wget -nv --report-speed=bits https://dl.google.com/go/$GO_BIN
RUN tar -xvzf $GO_BIN -C /root

RUN mkdir /root/gocode
RUN echo "export GOPATH=$HOME/go\nexport PATH=$PATH:$GOPATH/bin" >> /root/.profile

# export GOPATH=/root/gocode\nexport PATH=$PATH:$GOPATH/bin" >> /etc/bash.bashrc
# RUN bash -c "source $HOME/.profile && env && go version"
ENV VERSION 0.0.1

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

