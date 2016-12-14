FROM ubuntu:16.04

ENV SLIMERJS_VERSION 0.10.2
ENV FIREFOX_VERSION 49.0.2

RUN apt-get update && \
    apt-get install -y bash vim git wget xvfb unzip python curl httpie tree bzip2 lsb-release libasound2 libatk1.0-0 libc6 libcairo-gobject2 libcairo2 libdbus-1-3 libdbus-glib-1-2 libfontconfig1 libfreetype6 libgcc1 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libgtk2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libstartup-notification0 libstdc++6 libx11-6 libx11-xcb1 libxcb-shm0 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrender1 libxt6 && \
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

WORKDIR /src
COPY run-inner.sh /src/run-inner.sh
COPY src /src

CMD ["/usr/bin/slimerjs"]
