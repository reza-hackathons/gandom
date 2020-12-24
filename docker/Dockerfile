FROM frolvlad/alpine-gxx:latest

VOLUME /golem/work /golem/output /golem/resources

RUN apk --no-cache add make cmake bash

COPY libchaos-master /opt/libchaos-master
RUN cd /opt/libchaos-master && ./install.sh

COPY gen_random.cc /opt/gen_random.cc
RUN cd /opt && g++ gen_random.cc -lchaos -o gen_random

WORKDIR /golem/work

