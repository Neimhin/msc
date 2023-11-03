openssl_dir="$HOME/msc/dissertation-stealthy-ech/openssl"
export LD_LIBRARY_PATH=$openssl_dir:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
# -L/usr/lib/x86_64-linux-gnu
LDFLAGS="-L$openssl_dir" ./configure \
	--with-ssl=$openssl_dir \
	--enable-ech \
	--enable-httpsrr

