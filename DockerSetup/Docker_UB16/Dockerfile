FROM ubuntu:16.04

# Base libraries for build
# Following 1.7 platform guide, plus a few others (first line)
# lib32z1-dev => zconf.h was made multiarch and the packages don't seem to include a 32bit arch header
# libc6-i386 lib32z1 lib32stdc++6 lib32z1-dev => missing standard libs on i386 for multiarch
RUN apt-get update && apt-get install -y \
	build-essential python pkg-config \
	m4 flex bison patch gawk zip \
	automake libssl-dev libtool xutils-dev \
	lib32z1 lib32stdc++6 lib32z1-dev\
	gcc-multilib g++-multilib \
	libdrm-dev\
	libpng12-dev wget \
	libudev-dev \
	python3-minimal \
	python-pip \
	cmake \
	lcov \
	clang

# Meta toolkit
ADD example.tar.gz /
RUN /example/install.sh

# install clang for python
RUN pip install clang-5

RUN mkdir /sample
COPY sample/yas* /sample/
RUN dpkg -i /amd64.deb

RUN apt-get update && apt-get install -y \
	linux-headers-4.15.0-72-generic

ENV PATH="${PATH}:/opt/poky/2.4.3/sysroots/x86_64-pokysdk-linux/usr/bin/aarch64-poky-linux/"



