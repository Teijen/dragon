# Coreutils

We build coreutils v9.0 and include all binaries except those found in the `gnulib-tests` folder,
resulting in 109 binaries
* Source:  https://ftp.gnu.org/gnu/coreutils/coreutils-9.0.tar.gz

~~~
$ find_binaries ../../build/coreutils_v8.32/run1/ | grep -v gnulib-tests | wc -l
109
~~~

# Complex Benchmark

## OpenSSL

We build OpenSSL v1.1.1k, and use the `libssl.so` binary
* Source: https://github.com/openssl/openssl.git
* Tag: `OpenSSL_1_1_1k`

## Nginx

We build Nginx 1.26.2, and use the `nginx` binary
* Source https://nginx.org/download/nginx-1.26.2.tar.gz

## Redis

We build Redis 7.2.4, and use the `redis-server` binary
* Source https://github.com/redis/redis/archive/refs/tags/7.2.4.tar.gz

## PostgreSQL

We build PostgreSQL 17.2, and use the `postgres` binary
* Source https://ftp.postgresql.org/pub/source/v17.2/postgresql-17.2.tar.gz

# ReSym Test Binaries

We include all the binaries present in ReSym's test set, which can be downloaded as part
of the ReSym data.

* Main repo: https://github.com/lt-asset/resym
* Data files: https://zenodo.org/records/13923982
