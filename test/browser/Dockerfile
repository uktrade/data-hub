FROM ubuntu:16.04

ENV SLIMERJS_VERSION 0.10.2
ENV FIREFOX_VERSION 50.0

RUN apt-get update && \
    apt-get install -y vim git wget xvfb libxrender-dev libasound2 libdbus-glib-1-2 libgtk-3-0 unzip python curl httpie tree && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*

RUN curl -Lfs http://download.slimerjs.org/releases/$SLIMERJS_VERSION/slimerjs-$SLIMERJS_VERSION.zip -o /tmp/slimerjs-$SLIMERJS_VERSION.zip && \
    unzip -o /tmp/slimerjs-$SLIMERJS_VERSION.zip -d /usr/local && \
    rm -f /tmp/slimerjs-$SLIMERJS_VERSION.zip && \
    mv /usr/local/slimerjs-$SLIMERJS_VERSION /usr/local/slimerjs

RUN git clone https://github.com/casperjs/casperjs.git /usr/local/casperjs

RUN curl -Lfs https://ftp.mozilla.org/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 | tar -xjv -C /usr/local/

RUN ln -sf /usr/local/slimerjs/slimerjs /usr/bin/slimerjs
RUN ln -sf /usr/local/casperjs/bin/casperjs /usr/bin/casperjs
RUN ln -snf /usr/local/firefox/firefox /usr/bin/firefox
RUN ln -snf /usr/local/firefox/firefox-bin /usr/bin/firefox-bin

COPY src /src
COPY run-inner.sh /src/run-inner.sh
WORKDIR /src

ENTRYPOINT ["/usr/bin/slimerjs"]
