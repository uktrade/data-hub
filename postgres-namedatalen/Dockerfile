FROM ubuntu

# explicitly set user/group IDs
RUN groupadd -r postgres --gid=999 && useradd -r -g postgres --uid=999 postgres

# Custom PostgreSQL compilation
RUN apt-get update -y
# libbison-dev gzip git build-essential libreadline-dev zlib1g-dev
RUN apt-get install -y  postgresql-server-dev-all libbison-dev git build-essential gzip libreadline-dev zlib1g-dev flex
RUN apt-get remove -y postgresql-server-dev-all
RUN mkdir -p /tmp/build
WORKDIR /tmp/build
RUN git clone https://github.com/postgres/postgres.git
ADD namedatelen.patch /tmp/build
WORKDIR /tmp/build/postgres
RUN git checkout "REL9_5_3"
RUN git apply ../namedatelen.patch
RUN ./configure
RUN make
RUN make install

RUN apt-get install -y gosu

ENV PATH /usr/local/pgsql/bin/:$PATH
ENV PGDATA /var/lib/postgresql/data

VOLUME /var/lib/postgresql/data



WORKDIR /
ADD docker-entrypoint.sh /
RUN chmod a+x docker-entrypoint.sh


ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5432
CMD ["postgres"]
