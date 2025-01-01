# Coreutils
We build coreutils v8.32 and include all binaries except those found in the `gnulib-tests` folder,
resulting in 109 binaries
* Source:  https://github.com/coreutils/coreutils.git
* Tag: `v8.32`

~~~
$ find_binaries ../../build/coreutils_v8.32/run1/ | grep -v gnulib-tests | wc -l
109
~~~

# OpenSSL

We build OpenSSL v1.1.1k
* Source: https://github.com/openssl/openssl.git
* Tag: `OpenSSL_1_1_1k`

# Nginx

We build nginx 1.26.2
* Source https://nginx.org/download/nginx-1.26.2.tar.gz

# ReSym Test Binaries

We include all the binaries present in ReSym's test set, which can be downloaded as part
of the ReSym data.

* Main repo: https://github.com/lt-asset/resym
* Data files: https://zenodo.org/records/13923982
