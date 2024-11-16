FROM ubuntu:22.04

# Setup tzdata, otherwise it will ask for input and stop the build
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Base libraries for build
# libclang1-10, python3-clang-10 
RUN apt-get update
RUN apt-get install -y bison flex gawk gcc g++ llvm \
                        make ninja-build m4 patch pkg-config \
                        python-is-python3 tar zip \
                        automake bc binfmt-support cmake dpkg-dev \
                        libelf-dev libncurses5-dev libssl-dev \
                        mesa-common-dev opencl-headers perl qemu \
                        qemu-user-static texinfo wget xutils-dev \
                        python3-pip \
                        autopoint gperf intltool libglib2.0-dev \
                        libltdl-dev libtool python3-libxml2 python3-mako \
                        xfonts-utils xsltproc x11-xkb-utils \
                        clang-11 python3-clang python2


RUN pip3 install --trusted-host pypi.org \
                 --trusted-host files.pythonhosted.org \
                 meson

RUN update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-11/bin/clang 50

# Kernel Headers (G1)
ADD ./build-tools/linux-headers-5.15.0-37-generic.tar.gz /opt
#ADD ./build-tools/linux-headers-5.15.0-89-generic.tar.gz /opt
#RUN apt-get install -y linux-headers-5.15.0-37-generic

# Systoot
ADD ./build-tools/ubuntu-2204-amd64-i386.tar.xz /opt
#ADD ./build-tools/ubuntu-2004-amd64-i386.tar.xz /opt

# Meta toolkit
ADD ./build-tools/Meta_Embedded_Toolkit-2.8.1.CentOS-5.tar.gz /
RUN /Meta_Embedded_Toolkit-2.8.1.CentOS-5/install.sh

# RISC-V Toolkit
COPY ./build-tools/catapult-sdk_1.0.1.deb /
RUN apt-get update && apt-get install -y /catapult-sdk_1.0.1.deb

# To build rogueobjanal/fsim
RUN apt-get install -y libpng-dev

# Add LLVM
ADD ./build-tools/llvm.x86_64.tar.gz /llvm

# To pvrvncserver
RUN apt-get install -y libvncserver-dev
