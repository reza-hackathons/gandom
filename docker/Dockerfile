FROM frolvlad/alpine-gxx:latest

VOLUME /golem/work /golem/output /golem/resources

RUN apk --no-cache add make cmake bash libsodium-dev

COPY libchaos-master /opt/libchaos-master
RUN cd /opt/libchaos-master && ./install.sh

COPY generators /opt/generators
RUN cd /opt/generators && g++ chaos_prng.cc -lchaos -o chaos_prng
RUN cd /opt/generators && g++ csprng.cc -lsodium -o csprng

WORKDIR /golem/work

