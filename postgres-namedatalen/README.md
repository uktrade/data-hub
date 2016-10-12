Postgres container that allows for 512 field length
---------------------------------------------------

Container is exposing identical interface to
`https://hub.docker.com/r/_/postgres/`
but is patched with
`#define NAMEDATALEN 512`
