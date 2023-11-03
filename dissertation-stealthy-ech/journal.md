## 2nd November 2023
Going to try to compile Stephen Farrell's branch of OpenSSL, which has an implementation of ECH.
[git@github.com:sftcd/openssl.git](sftcd's OpenSSL)
Looking at ECH-draft-13c branch
#### steps (build openssl with ech support):
- install prerequisites:
	- ```apt install libtext-template-perl```
- run configure with prefix
	- `./Configure --prefix=/opt/openssl-ECH-draft-13c`
- run make:
	- got the following error logs:
```log
./util/libssl.num: No new symbols added
./util/libssl.num: 80 symbols are without ordinal number
./util/libcrypto.num: No new symbols added
./util/libcrypto.num: 109 symbols are without ordinal number
```

#### steps (build curl with ech using openssl just built):
- instructions: https://github.com/sftcd/curl/blob/ECH-experimental/docs/ECH.md
- [sftcd's curl fork](git@github.com:sftcd/curl.git)
- Use branch ECH-experimental
- install dependencies:
```bash
 1857  sudo apt install libldap2-dev
 1858  sudo apt install libpsl-dev
 1859  sudo apt install libgsasl7 libgsasl7-dev
 1860  sudo apt install libgsasl7
 1861  sudo apt install gsasl-common libgsasl7-dev
 1862  sudo apt install libidn11-dev
```
- configure:
```bash
export LD_LIBRARY_PATH=$HOME/msc/dissertation-stealthy-ech/openssl
LDFLAGS="-L$HOME/msc/dissertation-stealthy-ech/openssl" ./configure --with-ssl=$HOME/msc/dissertation-stealthy-ech/openssl --enable-ech --enable-httpsrr
```
- run cmake:
```bash
cmake -DOPENSSL_ROOT_DIR=$HOME/msc/dissertation-stealthy-ech/openssl -DUSE_ECH=1 -DUSE_HTTPSRR=1 -DUSE_MANUAL=1 ..
```
- make:
- fails with errors about undefined references to brotli and gsasl
UNFINISHED

#### steps (build curl with ech make, not cmake):
- 

